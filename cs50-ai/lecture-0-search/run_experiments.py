"""
Runs all four search algorithms on the same concept map for three real
student profiles, and prints/saves a comparison for each one.
"""

import os
from edupath import LearningProblem, solve

BASE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(BASE, "data", "linear_function_map.json")
OUTPUT_PATH = os.path.join(BASE, "output", "results.md")

# Three real student profiles based on classroom experience.
SCENARIOS = [
    {
        "name": "Student A: knows multiplication but not division",
        "initial_state": {"basic_operations", "multiplication_with_decimals"},
    },
    {
        "name": "Student B: knows equations but struggles with fractions",
        "initial_state": {"basic_operations", "multiplication_with_decimals",
                          "division", "algebraic_language", "linear_equations"},
    },
    {
        "name": "Student C: only basic operations (long path)",
        "initial_state": {"basic_operations"},
    },
]

ALGORITHMS = ["dfs", "bfs", "greedy", "astar", "astar_tight"]


def run_scenario(scenario):
    """Run all algorithms for one student profile and return result rows."""
    rows = []
    for algo in ALGORITHMS:
        problem = LearningProblem(MAP_PATH, scenario["initial_state"])
        path, explored, cost = solve(problem, algo)
        rows.append({"algorithm": algo, "explored": explored,
                     "cost": cost, "path": path})

    valid_costs = [r["cost"] for r in rows if r["cost"] is not None]
    min_cost = min(valid_costs) if valid_costs else None
    for r in rows:
        r["optimal"] = "yes" if r["cost"] == min_cost else "no"
    return rows


def main():
    all_lines = ["# Experiment Results - Lecture 0 Search (Linear Function)", ""]

    for scenario in SCENARIOS:
        print(f"\n{'=' * 70}")
        print(f"Scenario: {scenario['name']}")
        print(f"Initial state: {sorted(scenario['initial_state'])}")
        print("=" * 70)

        rows = run_scenario(scenario)

        header = f"{'Algorithm':<10} {'States explored':>16} {'Path cost':>10} {'Optimal?':>9}"
        print(header)
        print("-" * len(header))
        for r in rows:
            print(f"{r['algorithm']:<10} {r['explored']:>16} {r['cost']:>10} {r['optimal']:>9}")
        print()
        for r in rows:
            seq = " -> ".join(r["path"]) if r["path"] else "(no solution)"
            print(f"{r['algorithm']}: {seq}")

        all_lines.append(f"## {scenario['name']}")
        all_lines.append("")
        all_lines.append(f"Initial state: `{sorted(scenario['initial_state'])}`")
        all_lines.append("")
        all_lines.append("| Algorithm | States explored | Path cost | Optimal? | Sequence |")
        all_lines.append("|-----------|-----------------|-----------|----------|----------|")
        for r in rows:
            seq = " -> ".join(r["path"]) if r["path"] else "no solution"
            all_lines.append(f"| {r['algorithm']} | {r['explored']} | {r['cost']} | {r['optimal']} | {seq} |")
        all_lines.append("")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(all_lines) + "\n")
    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()