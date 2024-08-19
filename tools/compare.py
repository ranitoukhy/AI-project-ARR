import os
import sys
import argparse
from tabulate import tabulate
from datetime import datetime
from a_star.a_star import a_star_search
from brute_force.brute_force import brute_force
from shared.structures import KnapsackProblem

n_iters = 100
headers = ['Problem', 'Brute Force', 'A*'] #, 'Genetic']
err_margin = 0.0001

def milliseconds(timediff):
    return ((timediff.seconds * 1000000) + timediff.microseconds) / 1000.0

def main(args):
    results = []
    for filename in os.listdir(args.input):
        print(f"Processing {filename}...")
        problem = KnapsackProblem(os.path.join(args.input, filename))
        if args.optimal is not None:
            with open(os.path.join(args.optimal, filename), 'r') as f:
                optimal = float(f.readline())

        # Brute Force
        brute_force_time = 0.0
        for _ in range(n_iters):
            t0 = datetime.now()
            value, solution = brute_force(problem)
            t1 = datetime.now()
            brute_force_time += milliseconds(t1 - t0)
        brute_force_time /= n_iters

        if args.optimal is not None and abs(value - optimal) > err_margin:
            print(f"Brute force found sub-optimal solution {value}. Optimal is {optimal}.")
            sys.exit(1)
        
        # A*
        a_star_time = 0.0
        for _ in range(n_iters):
            t0 = datetime.now()
            value, solution = a_star_search(problem)
            t1 = datetime.now()
            a_star_time += milliseconds(t1 - t0)
        a_star_time /= n_iters

        if args.optimal is not None and abs(value - optimal) > err_margin:
            print(f"Brute force found sub-optimal solution {value}. Optimal is {optimal}.")
            sys.exit(1)
        
        # Genetic - TODO

        results.append([filename, brute_force_time, a_star_time])
    print("")
    print(tabulate(results, headers=headers))

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Tool to compare performance of genetic algorithm, A* search, and brute force solutions of the Knapsack problem.'
    )

    parser.add_argument('-i', '--input', required=True, help='Input directory of problem cases.')
    parser.add_argument('-o', '--optimal', help='Optional directory for optimal solutions of the problem cases.')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Path not found: {args.input}")
        sys.exit(1)
    
    if not os.path.isdir(args.input):
        print(f"Path is not a directory: {args.input}")
        sys.exit(1)
    
    sys.exit(main(args))
