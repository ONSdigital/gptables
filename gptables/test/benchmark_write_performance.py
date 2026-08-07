"""
Benchmark script to scope writing-time performance of gptables for tables of
varying sizes.

Usage:
    python -m gptables.test.benchmark_write_performance
    python -m gptables.test.benchmark_write_performance --profile
"""

import argparse
import cProfile
import io
import pstats
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

import gptables as gpt

# Table sizes to test: (rows, cols)
SIZES = [
    (10, 5),
    (50, 5),
    (100, 5),
    (100, 20),
    (500, 10),
    (1000, 10),
    (1000, 30),
    (5000, 10),
    (10000, 10),
    (10000, 20),
    (20000, 10),
    (50000, 10),
    (100000, 10),
]


def _make_table(rows: int, cols: int) -> pd.DataFrame:
    """Generate a numeric DataFrame of the given shape with a string index column."""
    rng = np.random.default_rng(42)
    data = {
        f"col_{i}": rng.integers(0, 1000, size=rows).astype(float)
        for i in range(cols - 1)
    }
    data = {"category": [f"row_{r}" for r in range(rows)], **data}
    return pd.DataFrame(data)


def _write_once(rows: int, cols: int, tmp_path: Path) -> float:
    """Write a single GPTable workbook and return elapsed seconds."""
    table = _make_table(rows, cols)
    gptable = gpt.GPTable(
        table=table,
        table_name=f"benchmark_{rows}x{cols}",
        title=f"Benchmark table ({rows} rows x {cols} cols)",
        scope="Benchmark",
        source="Generated data",
        index_columns={1: 0},
    )
    sheets = {"Sheet1": gptable}
    outfile = tmp_path / f"benchmark_{rows}x{cols}.xlsx"

    t0 = time.perf_counter()
    wb = gpt.produce_workbook(filename=str(outfile), sheets=sheets)
    wb.close()
    return time.perf_counter() - t0


def run_benchmarks(repeats: int = 3) -> None:
    print(
        f"\n{'Rows':>6}  {'Cols':>6}  {'Cells':>8}  {'Mean (s)':>10}  {'Min (s)':>10}  {'Max (s)':>10}"
    )
    print("-" * 60)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for rows, cols in SIZES:
            times = []
            for _ in range(repeats):
                elapsed = _write_once(rows, cols, tmp_path)
                times.append(elapsed)
            cells = rows * cols
            mean_t = sum(times) / len(times)
            print(
                f"{rows:>6}  {cols:>6}  {cells:>8}  {mean_t:>10.3f}  {min(times):>10.3f}  {max(times):>10.3f}"
            )
    print()


def run_profile(rows: int = 1000, cols: int = 10) -> None:
    """Profile a single write of the given size and print the top hotspots."""
    print(f"\nProfiling write of {rows}x{cols} table ...\n")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        table = _make_table(rows, cols)
        gptable = gpt.GPTable(
            table=table,
            table_name="profile_table",
            title="Profile table",
            scope="Benchmark",
            source="Generated data",
            index_columns={1: 0},
        )
        sheets = {"Sheet1": gptable}
        outfile = tmp_path / "profile.xlsx"

        pr = cProfile.Profile()
        pr.enable()
        wb = gpt.produce_workbook(filename=str(outfile), sheets=sheets)
        wb.close()
        pr.disable()

    stream = io.StringIO()
    ps = pstats.Stats(pr, stream=stream).sort_stats("cumulative")
    ps.print_stats(30)
    print(stream.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gptables write-performance benchmark")
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Run cProfile on a 1000x10 table instead of the size sweep",
    )
    parser.add_argument(
        "--profile-size",
        nargs=2,
        type=int,
        metavar=("ROWS", "COLS"),
        default=[1000, 10],
        help="Table size to profile (default: 1000 10)",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Number of repeats per size for the benchmark sweep (default: 3)",
    )
    args = parser.parse_args()

    if args.profile:
        run_profile(*args.profile_size)
    else:
        run_benchmarks(repeats=args.repeats)
