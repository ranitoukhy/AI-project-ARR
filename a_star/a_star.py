import os
import sys
import argparse
from datetime import datetime
from shared.structures import KnapsackProblem
from a_star.search import PriorityQueue, priority_func
from shared.utils import milliseconds

def a_star_search(problem):
    """
    Runs the A* search algorithm on a KnapsackProblem object.
    The algorithm manages a PriorityQueue of KnapsackStates to run an informed BFS based on a priority function per state.
    :param problem: A KnapsackProblem object
    :return: The value of the solution found, and the solution itself.
    """
    fringe = PriorityQueue(priority_func)
    fringe.push(problem.get_start_state())
    while not fringe.isEmpty():
        state = fringe.pop()
        if problem.is_goal_state(state):
            return state.value, state.items_taken
        for successor in problem.get_successors(state):
            fringe.push(successor)

def main(args):
    problem = KnapsackProblem(args.input)
    print("Starting an A* search for finding a solution to the Knapsack problem.")
    print("")
    print(f"Problem: {problem}")
    print("")

    if args.time:
        t0 = datetime.now()
    max_value, solution = a_star_search(problem)
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
