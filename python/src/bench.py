#!/usr/bin/env python3
"""
Simple benchmark runner for algorithms in cli/algs/

Usage:
    python bench.py manacher              # Benchmark main implementation
    python bench.py manacher --compare    # Compare main vs alt
    python bench.py manacher --test       # Run tests
"""

import sys
import importlib
import time
import statistics


def benchmark_function(func, runs=20, warmup=3):
    """
    Benchmark a function with multiple runs.

    Args:
        func: Function to benchmark
        runs: Number of benchmark runs
        warmup: Number of warmup runs (not counted)

    Returns:
        dict with timing statistics
    """
    # Warmup runs
    for _ in range(warmup):
        func()

    # Actual benchmark runs
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)

    return {
        "mean": statistics.mean(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
        "runs": runs,
    }


def format_time(seconds):
    """Format time in appropriate unit."""
    if seconds >= 1:
        return f"{seconds:.3f} sec"
    if seconds >= 0.001:
        return f"{seconds * 1000:.3f} ms"
    if seconds >= 0.000001:
        return f"{seconds * 1000000:.3f} us"

    return f"{seconds * 1000000000:.3f} ns"


def print_results(name, stats):
    """Print benchmark results in a nice format."""
    print(f"\n{name}:")
    print(f"  Mean:   {format_time(stats['mean'])} ± {format_time(stats['stdev'])}")
    print(f"  Min:    {format_time(stats['min'])}")
    print(f"  Max:    {format_time(stats['max'])}")
    print(f"  Runs:   {stats['runs']}")


def main():
    """
    Main function.
    """
    if len(sys.argv) < 2:
        print("Usage: python bench.py <algorithm> [--compare] [--test]")
        print("\nAvailable algorithms:")
        print("  - manacher")
        sys.exit(1)

    algorithm = sys.argv[1]
    compare = "--compare" in sys.argv
    test = "--test" in sys.argv

    # Import the algorithm module
    try:
        module = importlib.import_module(f"algs.{algorithm}")
    except ModuleNotFoundError:
        print(f"Error: Algorithm '{algorithm}' not found in algs/")
        sys.exit(1)

    # Run tests if requested
    if test:
        if hasattr(module, "test"):
            print(f"Running tests for {algorithm}...")
            module.test()
            return

        print(f"Error: No test() function found in {algorithm}")
        sys.exit(1)

    # Get benchmark functions
    main_func_name = f"run_{algorithm}"
    alt_func_name = "run_alt"

    if not hasattr(module, main_func_name):
        # Try without run_ prefix
        main_func_name = algorithm
        if not hasattr(module, main_func_name):
            print(f"Error: No {main_func_name}() or run_{algorithm}() function found")
            sys.exit(1)

    main_func = getattr(module, main_func_name)

    # Run benchmarks
    print(f"Benchmarking {algorithm}...")
    print("=" * 50)

    # Benchmark main implementation
    print(f"\nBenchmarking main implementation ({main_func_name})...")
    main_stats = benchmark_function(main_func)
    print_results(f"{algorithm} (main)", main_stats)

    # Benchmark alt implementation if requested
    if compare and hasattr(module, alt_func_name):
        alt_func = getattr(module, alt_func_name)
        print(f"\nBenchmarking alternative implementation ({alt_func_name})...")
        alt_stats = benchmark_function(alt_func)
        print_results(f"{algorithm} (alt)", alt_stats)

        # Print comparison
        speedup = alt_stats["mean"] / main_stats["mean"]
        print(f"\n{'Comparison:':}")
        print(f"  Main is {speedup:.2f}x faster than alt")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
