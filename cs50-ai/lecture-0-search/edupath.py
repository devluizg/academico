"""
EduPath - Learning Path Planner
CS50 AI - Lecture 0: Search

An AI agent that uses search algorithms to find the optimal sequence of
study topics taking a student from their current knowledge (initial state)
to a learning goal (goal state), over a concept map with prerequisites
defined by a teacher.
"""

import heapq
import json


class Node:
    """A node in the search tree. Keeps track of the four values described
    in Lecture 0: the current state, the parent node that generated it,
    the action taken to get here, and the path cost so far."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


class StackFrontier:
    """Frontier as a stack (last in, first out) -> Depth-First Search."""

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node


class QueueFrontier(StackFrontier):
    """Frontier as a queue (first in, first out) -> Breadth-First Search."""

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node


class PriorityFrontier:
    """Frontier as a priority queue (lowest f removed first).
    Used by Greedy Best-First Search (f = h) and A* Search (f = g + h)."""

    def __init__(self):
        self.frontier = []
        self._counter = 0  # tie-breaker so heapq never compares Nodes

    def add(self, node, priority):
        heapq.heappush(self.frontier, (priority, self._counter, node))
        self._counter += 1

    def contains_state(self, state):
        return any(node.state == state for _, _, node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        _, _, node = heapq.heappop(self.frontier)
        return node


class LearningProblem:
    """Encodes the search problem: states, actions, transition model,
    goal test and path cost. Loaded from a teacher-defined concept map."""

    DIFFICULTY_WEIGHT = 10  # how much each difficulty point adds to cost

    def __init__(self, map_path, initial_state, objective=None):
        with open(map_path) as f:
            data = json.load(f)

        self.concepts = data["concepts"]
        self.objective = objective or data["objective"]
        self.initial_state = frozenset(initial_state)

        # Concepts required to reach the objective (objective + all its
        # transitive prerequisites). Used by the heuristic.
        self.required = self._transitive_prerequisites(self.objective)

        # Cheapest concept cost, used to build an admissible heuristic.
        self.min_cost = min(self.concept_cost(c) for c in self.concepts)

    def concept_cost(self, concept):
        """Cost of studying one concept: time + weighted difficulty."""
        info = self.concepts[concept]
        return info["time"] + info["difficulty"] * self.DIFFICULTY_WEIGHT

    def _transitive_prerequisites(self, concept):
        """Return the concept plus everything it transitively depends on."""
        required = {concept}
        stack = [concept]
        while stack:
            current = stack.pop()
            for prereq in self.concepts[current]["prerequisites"]:
                if prereq not in required:
                    required.add(prereq)
                    stack.append(prereq)
        return required

    def actions(self, state):
        """Concepts the student may study next: those whose prerequisites
        are all already mastered in `state`."""
        available = []
        for concept, info in self.concepts.items():
            if concept in state:
                continue
            if all(p in state for p in info["prerequisites"]):
                available.append(concept)
        return available

    def result(self, state, action):
        """Transition model: studying `action` adds it to the mastered set."""
        return state | {action}

    def goal_test(self, state):
        """Goal reached when the objective concept is mastered."""
        return self.objective in state

    def step_cost(self, state, action):
        """Cost of the action of studying `action`."""
        return self.concept_cost(action)

    def heuristic(self, state):
        """Admissible and consistent heuristic: an optimistic estimate of
        the remaining cost. Count how many required concepts are still
        missing and assume each costs the cheapest possible value.

        Why it never overestimates: the student must still master every
        missing required concept, and each of them costs at least min_cost,
        so the true remaining cost is always >= this estimate.
        """
        missing = self.required - set(state)
        return len(missing) * self.min_cost

    def heuristic_tight(self, state):
        """A tighter admissible heuristic: the sum of the actual costs of
        the required concepts still missing. Still never overestimates,
        because the student must pay at least this much to reach the goal."""
        missing = self.required - set(state)
        return sum(self.concept_cost(c) for c in missing)


def solve(problem, algorithm):
    """Solve the problem with the chosen algorithm.

    Returns (solution path, states explored, total cost), or
    (None, states explored, None) when there is no solution.
    """
    start = Node(problem.initial_state)

    if algorithm in ("dfs", "bfs"):
        frontier = StackFrontier() if algorithm == "dfs" else QueueFrontier()
        use_priority = False
    elif algorithm in ("greedy", "astar", "astar_tight"):
        frontier = PriorityFrontier()
        use_priority = True
    else:
        raise ValueError(f"unknown algorithm: {algorithm}")

    def priority_of(node):
        if algorithm == "astar_tight":
            h = problem.heuristic_tight(node.state)
        else:
            h = problem.heuristic(node.state)
        if algorithm == "greedy":
            return h                # Greedy Best-First: f(n) = h(n)
        return node.path_cost + h   # A*: f(n) = g(n) + h(n)

    if use_priority:
        frontier.add(start, priority_of(start))
    else:
        frontier.add(start)

    explored = set()
    num_explored = 0

    while True:
        if frontier.empty():
            return None, num_explored, None

        node = frontier.remove()
        num_explored += 1

        if problem.goal_test(node.state):
            total_cost = node.path_cost
            actions = []
            while node.parent is not None:
                actions.append(node.action)
                node = node.parent
            actions.reverse()
            return actions, num_explored, total_cost

        explored.add(node.state)

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            if child_state in explored or frontier.contains_state(child_state):
                continue
            child_cost = node.path_cost + problem.step_cost(node.state, action)
            child = Node(child_state, node, action, child_cost)
            if use_priority:
                frontier.add(child, priority_of(child))
            else:
                frontier.add(child)