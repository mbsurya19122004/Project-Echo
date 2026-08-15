import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
import tarfile
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

VENV_DIR = PROJECT_DIR / "venv"
MODEL_DIR = PROJECT_DIR / "models"
REQUIREMENTS = PROJECT_DIR / "requirements.txt"

MODEL_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/"
    "asr-models/"
    "sherpa-onnx-nemotron-speech-streaming-en-0.6b-560ms-int8-2026-04-25.tar.bz2"
)

MODEL_NAME = "sherpa-onnx-nemotron-speech-streaming-en-0.6b-560ms-int8-2026-04-25"
MODEL_ARCHIVE = PROJECT_DIR / "models" / f"{MODEL_NAME}.tar.bz2"


def run(command):
    print(f"\n> {' '.join(map(str, command))}")
    subprocess.check_call(command)


def venv_python():
    return (
        VENV_DIR / "Scripts" / "python.exe"
        if os.name == "nt"
        else VENV_DIR / "bin" / "python"
    )


def create_venv():
    if VENV_DIR.exists():
        print("Virtual environment already exists.")
        return

    print("Creating virtual environment...")
    run([sys.executable, "-m", "venv", str(VENV_DIR)])


def install_requirements():
    if not REQUIREMENTS.exists():
        print("requirements.txt not found. Skipping package installation.")
        return

    print("Installing requirements...")
    run([
        str(venv_python()),
        "-m",
        "pip",
        "install",
        "-r",
        str(REQUIREMENTS),
    ])


def download_model():
    if MODEL_ARCHIVE.exists():
        print("Model archive already downloaded.")
        return

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading model:\n{MODEL_URL}")

    def progress(block_num, block_size, total_size):
        if total_size <= 0:
            return

        downloaded = min(block_num * block_size, total_size)
        percent = downloaded / total_size * 100

        width = 40
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)

        downloaded_mb = downloaded / 1024**2
        total_mb = total_size / 1024**2

        print(
            f"\r[{bar}] {percent:6.2f}% "
            f"{downloaded_mb:.1f}/{total_mb:.1f} MB",
            end="",
            flush=True,
        )

    urllib.request.urlretrieve(
        MODEL_URL,
        MODEL_ARCHIVE,
        reporthook=progress,
    )

    print("\nModel download complete.")


def extract_model():
    destination = MODEL_DIR / MODEL_NAME

    if destination.exists():
        print(f"Model already exists: {destination}")
        return

    temp_dir = PROJECT_DIR / "_model_extract"

    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    temp_dir.mkdir()

    print("Extracting model...")

    if zipfile.is_zipfile(MODEL_ARCHIVE):
        with zipfile.ZipFile(MODEL_ARCHIVE) as archive:
            files = archive.infolist()
            total_size = sum(file.file_size for file in files)
            extracted = 0

            for file in files:
                archive.extract(file, temp_dir)
                extracted += file.file_size

                percent = extracted / total_size * 100 if total_size else 100
                width = 40
                filled = int(width * percent / 100)
                bar = "█" * filled + "░" * (width - filled)

                print(
                    f"\r[{bar}] {percent:6.2f}%",
                    end="",
                    flush=True,
                )

    elif tarfile.is_tarfile(MODEL_ARCHIVE):
        with tarfile.open(MODEL_ARCHIVE, "r:*") as archive:
            members = archive.getmembers()
            total_size = sum(
                member.size for member in members
                if member.isfile()
            )
            extracted = 0

            for member in members:
                archive.extract(member, temp_dir)

                if member.isfile():
                    extracted += member.size

                percent = extracted / total_size * 100 if total_size else 100
                width = 40
                filled = int(width * percent / 100)
                bar = "█" * filled + "░" * (width - filled)

                print(
                    f"\r[{bar}] {percent:6.2f}%",
                    end="",
                    flush=True,
                )

    else:
        raise RuntimeError("Downloaded model is not a supported archive.")

    print()

    entries = list(temp_dir.iterdir())

    if len(entries) == 1 and entries[0].is_dir():
        shutil.move(entries[0], destination)
    else:
        destination.mkdir()
        for entry in entries:
            shutil.move(entry, destination)

    shutil.rmtree(temp_dir)

    print(f"Model installed: {destination}")


def cleanup():
    if MODEL_ARCHIVE.exists():
        print("Removing model archive...")
        MODEL_ARCHIVE.unlink()


def main():
    print("=" * 60)
    print("Setting up project")
    print("=" * 60)

    create_venv()
    install_requirements()
    download_model()
    extract_model()
    cleanup()

    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)

    print(f"\nVirtual environment: {VENV_DIR}")
    print(f"Model:               {MODEL_DIR / MODEL_NAME}")

    if os.name != "nt":
        print(f"\nActivate with:\n  source {VENV_DIR}/bin/activate")


if __name__ == "__main__":
    main()