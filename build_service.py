from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SPEC_FILE = PROJECT_ROOT / "service_stop_windows_update.spec"


def build_app(spec_file: Path = SPEC_FILE) -> None:
    if not spec_file.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_file}")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_file),
    ]
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)


if __name__ == "__main__":
    build_app()