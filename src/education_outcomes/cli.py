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
    verify_sha256,
)
from education_outcomes.model import evaluate
from education_outcomes.profile import profile_dataset


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
    parser.add_argument(
        "--expected-sha256",
        help="Optional trusted 64-character checksum; mismatches stop analysis",
    )
    parser.add_argument("--download", action="store_true", help="Download the public UCI data")
    args = parser.parse_args()
    try:
        retrieved_at_utc = None
        if args.download:
            download_data(args.data, expected_sha256=args.expected_sha256)
            retrieved_at_utc = datetime.now(timezone.utc)
        elif args.expected_sha256 is not None:
            verify_sha256(args.data.read_bytes(), args.expected_sha256, args.data.name)

        manifest = build_provenance_manifest(args.data, retrieved_at_utc)
        frame = load_data(args.data)
        report = evaluate(frame)
        report["data_profile"] = profile_dataset(frame)
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
