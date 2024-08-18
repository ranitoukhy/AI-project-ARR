import os
import sys
import argparse
import time
import cProfile
from shared.structures import KnapsackProblem
from search import a_star_search

def main(args):
    problem = KnapsackProblem(args.input)
    print("Starting an A* search for finding a solution to the Knapsack problem.")
    print("")
    print(f"Problem: {problem}")
    print("")

    if args.time:
        t0 = time.time()
    max_value, solution = a_star_search(problem)
    if args.time:
        t1 = time.time()
    
    print(f"Value found: {max_value}. Solution: {sorted(solution, key=lambda item: item.index)}")
    print("")

    if args.time:
        print(f"Time: {t1-t0:0.4f} seconds.")
        print("")
    
    return max_value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A* search for finiding a solution to the Knapsack problem')

    parser.add_argument('-i', '--input', required=True, help='Input Knapsack problem file path.')
    parser.add_argument('-t', '--time', action='store_true', help='Time of the run will be printed.')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Path not found: {args.input}")
        sys.exit(1)
    
    # cProfile.run('main(args)')
    sys.exit(main(args))
