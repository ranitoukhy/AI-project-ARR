import os
import sys
import argparse
from datetime import datetime
from shared.structures import KnapsackProblem
from shared.utils import milliseconds

class Solution:
    def __init__(self, items):
        self.items = items
        self.value = sum([item.value for item in items])

def dynamic_programming(problem):
    """
    Creates a Dynamic programming table for solving the Knapsack problem.
    The solution in cell [i][j] is the solution to the Knapsack problem of capacity j using items 1...i only.
    """
    solutions = [[None for _ in range(int(problem.capacity)+1)] for _ in range(problem.num_items+1)]
    for i in range(problem.num_items+1):
        solutions[i][0] = Solution(list())
    for j in range(int(problem.capacity)+1):
        solutions[0][j] = Solution(list())
    
    for i in range(1, problem.num_items+1):
        for j in range(1, int(problem.capacity)+1):
            without_i = solutions[i-1][j]
            with_i = Solution(list())
            if j >= problem.items[i-1].weight:
                with_i = Solution(solutions[i-1][j - int(problem.items[i-1].weight)].items + [problem.items[i-1]])
            solutions[i][j] = with_i if with_i.value > without_i.value else without_i
    
    return solutions[-1][-1].value, set(solutions[-1][-1].items)

def main(args):
    problem = KnapsackProblem(args.input)
    print("Starting a dynamic program for finding the optimal solution to the Knapsack problem.")
    print("")
    print(f"Problem: {problem}")
    print("")

    if args.time:
        t0 = datetime.now()
    max_value, solution = dynamic_programming(problem)
    if args.time:
        t1 = datetime.now()

    print(f"Value found: {max_value}. Solution: {sorted(solution, key=lambda item: item.index)}")
    print("")

    if args.time:
        timediff_ms = milliseconds(t1-t0)
        print(f"Time: {t1-t0:0.4f} seconds.")
        print("")

    return max_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dynamic programming for finiding a solution to the Knapsack problem')

    parser.add_argument('-i', '--input', required=True, help='Input Knapsack problem file path.')
    parser.add_argument('-t', '--time', action='store_true', help='Time of the run will be printed.')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Path not found: {args.input}")
        sys.exit(-1)

    sys.exit(main(args))
