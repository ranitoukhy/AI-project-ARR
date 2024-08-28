import cProfile
import random
import os
import sys
import argparse
from datetime import datetime
from typing import List

from shared.structures import *
from shared.utils import milliseconds
from heapq import *

class KnapsackGeneticProblem:
    def __init__(self, filepath):
        self.num_items, self.max_weight, self.items = parse_input(filepath)


    def __len__(self):
        return len(self.items)

    def get_items_from_str(self, str):
        return [self.items[i] for i in range(len(str)) if str[i] == '1']

    def get_total_value_and_weight_from_str(self,sol_str):
        chosen_items = self.get_items_from_str(sol_str)
        total_val = 0
        total_weight = 0
        for item in chosen_items:
            total_val += item.value
            total_weight += item.weight
        return total_val, total_weight

    def print_from_str(self, sol_str):
        items = self.get_items_from_str(sol_str)
        items_str = "Chosen Items: "
        for i,item in enumerate(items):
            items_str += str(item)
            if i < len(items)-1:
                items_str += ", "
        total_val, total_weight = self.get_total_value_and_weight_from_str(sol_str)
        items_str += f"\nTotal Value: {total_val}\nTotal Weight: {total_weight}"

    def score_for_solution_str(self, sol_str):
        total_val, total_weight = self.get_total_value_and_weight_from_str(sol_str)
        return total_val if total_weight <= self.max_weight else 0.0



class GeneticAlgorithmAgent:

    def __init__(self,
                 problem,
                 population_size,
                 number_iterations,
                 elitism_fraction,
                 cross_prob,
                 mutation_prob,
                 inner_mutation_prob):

        random.seed(0)

        self.problem: KnapsackGeneticProblem = problem
        self.population_size = population_size & ~1
        self.number_iterations = number_iterations
        self.cross_prob = cross_prob
        self.inner_mutation_prob = inner_mutation_prob
        self.mutation_prob = mutation_prob
        self.elites_size = int(self.population_size * elitism_fraction) & ~1
        self.elites_heap = []
        self.population : List[KnapsackSolution] = self.generate_first_population()

    def generate_first_population(self):
        pop = set()
        while len(pop) < self.population_size:
            solution_str = ''.join(random.choice('0' * (self.problem.num_items - 1) + '1') for _ in range(self.problem.num_items))
            pop.add(solution_str)

        return [KnapsackSolution(solution_str, self.problem.score_for_solution_str(solution_str)) for solution_str in pop]

    def tournament(self) -> List[KnapsackSolution]:
        parents = []
        order = random.sample(range(self.population_size), self.population_size)
        for i in range(0, self.population_size, 2):
            parent1 = self.population[order[i]]
            parent2 = self.population[order[i+1]]
            if parent1.score > parent2.score:
                parents.append(parent1)
            else:
                parents.append(parent2)

        return parents

    def get_elites(self):
        self.population.sort(reverse=True)
        return [KnapsackSolution(pop.solution_str, pop.score) for pop in self.population[:self.elites_size]]

    def get_crossovers(self) -> List[KnapsackSolution]:
        def crossover(sol1: str, sol2: str):
            cutoff = len(sol1) // 2
            res1 = sol1[:cutoff] + sol2[cutoff:]
            res2 = sol2[:cutoff] + sol1[cutoff:]

            cross1 = KnapsackSolution(res1, self.problem.score_for_solution_str(res1))
            cross2 = KnapsackSolution(res1, self.problem.score_for_solution_str(res2))
            return [cross1, cross2]

        crossovers = []
        parents = self.tournament()

        num_crossovers = (self.population_size - self.elites_size) // 2
        for i in range(num_crossovers):
            indexes = random.sample(range(len(parents)), 2)
            parent1, parent2 = parents[indexes[0]], parents[indexes[1]]

            if random.random() < self.cross_prob:
                crossovers += crossover(parent1.solution_str, parent2.solution_str)
            else:
                crossovers += [parent1, parent2]

        return crossovers

    def mutate_solutions(self, solutions: List[KnapsackSolution]):
        def mutate(solution: KnapsackSolution):
            for i in range(len(solution.solution_str)):
                if random.random() < self.inner_mutation_prob:
                    # mutation = '1' if solution[i] == '0' else '0'
                    # if i == 0:
                    #     solution = mutation + solution[1:]
                    # elif i == len(solution)-1:
                    #     solution = solution[:-1] + mutation
                    # else:
                    #     solution = solution[:i] + mutation + solution[i+1:]
                    solution.solution_str = bin(int(solution.solution_str, 2) ^ 1 << i)[2:].zfill(self.problem.num_items)

            solution.score = self.problem.score_for_solution_str(solution.solution_str)
            return solution

        for i in range(len(solutions)):
            sol = solutions[i]
            if random.random() < self.mutation_prob or sol.score == 0:
                mutation_iter = 0
                mutated_sol = mutate(sol)
                while mutated_sol.score == 0 and mutation_iter < 100:
                    mutated_sol = mutate(mutated_sol)
                    mutation_iter += 1
                solutions[i] = mutated_sol

        return solutions


    def update_elites_heap(self, new_offspring):
        if len(self.elites_heap) < self.elites_size:
            heappush(self.elites_heap, new_offspring)

    def generate_next_populations(self):
        elites = self.get_elites()
        print(f"best elite, score = {elites[0].solution_str, elites[0].score}")
        crossovers = self.get_crossovers()
        mutations = self.mutate_solutions(crossovers)
        self.population = elites + mutations

    def run(self):
        for i in range(self.number_iterations):
            self.generate_next_populations()
            # print statistics

            max_sol = max(self.population)
            print(f"iteration {i}: solution value = {max_sol.score}")

        max_sol = max(self.population)

        return max_sol.score, self.problem.get_items_from_str(max_sol.solution_str)

def genetic_search(filepath):
    problem = KnapsackGeneticProblem(filepath)
    # if len(problem) >= 10:
    #     population_size = 125
    # elif len(problem) <= 4:
    #     population_size = 2 ** (len(problem) - 2)
    # else:
    #     population_size = 2 ** (len(problem) - 3)
    population_size = 1000
    agent = GeneticAlgorithmAgent(
        problem=problem,
        population_size=population_size,
        number_iterations=100,
        elitism_fraction=0.05,
        cross_prob=0.7,
        mutation_prob=0.5,
        inner_mutation_prob=1 / len(problem)
    )

    return agent.run()

def main(args):
    print("Starting a Genetic algorithm for finding a solution to the Knapsack problem.")
    print("")

    if args.time:
        t0 = datetime.now()
    max_value, solution = genetic_search(args.input)
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
    parser = argparse.ArgumentParser(description='Genetic algorithm for finiding a solution to the Knapsack problem')

    parser.add_argument('-i', '--input', required=True, help='Input Knapsack problem file path.')
    parser.add_argument('-t', '--time', action='store_true', help='Time of the run will be printed.')
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Path not found: {args.input}")
        sys.exit(-1)
    
    cProfile.run('main(args)')
    # sys.exit(main(args))
