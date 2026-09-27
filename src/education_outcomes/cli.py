"""Command-line reproducible benchmark."""
import argparse
import hashlib
import json
from pathlib import Path
from education_outcomes.data import download_data, load_data, SOURCE_URL
from education_outcomes.model import evaluate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/raw/student-por.csv"))
    parser.add_argument("--output", type=Path, default=Path("reports/baseline.json"))
    parser.add_argument("--download", action="store_true", help="Download the public UCI data")
    args = parser.parse_args()
    try:
        if args.download:
            download_data(args.data)
        report = evaluate(load_data(args.data))
        report["source_url"] = SOURCE_URL
        report["sha256"] = hashlib.sha256(args.data.read_bytes()).hexdigest()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
