import sys
import genetic
from datetime import datetime

def milliseconds(timediff):
    return ((timediff.seconds * 1000000) + timediff.microseconds) / 1000.0

def calc_avg(filepath, num_iter=10):
    avg_score = 0
    avg_time = 0

    for i in range(num_iter):
        t0 = datetime.now()
        avg_score += genetic.genetic_search(filepath)[0]
        t1 = datetime.now()
        avg_time += milliseconds(t1-t0)

    return avg_score / num_iter, avg_time / num_iter

def find_hyper():
    outfile = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\test.txt"
    # filepath = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\knapPI_1_1000_1000_1"
    filepath = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\knapPI_1_100_1000_1"
    results = []

    population_sizes = [50,100,500]
    number_iterations = [150] # [10,50,100,120]
    elitism_fractions = [ef / 100.0 for ef in range(20, 55, 5)] # [0.05,0.1,0.15,0.2,0.25,0.3]
    cross_probs = [0,0.1,0.4,0.7,1]

    problem = genetic.KnapsackGeneticProblem(filepath)
    mutation_probs = [0,0.1,0.4,0.7,1]
    inner_mutation_probs = [imp / 100.0 for imp in range(0, 30, 5)]

    start_item_counts = [1]#[count for count in range(1, len(problem)//10, max(len(problem)//10//10, 1))]


    header_line = "population size,number iterations,elitism fraction,crossover probability,mutation probability,inner mutation probability,score,weight"

    for pop_size in [1000]:#population_sizes:
        for num_iter in [1000]:#number_iterations:
            for elit_frac in [0.35]:#elitism_fractions:
                for cross_prob in [0.7]:#cross_probs:
                    for mut_prob in [1]:#mutation_probs:
                        for inner_mut_prob in [0.05]:#inner_mutation_probs:
                            for start_count in start_item_counts:
                                header_line += ""
                                problem = genetic.KnapsackGeneticProblem(filepath)
                                agent = genetic.GeneticAlgorithmAgent(
                                    problem,
                                    len(problem),
                                    len(problem),
                                    elit_frac,
                                    cross_prob,
                                    mut_prob,
                                    inner_mutation_prob=1 / len(problem),
                                )
                                score, items = agent.run()
                                total_weight = sum([item.weight for item in items])

                                parameter_str = f"{pop_size},{num_iter},{elit_frac},{cross_prob},{mut_prob},{inner_mut_prob}"#,{start_count}"
                                print(f"{parameter_str}  -  {score}")
                                results.append(f"{parameter_str},{score},{total_weight}")

    with open(outfile, 'w') as file:
        file.write(header_line + '\n')
        for result in results:
            file.write(result + '\n')


if __name__ == '__main__':
    filepath = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\knapPI_1_100_1000_1"
    avg_score, avg_time = calc_avg(filepath)
    print(f"Score: {avg_score}, TIme: {avg_time}")