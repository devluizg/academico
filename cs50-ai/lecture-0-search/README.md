# Lecture 0 - Search: EduPath (Learning Path Planner)

> A portfolio project for **CS50's Introduction to Artificial Intelligence
> with Python — Lecture 0: Search**.
>
> This README is written as a **concept-to-code map**: every idea from the
> lecture is linked to the exact piece of code that implements it, so anyone
> reading the source can understand *what each part does and why*.

---

## 1. The Educational Problem

In Brazilian high schools, students are expected to learn **linear
functions** (*função do 1º grau*) in their first year. However, most of them
arrive missing foundational skills from previous years: decimal
multiplication, division, and equation solving. A single classroom contains
students at **radically different starting points**.

A fixed curriculum fails everyone — advanced students get bored, while
struggling students fall further behind. The real bottleneck is not the new
content itself, but the **missing prerequisites**.

EduPath models what an experienced teacher does intuitively: diagnose where
each student stands, then design a **personalized learning path**. Two
students aiming for the same goal may follow completely different sequences.
Search algorithms let us find the optimal path for each starting point.

---

## 2. The Five Building Blocks of a Search Problem

The lecture (13:41) defines a search problem with five components. Here is
how each one appears in this project:

| Lecture concept (timestamp) | Educational meaning | Code location |
|---|---|---|
| **Initial state** | What the student already knows | `INITIAL_STATE` in `run_experiments.py` |
| **Actions** `actions(S)` (06:37) | Concepts the student can study next | `LearningProblem.actions()` |
| **Transition model** `result(S, A)` (07:51) | "After studying X, I now know X" | `LearningProblem.result()` |
| **Goal test** (11:00) | "Have I mastered the objective?" | `LearningProblem.goal_test()` |
| **Path cost** (12:02) | Total time/effort spent studying | `LearningProblem.concept_cost()` |

---

## 3. Concept-to-Code Map

This is the core of the README. Each subsection shows a lecture idea, the
exact code that implements it, and a plain-English explanation.

### 3.1 The `Node` — the smallest unit of the search

**Lecture (15:06):**
> *"A node is a data structure that keeps track of a state, a parent, an
> action, and a path cost."*

**Code (`edupath.py`):**
```python
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
```

**What each attribute means:**

| Attribute | What it stores | Why it exists |
|---|---|---|
| `state` | The set of concepts mastered so far | A "snapshot" of where the student is |
| `parent` | The previous `Node` that created this one | To **reconstruct the path** at the end (15:47) |
| `action` | Which concept was studied to get here | To know the sequence of actions |
| `path_cost` | Accumulated cost from the start | So A* can compare different paths |

> **Why `parent` matters:** When we reach the goal, we follow the `parent`
> pointers backwards to recover the entire study sequence — like following a
> trail of breadcrumbs back to the start.

---

### 3.2 The Frontiers — where the algorithms actually differ

**Lecture (25:46):**
> *"It turns out it's actually quite important how we decide to structure our
> frontier... in what order are we going to be removing elements?"*

**This is the single most important idea of the lecture:** DFS, BFS, Greedy
and A* all use the *same* search loop. The **only** difference is *which node
gets removed from the frontier next*.

#### StackFrontier → generates DFS

**Lecture (26:03):** *"A stack is a last in, first out data type."*

```python
class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        node = self.frontier[-1]          # take the LAST item
        self.frontier = self.frontier[:-1]
        return node
```

`frontier[-1]` grabs the **last** element added. This makes the algorithm
always dive into the most recently discovered node → **Depth-First Search**.

#### QueueFrontier → generates BFS

**Lecture (29:06):** *"A queue is a first in, first out data type."*

```python
class QueueFrontier(StackFrontier):
    def remove(self):
        node = self.frontier[0]           # take the FIRST item
        self.frontier = self.frontier[1:]
        return node
```

`frontier[0]` grabs the **first** element added. Nodes are explored in the
order they were discovered → **Breadth-First Search**.

#### PriorityFrontier → generates Greedy and A*

```python
class PriorityFrontier:
    def add(self, node, priority):
        heapq.heappush(self.frontier, (priority, self._counter, node))

    def remove(self):
        _, _, node = heapq.heappop(self.frontier)   # take LOWEST priority
        return node
```

Always removes the node with the **lowest priority value**. What that value
is depends on the algorithm:
- **Greedy:** priority = `h(n)` (heuristic only)
- **A\*:** priority = `g(n) + h(n)` (cost so far + heuristic)

---

### 3.3 The `LearningProblem` — encoding the five building blocks

#### `actions(state)` — what can be studied next

**Lecture (06:37):** *"actions of S returns the set of all actions that can
be executed in that state."*

```python
def actions(self, state):
    available = []
    for concept, info in self.concepts.items():
        if concept in state:
            continue
        if all(p in state for p in info["prerequisites"]):
            available.append(concept)
    return available
```

A concept can only be studied if **all its prerequisites are already
mastered** (`all(p in state ...)`). This is exactly how a teacher reasons:
you don't teach functions before the student understands equations.

#### `result(state, action)` — the transition model

**Lecture (07:51):** *"result gives us the state we get after we perform
action A in state S."*

```python
def result(self, state, action):
    return state | {action}
```

`state | {action}` is a **set union**: the new state is the old one plus the
newly studied concept. If I knew `{A, B}` and studied `C`, I now know
`{A, B, C}`.

#### `goal_test(state)` — have we arrived?

**Lecture (11:08):** *"some way to determine whether a given state is a goal
state."*

```python
def goal_test(self, state):
    return self.objective in state
```

Simply asks: *"Is the objective concept in the mastered set?"*

#### `heuristic(state)` — the informed estimate ⭐

**Lecture (55:22):** *"a heuristic function h(n) that takes a state and
returns our estimate of how close we are to the goal."*

```python
def heuristic(self, state):
    missing = self.required - set(state)
    return len(missing) * self.min_cost
```

Counts how many **required** concepts are still missing, then multiplies by
the cheapest concept cost. It is an **optimistic** (low) estimate.

---

### 3.4 The `solve()` loop — the engine shared by all algorithms

**Lecture pseudocode (17:27).** Every step below maps to one line of the
lecture's pseudocode:

```python
while True:
    if frontier.empty():                    # 1. empty frontier → no solution
        return None, num_explored, None

    node = frontier.remove()                # 2. remove a node
    num_explored += 1

    if problem.goal_test(node.state):       # 3. is it the goal?
        # ... backtrack through parents to rebuild the path ...
        return actions, num_explored, total_cost

    explored.add(node.state)                # 4. mark as explored (avoid loops)

    for action in problem.actions(node.state):     # 5. expand the node
        child_state = problem.result(node.state, action)
        if child_state in explored or frontier.contains_state(child_state):
            continue                        # don't revisit
        frontier.add(child, ...)            # add new node to frontier
```

The `explored` set is the fix for the **infinite loop problem** the lecture
shows at 22:14 (going A → B → A → B forever). Once a state is explored, we
never go back to it (24:07).

---

## 4. A Quick Note on Object-Oriented Programming (OOP)

If you are new to OOP, here is how to read the code:

| OOP term | Plain meaning | Example in this project |
|---|---|---|
| **Class** | A blueprint / recipe | `class Node:` |
| **Object / instance** | A concrete thing made from the blueprint | `start = Node(initial_state)` |
| **Attribute** | A piece of data the object stores | `self.state`, `self.parent` |
| **Method** | A function that belongs to the class | `def add(self, node):` |
| **`self`** | Refers to "this specific object" | `self.frontier.append(node)` |
| **Inheritance** | A class reuses another class's code | `class QueueFrontier(StackFrontier):` |

Notice `QueueFrontier(StackFrontier)`: the queue **inherits** everything from
the stack (the list, `add`, `empty`, `contains_state`) and only **overrides**
the `remove()` method. That single changed method is what turns DFS into BFS.

---

## 5. Why the Heuristic Is Admissible

**Lecture (01:09:37):** *"a heuristic is admissible if it never overestimates
the true cost."*

Our heuristic is `h(state) = (missing required concepts) × (cheapest cost)`.

It **never overestimates** because:
1. To reach the objective, the student **must** master every missing required
   concept.
2. Each of them costs **at least** `min_cost`.
3. Therefore the true remaining cost is always `≥ h(n)`.

Because the heuristic is admissible, **A\* is guaranteed to find the optimal
solution** (01:09:25).

We also added a **tighter** admissible heuristic, `heuristic_tight`, which
sums the *actual* costs of the missing required concepts. It is still
admissible, but much closer to the true cost — and the experiments below show
how dramatically this reduces the number of states A* must explore.

---

## 6. Results & Discussion

Each scenario was run with five algorithms: DFS, BFS, Greedy, A* (weak
heuristic) and A* (tight heuristic).

### Scenario A — knows multiplication, but not division

| Algorithm | States explored | Path cost | Optimal? |
|---|---|---|---|
| dfs | 12 | 965 | ❌ no |
| bfs | 93 | 800 | ✅ yes |
| greedy | 10 | 800 | ✅ yes |
| astar | 90 | 800 | ✅ yes |
| **astar_tight** | **29** | **800** | ✅ yes |

### Scenario B — knows equations, but struggles with fractions

| Algorithm | States explored | Path cost | Optimal? |
|---|---|---|---|
| dfs | 9 | 705 | ❌ no |
| bfs | 39 | 540 | ✅ yes |
| greedy | 7 | 540 | ✅ yes |
| astar | 36 | 540 | ✅ yes |
| **astar_tight** | **11** | **540** | ✅ yes |

### Scenario C — only basic operations (long path)

| Algorithm | States explored | Path cost | Optimal? |
|---|---|---|---|
| dfs | 13 | 1045 | ❌ no |
| bfs | 99 | 880 | ✅ yes |
| greedy | 11 | 880 | ✅ yes |
| astar | 96 | 880 | ✅ yes |
| **astar_tight** | **35** | **880** | ✅ yes |

### Key findings

**1. DFS wasted effort on "decoy" concepts.**
In every scenario DFS studied `exponentiation` and `square_root` — concepts
that do **not** lead to the objective. That is exactly 165 wasted cost points
(`965 = 800 + 85 + 80`). This illustrates the lecture's warning (28:00):
*"DFS just picked one path and kept following it until it hit a dead end."*
Translated to education: without diagnosis and planning, a student spends
energy on content that does not bring them closer to the goal.

**2. BFS is optimal but explores a lot.**
BFS found the optimal path in every case, but explored far more states than
the informed algorithms. It is systematic, and that has a price.

**3. Greedy was efficient here, but is not guaranteed.**
Greedy explored very few states because the heuristic guided it straight to
the required concepts. However, the lecture (01:02:00) shows a case where
Greedy finds a *non-optimal* path. In this domain it got lucky; in another
concept map it could fail.

**4. A better heuristic makes A* dramatically more efficient.**
Switching from the weak heuristic to the tight heuristic cut the states
explored by roughly **two-thirds** (e.g. 96 → 35 in Scenario C), while keeping
the same optimal cost. This is a direct experimental confirmation of the
lecture (01:11:13): *"The better the heuristic, the fewer states that I'll
have to explore."*

---

## 7. How to Run

```bash
cd cs50-ai/lecture-0-search
python3 run_experiments.py
```

Results are printed to the console and saved to `output/results.md`.

---

## 8. Scope Note

This folder covers **Lecture 0 (Search) only**. Inferring the student's
knowledge from answers (**Knowledge**) or estimating mastery probabilities
(**Uncertainty**) belong to future lectures.