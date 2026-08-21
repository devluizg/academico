# Experiment Results - Lecture 0 Search (Linear Function)

## Student A: knows multiplication but not division

Initial state: `['basic_operations', 'multiplication_with_decimals']`

| Algorithm | States explored | Path cost | Optimal? | Sequence |
|-----------|-----------------|-----------|----------|----------|
| dfs | 12 | 965 | no | exponentiation -> square_root -> algebraic_language -> number_line -> cartesian_plane -> division -> linear_equations -> linear_function_concept -> linear_function_graph -> fractions -> linear_function_word_problems |
| bfs | 93 | 800 | yes | division -> fractions -> number_line -> cartesian_plane -> algebraic_language -> linear_equations -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |
| greedy | 10 | 800 | yes | division -> fractions -> number_line -> cartesian_plane -> algebraic_language -> linear_equations -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |
| astar | 90 | 800 | yes | number_line -> division -> algebraic_language -> cartesian_plane -> linear_equations -> linear_function_concept -> linear_function_graph -> fractions -> linear_function_word_problems |
| astar_tight | 29 | 800 | yes | division -> fractions -> number_line -> cartesian_plane -> algebraic_language -> linear_equations -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |

## Student B: knows equations but struggles with fractions

Initial state: `['algebraic_language', 'basic_operations', 'division', 'linear_equations', 'multiplication_with_decimals']`

| Algorithm | States explored | Path cost | Optimal? | Sequence |
|-----------|-----------------|-----------|----------|----------|
| dfs | 9 | 705 | no | exponentiation -> square_root -> number_line -> cartesian_plane -> linear_function_concept -> linear_function_graph -> fractions -> linear_function_word_problems |
| bfs | 39 | 540 | yes | fractions -> number_line -> cartesian_plane -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |
| greedy | 7 | 540 | yes | fractions -> number_line -> cartesian_plane -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |
| astar | 36 | 540 | yes | number_line -> cartesian_plane -> linear_function_concept -> linear_function_graph -> fractions -> linear_function_word_problems |
| astar_tight | 11 | 540 | yes | fractions -> number_line -> cartesian_plane -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |

## Student C: only basic operations (long path)

Initial state: `['basic_operations']`

| Algorithm | States explored | Path cost | Optimal? | Sequence |
|-----------|-----------------|-----------|----------|----------|
| dfs | 13 | 1045 | no | algebraic_language -> number_line -> cartesian_plane -> multiplication_with_decimals -> exponentiation -> square_root -> division -> linear_equations -> linear_function_concept -> linear_function_graph -> fractions -> linear_function_word_problems |
| bfs | 99 | 880 | yes | multiplication_with_decimals -> division -> fractions -> number_line -> cartesian_plane -> algebraic_language -> linear_equations -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |
| greedy | 11 | 880 | yes | multiplication_with_decimals -> division -> fractions -> number_line -> cartesian_plane -> algebraic_language -> linear_equations -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |
| astar | 96 | 880 | yes | number_line -> algebraic_language -> multiplication_with_decimals -> division -> cartesian_plane -> linear_equations -> linear_function_concept -> linear_function_graph -> fractions -> linear_function_word_problems |
| astar_tight | 35 | 880 | yes | multiplication_with_decimals -> division -> fractions -> number_line -> cartesian_plane -> algebraic_language -> linear_equations -> linear_function_concept -> linear_function_graph -> linear_function_word_problems |

