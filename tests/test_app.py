from pathlib import Path
import subprocess
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT_DIR / "source_versions"


def test_app_syntax():
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(ROOT_DIR / "app.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_all_source_versions_compile():
    source_files = list(SOURCE_DIR.glob("*.py"))

    assert len(source_files) == 10, "Expected all 10 supplied source versions."

    for source_file in source_files:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(source_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"{source_file.name} failed compilation:\n{result.stderr}"
        )