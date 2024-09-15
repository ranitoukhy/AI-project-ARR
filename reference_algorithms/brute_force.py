import os
import sys
import argparse
from datetime import datetime
from itertools import combinations
from shared.structures import KnapsackProblem
from shared.utils import milliseconds

def brute_force(problem):
    """
    Iterates over all possible combinations of items to find the one with the highest value which satisfies the capacity constraint.
    :param problem: A KnapsackProblem object
    :return: The value of the solution found, and the solution itself.
    """
    solution = set()
    max_value = 0
    
    # Check all possible combinations of items
    for r in range(1, problem.num_items+1):
        for combination in combinations(problem.items, r):
            total_weight = sum(item.weight for item in combination)
            total_value = sum(item.value for item in combination)
            
            if total_weight <= problem.capacity and total_value > max_value:
                max_value = total_value
                solution = set(combination)
    
    return max_value, solution

def main(args):
    problem = KnapsackProblem(args.input)
    print("Starting a brute force search for finding the optimal solution to the Knapsack problem.")
    print("")
    print(f"Problem: {problem}")
    print("")

    if args.time:
        t0 = datetime.now()
    max_value, solution = brute_force(problem)
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
    parser = argparse.ArgumentParser(description='Brute force approach for finiding a solution to the Knapsack problem')

    parser.add_argument('-i', '--input', required=True, help='Input Knapsack problem file path.')
    parser.add_argument('-t', '--time', action='store_true', help='Time of the run will be printed.')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Path not found: {args.input}")
        sys.exit(-1)
    
    sys.exit(main(args))
