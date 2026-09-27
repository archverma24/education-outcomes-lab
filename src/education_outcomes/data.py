"""Download and validate the UCI Portuguese-course dataset."""
from io import BytesIO
import ssl
import certifi
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import pandas as pd

SOURCE_URL = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
FEATURES = ["G1", "G2"]
TARGET = "G3"


def download_data(destination: Path) -> Path:
    """Read only the named CSV from the archive; never extract arbitrary paths."""
    with urlopen(SOURCE_URL, timeout=30, context=ssl.create_default_context(cafile=certifi.where())) as response:
        archive = ZipFile(BytesIO(response.read()))
    if "student.zip" in archive.namelist():
        archive = ZipFile(BytesIO(archive.read("student.zip")))
    payload = archive.read("student-por.csv")
    validate_data(pd.read_csv(BytesIO(payload), sep=";"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp")
    temporary.write_bytes(payload)
    temporary.replace(destination)
    return destination


def validate_data(frame: pd.DataFrame) -> None:
    required = FEATURES + [TARGET]
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if len(frame) < 20:
        raise ValueError("At least 20 rows are required for a train/test split.")
    for column in required:
        values = frame[column]
        if not pd.api.types.is_numeric_dtype(values):
            raise ValueError(f"{column} must be numeric.")
        if values.isna().any() or not values.between(0, 20).all():
            raise ValueError(f"{column} must contain non-missing grades from 0 to 20.")
        if (values % 1 != 0).any():
            raise ValueError(f"{column} must contain whole-number grades.")


def load_data(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, sep=";")
    validate_data(frame)
    return frame
