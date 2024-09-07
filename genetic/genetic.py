import random
import os
import sys
import argparse
from datetime import datetime
from typing import List

from shared.structures import *
from shared.utils import milliseconds

class KnapsackGeneticProblem:
    """
    This class represents the 1-0 knapsack problem with utility functions for
    the genetic algorithm agent
    """
    def __init__(self, filepath):
        self.num_items, self.max_weight, self.items = parse_input(filepath)
        self.items_sorted_by_vpw = sorted(list(range(len(self.items))), key=lambda i: self.items[i].value / self.items[i].weight, reverse=True)

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
    """
    A genetic-algorithm agent that, given pre-defined parameters, returns a
    solution for the 0-1 Knapsack Problem create by mutating and crossing over
    solutions throughout multiple generations
    """

    def __init__(self,
                 problem,
                 population_size_factor=2,
                 number_iterations_factor=1,
                 elitism_fraction=0.35,
                 cross_prob=0.7,
                 mutation_prob=1,
                 inner_mutation_prob=0.05,
                 expected_items_mutated=1):
        """
        :param problem: A KnapsackGeneticProblem instance
        :param population_size_factor: The population size will be population_size_factor * len(problem)
        :param number_iterations_factor: The number of iterations will be number_iterations_factor * len(problem)
        :param elitism_fraction: The fraction of the generation that should be passed as elites
        :param cross_prob: The probability of crossing over two parents during the crossover phase
        :param mutation_prob: The probability of mutating a chromosome during the mutation phase
        :param inner_mutation_prob: The probability of switching a single item when mutating a chromosome
        :param expected_items_mutated: Alternative way for setting inner mutation probability.
                        Inner mutation probability will be expected_items_mutated/len(problem)
        """
        self.problem: KnapsackGeneticProblem = problem
        self.population_size = population_size_factor*len(problem)
        self.number_iterations = number_iterations_factor*len(problem)
        self.cross_prob = cross_prob
        self.mutation_prob = mutation_prob
        self.inner_mutation_prob = inner_mutation_prob \
            if expected_items_mutated <= 0 \
            else expected_items_mutated / len(problem)
        self.elites_size = int(self.population_size * elitism_fraction) & ~1
        self.population: List[KnapsackSolution] = self.generate_first_population()

    def generate_first_population(self):
        """
        Generates the first population for the genetic algorithm.
        The population consists of solutions that are constructed of a single item in the knapsack
        :return: A list of KnapsackSolution items representing the first population
        """
        pop = ['0'*(i%self.problem.num_items)+'1'+'0'*(self.problem.num_items-(i%self.problem.num_items)-1) for i in range(self.population_size)]
        return [KnapsackSolution(solution_str, self.problem.score_for_solution_str(solution_str)) for solution_str in pop]

    def get_parents_for_crossover(self) -> List[KnapsackSolution]:
        """
        Creates a list of parents to pass on the crossover phase.
        The parents are the top (population_size - elite_size) chromosomes in the current population
        :return: A list of KnapsackSolution "parents"
        """
        sum_values = sum([chrome.score for chrome in self.population])
        fitness_values = [chrome.score / sum_values for chrome in self.population]
        parents = random.choices(self.population, weights=fitness_values, k=self.population_size - self.elites_size)

        return parents

    def get_elites(self):
        """
        :return: The top elite_size chromosomes of the current population
        """
        self.population.sort(reverse=True)
        return [KnapsackSolution(pop.solution_str, pop.score) for pop in self.population[:self.elites_size]]

    def get_crossovers(self) -> List[KnapsackSolution]:
        """
        Creates chromosomes for the non-elite segment of the next population
        The process consists of:
            1. Selecting the top (population_size - elite_size)/2 chromosomes of the current population as "parents"
            2. Taking pairs of parents and either creating crossovers from them or
                passing them directly to the next population
        :return: A list of (population_size - elite_size) KnapsackSolutions
        """
        def crossover(sol1: str, sol2: str):
            """
            Crosses over two KnapsackSolution items by creating two new KnapsackSolutions that
            consist of the first half of one of the inputted solutions and the second half of the
            second inputted solution
            :return: Two KnapsackSolution "crossover-ed" objects
            """
            cutoff = len(sol1) // 2
            res1 = sol1[:cutoff] + sol2[cutoff:]
            res2 = sol2[:cutoff] + sol1[cutoff:]

            cross1 = KnapsackSolution(res1, self.problem.score_for_solution_str(res1))
            cross2 = KnapsackSolution(res2, self.problem.score_for_solution_str(res2))
            return [cross1, cross2]

        crossovers = []
        parents = self.get_parents_for_crossover()

        for i in range(len(parents)//2):
            parent1, parent2 = parents[2*i], parents[2*i+1]

            if random.random() < self.cross_prob:
                crossovers += crossover(parent1.solution_str, parent2.solution_str)
            else:
                crossovers += [parent1, parent2]

        return crossovers

    def mutate_solutions(self, solutions: List[KnapsackSolution]):
        """
        Bit-flips a list of solutions, with probability self.inner_mutation_prob for each bit.
        :param solutions: A list of KnapsackSolutions to mutate
        :return: A list of mutated KnapsackSolutions
        """
        def mutate(solution: KnapsackSolution):
            """
            Mutates a given solution by iterating over all items in the KnapsackProblem and with a probability of
            inner_mutation_prob flip the decision made regarding said item in the solution
            (take the item if not taken, remove the item if taken)
            :param solution: A KnapsackSolution to mutate
            :return: The mutation of the given solution
            """
            sol_str = solution.solution_str
            for i in range(len(sol_str)):
                if random.random() < self.inner_mutation_prob:
                    solution.solution_str = bin(int(solution.solution_str, 2) ^ 1 << i)[2:].zfill(self.problem.num_items)

            solution.score = self.problem.score_for_solution_str(solution.solution_str)
            return solution

        for i in range(len(solutions)):
            sol = solutions[i]

            mutation_iter = 0
            mutated_sol = mutate(sol)
            while (sol.score != 0 and mutated_sol.score == 0) and mutation_iter < 100:
                mutated_sol = mutate(mutated_sol)
                mutation_iter += 1
            solutions[i] = mutated_sol

        return solutions

    def generate_next_populations(self):
        """
        Generates the next genetic-algorithm population.
        The generation executed using following steps:
            1. Get the top elite_size chromosomes of the current population
            2. Create (population_size - elite_size) KnapsackSolutions by either crossing
                over solutions from the current population or passing them on directly
            3. Mutate the non-elite solution from step 2 with a certain probability
            4. Set new population to be elites + mutated non-elites
        :return:
        """
        elites = self.get_elites()
        crossovers = self.get_crossovers()
        mutations = self.mutate_solutions(crossovers)
        self.population = elites + mutations

    def run(self):
        """
        Runs the Genetic algorithm agent on the problem it was initialized with.
        :return: The value of the solution found, and the solution itself.
        """
        for i in range(self.number_iterations):
            self.generate_next_populations()

        max_sol = max(self.population)

        return max_sol.score, self.problem.get_items_from_str(max_sol.solution_str)

def genetic_search(filepath):
    """
    Runs the Genetic algorithm on a problem to find a good solution to the Knapsack problem.
    :param filepath: A path to a Knapsack problem with the format specified in structures.parse_input
    :return: The value of the solution found, and the solution itself.
    """
    problem = KnapsackGeneticProblem(filepath)
    agent = GeneticAlgorithmAgent(
        problem=problem,
        population_size_factor=2,
        number_iterations_factor=1,
        elitism_fraction=0.35,
        cross_prob=0.7,
        mutation_prob=1,
        inner_mutation_prob=0,
        expected_items_mutated=1
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

    sys.exit(main(args))
