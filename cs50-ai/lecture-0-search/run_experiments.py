"""
Runs all four search algorithms on the same concept map and same initial
state, prints a comparison table, and saves it to output/results.md.
"""

import os
from edupath import LearningProblem, solve

BASE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(BASE, "data", "fractions_map.json")
OUTPUT_PATH = os.path.join(BASE, "output", "results.md")

# The student's prior knowledge (initial state).
INITIAL_STATE = {"natural_numbers"}

ALGORITHMS = ["dfs", "bfs", "greedy", "astar"]


def main():
    rows = []
    for algo in ALGORITHMS:
        problem = LearningProblem(MAP_PATH, INITIAL_STATE)
        path, explored, cost = solve(problem, algo)
        rows.append({"algorithm": algo, "explored": explored,
                     "cost": cost, "path": path})

    # Mark optimality: cost equal to the best found cost.
    min_cost = min(r["cost"] for r in rows if r["cost"] is not None)
    for r in rows:
        r["optimal"] = "yes" if r["cost"] == min_cost else "no"

    # Console output
    header = f"{'Algorithm':<10} {'States explored':>16} {'Path cost':>10} {'Optimal?':>9}"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r['algorithm']:<10} {r['explored']:>16} {r['cost']:>10} {r['optimal']:>9}")
    print()
    for r in rows:
        seq = " -> ".join(r["path"]) if r["path"] else "(no solution)"
        print(f"{r['algorithm']}: {seq}")

    # Save to Markdown
    lines = ["# Experiment Results - Lecture 0 Search", ""]
    lines.append(f"Initial state: `{sorted(INITIAL_STATE)}`  ")
    lines.append(f"Objective: `fraction_word_problems`")
    lines.append("")
    lines.append("| Algorithm | States explored | Path cost | Optimal? | Sequence |")
    lines.append("|-----------|-----------------|-----------|----------|----------|")
    for r in rows:
        seq = " -> ".join(r["path"]) if r["path"] else "no solution"
        lines.append(f"| {r['algorithm']} | {r['explored']} | {r['cost']} | {r['optimal']} | {seq} |")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()