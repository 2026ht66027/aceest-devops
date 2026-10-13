from pathlib import Path
import subprocess
import sys


ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT_DIR / "source_versions"


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
    """Verify that all 10 supplied source versions are present."""
    source_files = list(SOURCE_DIR.glob("*.py"))
    assert len(source_files) == 10


def test_app_syntax():
    """Verify that app.py has valid Python syntax."""
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(ROOT_DIR / "app.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_all_source_versions_compile():
    """Verify that every supplied version compiles."""
    source_files = list(SOURCE_DIR.glob("*.py"))

    assert len(source_files) == 10, (
        "Expected all 10 supplied source versions."
    )

    for source_file in source_files:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(source_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"{source_file.name} failed compilation:\n{result.stderr}"
        )


def test_app_has_valid_python_ast():
    """Verify that app.py can be parsed as Python code."""
    app_file = ROOT_DIR / "app.py"

    with app_file.open(encoding="utf-8") as file:
        source_code = file.read()

    ast.parse(source_code)


def test_requirements_not_empty():
    """Verify that requirements.txt lists dependencies."""
    requirements_file = ROOT_DIR / "requirements.txt"

    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert requirements, "requirements.txt must list dependencies"


def test_dockerfile_has_base_image():
    """Verify that the Dockerfile specifies a base image."""
    dockerfile = (ROOT_DIR / "Dockerfile").read_text(encoding="utf-8")

    assert any(
        line.strip().upper().startswith("FROM ")
        for line in dockerfile.splitlines()
    ), "Dockerfile must contain a FROM instruction"