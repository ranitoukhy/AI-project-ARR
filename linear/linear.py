import os
import sys
import argparse
from datetime import datetime
import scipy.optimize as opt
from shared.structures import KnapsackProblem
from shared.utils import milliseconds

def linear_programming(problem):
    values = [item.value for item in problem.items]
    weights = [item.weight for item in problem.items]
    
    c = [(-1) * value for value in values]
    integrality = [1] * problem.num_items
    bounds = opt.Bounds(0, 1)
    constraints = opt.LinearConstraint(weights, 0, problem.capacity)

    result = opt.milp(c, integrality=integrality, bounds=bounds, constraints=constraints)
    if not result.success:
        print(f"Linear programming solver failed with status %d", result.status)
        if result.status == 4:
            print(result.message)
        sys.exit(-1)
    
    max_value = (-1) * result.fun
    solution = set([problem.items[i] for i in range(problem.num_items) if result.x[i] == 1])

    return max_value, solution


def main(args):
    problem = KnapsackProblem(args.input)
    print("Starting a Linear programming solver for finding a solution to the Knapsack problem.")
    print("")
    print(f"Problem: {problem}")
    print("")

    if args.time:
        t0 = datetime.now()
    max_value, solution = linear_programming(problem)
    if args.time:
        t1 = datetime.now()
    
    print(f"Value found: {max_value}. Solution: {sorted(solution, key=lambda item: item.index)}")
    print("")

    if args.time:
        timediff_ms = milliseconds(t1-t0)
        print(f"Time: {timediff_ms:0.2f} milliseconds.")
        print("")
    
    return max_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A* search for finiding a solution to the Knapsack problem')

    parser.add_argument('-i', '--input', required=True, help='Input Knapsack problem file path.')
    parser.add_argument('-t', '--time', action='store_true', help='Time of the run will be printed.')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Path not found: {args.input}")
        sys.exit(-1)
    
    sys.exit(main(args))