import random
from typing import *
from shared.structures import *

class KnapsackGeneticProblem:
    def __init__(self, filepath):
        self.items, self.num_items, self.max_weight = parse_input(filepath)

    def __len__(self):
        return len(self.items)

    def get_items_from_str(self, str):
        items = []
        for i in range(len(str)):
            if str[i] == '1':
                items.append(self.items[i])
        return items

    def get_total_value_and_weight_from_str(self,str):
        chosen_items = self.get_items_from_str(str)
        total_val = 0
        total_weight = 0
        for item in chosen_items:
            total_val += item.value
            total_weight += item.weight
        return total_val, total_weight

    def print_from_str(self, str):
        items = self.get_items_from_str(str)
        items_str = "Chosen Items: "
        for i,item in enumerate(items):
            items_str += str(item)
            if i < len(items)-1:
                items_str += ", "
        total_val, total_weight = self.get_total_value_and_weight_from_str(str)
        items_str += f"\nTotal Value: {total_val}\nTotal Weight: {total_weight}"

    def score_for_solution_str(self, str):
        total_val, total_weight = self.get_total_value_and_weight_from_str(str)
        return total_val if total_weight <= self.max_weight else 0


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
        self.population_size = population_size
        self.number_iterations = number_iterations
        self.elitism_fraction = elitism_fraction
        self.cross_prob = cross_prob
        self.inner_mutation_prob = inner_mutation_prob
        self.mutation_prob = mutation_prob

        self.elites_size = int(self.population_size * self.elitism_fraction)
        if (self.population_size - self.elites_size) % 2 == 1:
            self.elites_size += 1
            self.elitism_fraction = self.population_size / float(self.elites_size)
            print(f"Changed elites fraction for rounding reasons to {self.elitism_fraction}")

        self.population = self.generate_first_population()

    def generate_first_population(self):
        pop = set()
        iteration = 0
        while len(pop) < self.population_size and iteration < 10000:
            solution = ""
            for j in range(len(self.problem)):
                solution += '1' if random.random() > 0.5 else '0'
            if self.problem.score_for_solution_str(solution) != 0:
                pop.add(solution)
            iteration += 1

        if len(pop) < self.population_size:
            raise Exception(f"Couldn't create {self.population_size} feasible solutions for first generation")

        return list(pop)

    def get_elites(self):
        sorted(self.population, key=lambda str_solution: self.problem.score_for_solution_str(str_solution))
        return self.population[:self.elites_size]

    def get_crossovers(self):
        def crossover(sol1, sol2):
            sol_len = len(sol1)
            res1 = sol1[:sol_len] + sol2[sol_len:]
            res2 = sol2[:sol_len] + sol1[sol_len:]
            return res1, res2

        crossovers = []

        num_crossovers = (self.population_size - self.elites_size) // 2
        for i in range(num_crossovers):
            indexes = random.sample(range(self.population_size), 2)
            parent1, parent2 = self.population[indexes[0]], self.population[indexes[1]]
            child1, child2 = crossover(parent1, parent2)

            crossovers.append(child1)
            crossovers.append(child2)

        return crossovers

    def mutate_solutions(self, solutions):
        def mutate(solution):
            for i in range(len(solution)):
                if random.random() < self.inner_mutation_prob:
                    mutation = '1' if solution[i] == '0' else '0'
                    if i == 0:
                        solution = mutation + solution[1:]
                    elif i == len(solution)-1:
                        solution = solution[:-1] + mutation
                    else:
                        solution = solution[:i] + mutation + solution[i+1:]
            return solution

        for i in range(len(solutions)):
            sol = solutions[i]
            if random.random() < self.mutation_prob or self.problem.score_for_solution_str(sol) == 0:
                mutation_iter = 0
                mutated_sol = mutate(sol)
                while self.problem.score_for_solution_str(mutated_sol) == 0 and mutation_iter < 100:
                    mutated_sol = mutate(mutated_sol)
                    mutation_iter += 1
                solutions[i] = mutated_sol

        return solutions

    def generate_next_populations(self):
        elites = self.get_elites()
        crossovers = self.get_crossovers()
        mutations = self.mutate_solutions(crossovers)
        self.population = elites + mutations

    def run(self):
        for i in range(self.number_iterations):
            self.generate_next_populations()
            # print statistics

        max_sol = max(self.population, key=lambda member: self.problem.score_for_solution_str(member))

        return self.problem.score_for_solution_str(max_sol) #self.problem.get_items_from_str(max_sol)

def genetic_search(filepath):
    problem = KnapsackGeneticProblem(filepath)
    agent = GeneticAlgorithmAgent(
        problem=problem,
        population_size=len(problem) * 500,
        number_iterations=1000,
        elitism_fraction=0.1,
        cross_prob=1,
        mutation_prob=0.5,
        inner_mutation_prob=1 / len(problem)
    )

    return agent.run()










