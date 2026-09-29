"""Download and validate the UCI Portuguese-course dataset."""
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
import ssl
import certifi
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import pandas as pd

SOURCE_URL = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
DATASET_TITLE = "Student Performance"
CITATION = "Cortez, P. (2008). Student Performance. UCI Machine Learning Repository."
LICENSE_NAME = "Creative Commons Attribution 4.0 International (CC BY 4.0)"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
DOI_URL = "https://doi.org/10.24432/C5TG7T"
COURSE = "Portuguese"
DATA_FILE_NAME = "student-por.csv"
FEATURES = ["G1", "G2"]
TARGET = "G3"


def build_provenance_manifest(
    path: Path, retrieved_at_utc: datetime | None = None
) -> dict:
    """Build versioned source metadata for the exact dataset bytes at path."""
    if retrieved_at_utc is None:
        retrieved_at = None
    else:
        if retrieved_at_utc.tzinfo is None or retrieved_at_utc.utcoffset() is None:
            raise ValueError("retrieved_at_utc must include a timezone.")
        retrieved_at = (
            retrieved_at_utc.astimezone(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )

    return {
        "manifest_version": 1,
        "dataset_title": DATASET_TITLE,
        "citation": CITATION,
        "doi_url": DOI_URL,
        "source_url": SOURCE_URL,
        "license": LICENSE_NAME,
        "license_url": LICENSE_URL,
        "course": COURSE,
        "file_name": path.name,
        "retrieved_at_utc": retrieved_at,
        "sha256": sha256(path.read_bytes()).hexdigest(),
    }


def download_data(destination: Path) -> Path:
    """Read only the named CSV from the archive; never extract arbitrary paths."""
    with urlopen(SOURCE_URL, timeout=30, context=ssl.create_default_context(cafile=certifi.where())) as response:
        archive = ZipFile(BytesIO(response.read()))
    if "student.zip" in archive.namelist():
        archive = ZipFile(BytesIO(archive.read("student.zip")))
    payload = archive.read(DATA_FILE_NAME)
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
