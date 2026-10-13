from pathlib import Path
import ast
import subprocess
import sys

# Project paths
ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT_DIR / "source_versions"

FAULTY_VERSION = SOURCE_DIR / "Aceestver1.1.2.py"


def test_app_exists():
    """Verify that the main application file exists."""
    assert (ROOT_DIR / "app.py").is_file()


def test_requirements_exists():
    """Verify that the dependency file exists."""
    assert (ROOT_DIR / "requirements.txt").is_file()


def test_dockerfile_exists():
    """Verify that the Dockerfile exists."""
    assert (ROOT_DIR / "Dockerfile").is_file()


def test_all_source_versions_exist():
    """Verify that all ten supplied source versions exist."""
    source_files = list(SOURCE_DIR.glob("*.py"))

    assert len(source_files) == 10, (
        f"Expected 10 source versions, found {len(source_files)}"
    )


def test_requirements_not_empty():
    """Verify that requirements.txt contains dependencies."""
    requirements_file = ROOT_DIR / "requirements.txt"

    requirements = [
        line.strip()
        for line in requirements_file.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert requirements, "requirements.txt must list dependencies"


def test_dockerfile_has_base_image():
    """Verify that the Dockerfile specifies a base image."""
    dockerfile = (ROOT_DIR / "Dockerfile").read_text(
        encoding="utf-8"
    )

    assert any(
        line.strip().upper().startswith("FROM ")
        for line in dockerfile.splitlines()
    ), "Dockerfile must contain a FROM instruction"


def test_app_syntax():
    """Verify that app.py compiles successfully."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "py_compile",
            str(ROOT_DIR / "app.py"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_all_source_versions_compile():
    """Verify that all ten supplied source versions compile."""
    source_files = list(SOURCE_DIR.glob("*.py"))

    assert len(source_files) == 10, (
        "Expected all 10 supplied source versions."
    )

    for source_file in source_files:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "py_compile",
                str(source_file),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, (
            f"{source_file.name} failed compilation:\n"
            f"{result.stderr}"
        )


def test_app_has_valid_python_ast():
    """Verify that app.py can be parsed as Python code."""
    source_code = (ROOT_DIR / "app.py").read_text(
        encoding="utf-8"
    )

    ast.parse(source_code)


def test_faulty_version_reset_bug_is_detected():
    """
    Detect a call to _update_text() with missing positional arguments.

    This test passes when the suspected defect is present.
    It does not launch the GUI or reproduce the runtime exception.
    """
    assert FAULTY_VERSION.is_file(), (
        f"Candidate source file not found: {FAULTY_VERSION}"
    )

    source_code = FAULTY_VERSION.read_text(encoding="utf-8")
    tree = ast.parse(source_code)

    # Find the _update_text method.
    update_method = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == "_update_text":
                update_method = node
                break

    assert update_method is not None, (
        "_update_text method was not found in the candidate version."
    )

    # Count positional parameters, including self.
    parameters = (
        update_method.args.posonlyargs
        + update_method.args.args
    )

    required_arguments = len(parameters) - 1

    assert required_arguments > 0, (
        "_update_text does not have the expected parameters."
    )

    # Find calls to self._update_text() with too few arguments.
    faulty_calls = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func

        if not (
            isinstance(function, ast.Attribute)
            and function.attr == "_update_text"
            and isinstance(function.value, ast.Name)
            and function.value.id == "self"
        ):
            continue

        if len(node.args) < required_arguments:
            faulty_calls.append(node)

    assert faulty_calls, (
        "No missing-arguments call was found in the candidate version."
    )

    print(
        f"Defect detected: found {len(faulty_calls)} "
        "call(s) to _update_text() with missing arguments."
    )