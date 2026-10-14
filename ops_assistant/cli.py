import argparse
import json
from pathlib import Path
from .collector import collect
from .analyzer import analyze
from .report import build_report

def main():
    parser = argparse.ArgumentParser(description="Read-only Kubernetes incident analyzer")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--fixture", help="Analyze a saved sanitized snapshot instead of a live cluster")
    args = parser.parse_args()

    if args.fixture:
        snapshot = json.loads(Path(args.fixture).read_text())
    else:
        snapshot = collect(args.namespace)

    report = build_report(snapshot, analyze(snapshot))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
