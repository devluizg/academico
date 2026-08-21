# Experiment Results - Lecture 0 Search

Initial state: `['natural_numbers']`  
Objective: `fraction_word_problems`

| Algorithm | States explored | Path cost | Optimal? | Sequence |
|-----------|-----------------|-----------|----------|----------|
| dfs | 10 | 645 | no | divisibility -> fraction_concept -> multiplying_fractions -> dividing_fractions -> equivalent_fractions -> comparing_fractions -> gcd_lcm -> adding_fractions -> fraction_word_problems |
| bfs | 33 | 580 | yes | divisibility -> gcd_lcm -> fraction_concept -> equivalent_fractions -> adding_fractions -> multiplying_fractions -> dividing_fractions -> fraction_word_problems |
| greedy | 9 | 580 | yes | divisibility -> gcd_lcm -> fraction_concept -> equivalent_fractions -> adding_fractions -> multiplying_fractions -> dividing_fractions -> fraction_word_problems |
| astar | 31 | 580 | yes | divisibility -> fraction_concept -> equivalent_fractions -> multiplying_fractions -> dividing_fractions -> gcd_lcm -> adding_fractions -> fraction_word_problems |
