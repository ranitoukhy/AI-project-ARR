# 0/1 Knapsack Problem using AI

In this project we have two AI implementations for solving the 0/1 Knapsack Problem, which is an NP-hard problem:<br>

* <b>The A* Search algorithm</b> provides an optimal solution, with a small runtime for non-edge-case problems.<br>
* <b>The Genetic algorithm</b> provides an approximated solution, with the trade-off between runtime and optimality being controllable through the choice of hyperparameters.<br>

## Requirements

Requirements for this project are the `scipy` package for running `linear_programming.py`, and the `tabulate` package for running `compare.py`.

## Code structure

Directories in this project include:<br>

* `a_star`: The A* Search algorithm.<br>
* `genetic`: The Genetic algorithm.<br>
* `reference_algorithms`: Three commonly-used algorithms for solving the 0/1 Knapsack problem: Linear Programming, Dynamic Programming, and Brute-force.<br>
* `input`: Sample Knapsack problems to provide the algorithms with, as well as the optimal value for each problem, to test the optimality of the algorithms.<br>
* `shared`: Some structures and utilities shared between files.<br>

In addition, we have the `compare.py` script for comparing all five algorithms on an input set of 0/1 Knapsack problems. See [Running the comparison](#running-the-comparison).<br>

## Running individual algorithms

Each algorithm accepts two parameters:<br>

* `-i` accepts a path to an input Knapsack problem (you can see examples in the "input" directory).<br>
* `-t` (optional), when set, will print out execution time of the script.<br>

Example:<br>

```
python3 a_star/a_star.py -i input/low-dimensional/f1_l-d_kp_10_269 -t
```

## Running the comparison

`compare.py` accepts two parameters:<br>

* `-i` accepts a path to a directory with 0/1 Knapsack problems.<br>
* `-o` accepts a path to the optimal solutions of the problems given with `-i`.<br>

Example:<br>

```
python3 compare.py -i input/low-dimensional -o input/low-dimensional-optimum
```

> Note: running with `-i input/large-scale` will take forever, as the brute-force algorithm is exponentially slow. You can comment it out in the script for these. That is also true for the low-dimensional problem `f8_l-d_kp_23_10000` - you can edit the script to skip that one. In general, you can change the `n_iter` parameter for averaging the results on less iterations.<br>
