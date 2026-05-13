#!/usr/bin/env python3
"""
Spec validator for agent-framework.

Reads JSON spec files from specs/ and verifies that each target markdown
file contains all required headings. Exits non-zero if any spec fails.

Usage:
    python scripts/validate.py [--repo-root PATH]
"""
import json
import sys
import argparse
from pathlib import Path


def load_specs(specs_dir: Path) -> list[dict]:
    specs = []
    for spec_file in sorted(specs_dir.glob("*.json")):
        with open(spec_file) as f:
            specs.append({"name": spec_file.stem, **json.load(f)})
    return specs


def get_headings(filepath: Path) -> set[str]:
    headings = set()
    for line in filepath.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.add(stripped)
    return headings


def validate(specs: list[dict], repo_root: Path) -> bool:
    passed = 0
    failed = 0
    errors = []

    for spec in specs:
        spec_name = spec["name"]
        for filepath_str, rules in spec["files"].items():
            filepath = repo_root / filepath_str
            if not filepath.exists():
                errors.append(f"  MISSING FILE: {filepath_str}")
                failed += 1
                continue

            headings = get_headings(filepath)
            missing = [h for h in rules["required_headings"] if h not in headings]

            if missing:
                errors.append(f"  FAIL [{spec_name}] {filepath_str}")
                for h in missing:
                    errors.append(f"       missing: {h}")
                failed += 1
            else:
                print(f"  ok   [{spec_name}] {filepath_str}")
                passed += 1

    if errors:
        print()
        for line in errors:
            print(line)

    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="Validate framework specs")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Path to repo root (default: parent of scripts/)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    specs_dir = repo_root / "specs"

    if not specs_dir.exists():
        print(f"ERROR: specs/ directory not found at {specs_dir}")
        sys.exit(1)

    specs = load_specs(specs_dir)
    if not specs:
        print("ERROR: no spec files found in specs/")
        sys.exit(1)

    print(f"Validating against {len(specs)} spec(s) in {specs_dir.relative_to(repo_root)}/\n")
    ok = validate(specs, repo_root)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
