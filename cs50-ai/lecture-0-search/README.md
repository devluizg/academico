# Lecture 0 - Search: EduPath (Learning Path Planner)

An AI agent that uses **search algorithms** to find the optimal sequence of
study topics that takes a student from their current knowledge (initial state)
to a learning goal (goal state), over a concept map with prerequisites
defined by a teacher.

## Mapping lecture concepts to this project

| Lecture 0 concept      | In this project                                            |
|------------------------|------------------------------------------------------------|
| Agent                  | The learning-path planner                                  |
| State                  | The set of concepts the student has mastered               |
| Initial state          | The student's prior knowledge (`INITIAL_STATE`)            |
| Actions `actions(S)`   | Concepts whose prerequisites are all mastered in `S`       |
| Transition model       | `result(S, a) = S ∪ {a}`                                   |
| Goal test              | Objective concept is in the mastered set                   |
| Path cost              | Sum of `time + difficulty × 10` per studied concept        |
| Frontier + explored set| Avoid revisiting states / infinite loops                   |
| DFS                    | `StackFrontier` (last in, first out)                       |
| BFS                    | `QueueFrontier` (first in, first out)                      |
| Greedy Best-First      | `PriorityFrontier` ordered by `h(n)`                       |
| A* Search              | `PriorityFrontier` ordered by `g(n) + h(n)`                |

## Why the heuristic is admissible

`h(state) = (number of missing required concepts) × (cheapest concept cost)`

It **never overestimates**: to reach the objective the student must still
master every missing required concept, and each one costs at least the
cheapest concept cost. Therefore the true remaining cost is always `≥ h(n)`,
which makes A* guaranteed to find the optimal solution.

## How to run

```bash
cd cs50-ai/lecture-0-search
python3 run_experiments.py
```

## Scope note

This folder covers **Lecture 0 (Search) only**. Inferring the student's
knowledge from answers (Knowledge) or estimating mastery probabilities
(Uncertainty) belong to future lectures.