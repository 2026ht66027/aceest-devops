from pathlib import Path
import ast
import subprocess
import sys
import pytest


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT_DIR / "source_versions"

FAULTY_VERSION = SOURCE_DIR / "Aceestver1.1.2.py"


# --------------------------------------------------
# PROJECT STRUCTURE TESTS
# --------------------------------------------------

def test_app_exists():
    """Verify that the main application exists."""
    assert (ROOT_DIR / "app.py").is_file()


def test_requirements_exists():
    """Verify that requirements.txt exists."""
    assert (ROOT_DIR / "requirements.txt").is_file()


def test_dockerfile_exists():
    """Verify that the Dockerfile exists."""
    assert (ROOT_DIR / "Dockerfile").is_file()


def test_all_source_versions_exist():
    """Verify that all ten supplied versions exist."""
    source_files = list(SOURCE_DIR.glob("*.py"))

    assert len(source_files) == 10, (
        f"Expected 10 source versions, found {len(source_files)}"
    )


def test_requirements_not_empty():
    """Verify that requirements.txt lists dependencies."""
    requirements_file = ROOT_DIR / "requirements.txt"

    requirements = [
        line.strip()
        for line in requirements_file.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert requirements, "requirements.txt must not be empty"


def test_dockerfile_has_base_image():
    """Verify that the Dockerfile contains a FROM instruction."""
    dockerfile = (ROOT_DIR / "Dockerfile").read_text(
        encoding="utf-8"
    )

    assert any(
        line.strip().upper().startswith("FROM ")
        for line in dockerfile.splitlines()
    ), "Dockerfile must contain a FROM instruction"


# --------------------------------------------------
# MAIN APPLICATION VALIDATION
# --------------------------------------------------

def test_app_syntax():
    """Compile the main application."""
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

    assert result.returncode == 0, (
        f"app.py compilation failed:\n{result.stderr}"
    )


def test_app_has_valid_python_ast():
    """Validate the Python syntax tree of app.py."""
    source_code = (ROOT_DIR / "app.py").read_text(
        encoding="utf-8"
    )

    ast.parse(source_code)


# --------------------------------------------------
# BUILD EACH SUPPLIED VERSION INDIVIDUALLY
# --------------------------------------------------

SOURCE_VERSIONS = sorted(SOURCE_DIR.glob("*.py"))


@pytest.mark.parametrize(
    "source_file",
    SOURCE_VERSIONS,
    ids=lambda path: path.name,
)
def test_source_version_compiles(source_file):
    """
    Compile each supplied version independently.

    Pytest reports a separate result for every version.
    """
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
        f"\nVersion failed: {source_file.name}\n"
        f"Error:\n{result.stderr}"
    )


@pytest.mark.parametrize(
    "source_file",
    SOURCE_VERSIONS,
    ids=lambda path: path.name,
)
def test_source_version_has_valid_ast(source_file):
    """
    Parse each supplied version independently.

    This provides a separate syntax-validation result per version.
    """
    source_code = source_file.read_text(encoding="utf-8")

    try:
        ast.parse(source_code)
    except SyntaxError as error:
        pytest.fail(
            f"{source_file.name} contains invalid Python syntax:\n"
            f"{error}"
        )


# --------------------------------------------------
# DETECT THE SUSPECTED DEFECT
# --------------------------------------------------

def test_faulty_version_reset_bug_is_detected():
    """
    Detect the suspected missing-arguments defect in version 1.1.2.

    This is a static source-code check. It does not launch the GUI.
    """
    assert FAULTY_VERSION.is_file(), (
        f"Candidate version not found: {FAULTY_VERSION}"
    )

    source_code = FAULTY_VERSION.read_text(encoding="utf-8")
    tree = ast.parse(source_code)

    update_method = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name == "_update_text":
                update_method = node
                break

    assert update_method is not None, (
        "_update_text method was not found."
    )

    parameters = (
        update_method.args.posonlyargs
        + update_method.args.args
    )

    required_arguments = len(parameters) - 1

    assert required_arguments > 0, (
        "Unexpected _update_text method signature."
    )

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
        "The suspected missing-arguments defect was not found."
    )

    print(
        f"Defect detected in {FAULTY_VERSION.name}: "
        f"{len(faulty_calls)} call(s) have missing arguments."
    )