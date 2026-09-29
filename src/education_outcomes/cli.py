"""Command-line reproducible benchmark."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from education_outcomes.data import (
    SOURCE_URL,
    build_provenance_manifest,
    download_data,
    load_data,
)
from education_outcomes.model import evaluate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/raw/student-por.csv"))
    parser.add_argument("--output", type=Path, default=Path("reports/baseline.json"))
    parser.add_argument(
        "--provenance-output",
        type=Path,
        default=Path("reports/provenance.json"),
        help="Where to write the versioned dataset provenance manifest",
    )
    parser.add_argument("--download", action="store_true", help="Download the public UCI data")
    args = parser.parse_args()
    try:
        retrieved_at_utc = None
        if args.download:
            download_data(args.data)
            retrieved_at_utc = datetime.now(timezone.utc)

        manifest = build_provenance_manifest(args.data, retrieved_at_utc)
        report = evaluate(load_data(args.data))
        report["provenance"] = manifest
        report["source_url"] = SOURCE_URL
        report["sha256"] = manifest["sha256"]

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
        args.provenance_output.parent.mkdir(parents=True, exist_ok=True)
        args.provenance_output.write_text(json.dumps(manifest, indent=2) + "\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
