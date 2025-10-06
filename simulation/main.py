"""Command line interface for running the Daimler dealership simulation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .scenario import DaimlerDealershipScenario


def run_simulation(months: int, seed: int | None, output: Path | None) -> dict[str, Any]:
    scenario = DaimlerDealershipScenario(months=months, seed=seed)
    result = scenario.run()
    summary = result.summary()
    if output:
        output.write_text(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate Daimler truck dealership competition")
    parser.add_argument("--months", type=int, default=12, help="Number of months to simulate")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write the summary JSON",
    )
    args = parser.parse_args()

    summary = run_simulation(months=args.months, seed=args.seed, output=args.output)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

