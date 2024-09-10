import sys
import genetic
from datetime import datetime
import os

large_scale_folder = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\"
large_scale_optimum_folder = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale-optimum\\"


def get_file_names(items, weight):
    return [f"knapPI_{i}_{items}_{weight}_1" for i in range(1, 4)]


files = {
    (items, weight): [(large_scale_folder + name, large_scale_optimum_folder + name)
                      for name in get_file_names(items, weight)]
    for (items, weight) in [
        (100, 1000),
        (200, 1000),
        (500, 1000),
        #(1000, 1000),
    ]}

print(files)

def milliseconds(timediff):
    return ((timediff.seconds * 1000000) + timediff.microseconds) / 1000.0


def calc_avg(filepath, num_iter=10):
    avg_score = 0
    avg_time = 0

    for i in range(num_iter):
        t0 = datetime.now()
        avg_score += genetic.genetic_search(filepath)[0]
        t1 = datetime.now()
        avg_time += milliseconds(t1 - t0)

    return avg_score / num_iter, avg_time / num_iter

def population_vs_iterations():
    factors = [0.5, 1, 2, 3]

    results = []

    headers = "population size factor,number iterations factor,score percent"
    output_file = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\pop_vs_iter.txt"

    for pop_factor in factors:
        for num_ters_factor in factors:
            total_avg = 0
            percent_avg = 0
            count = 0
            for key in files.keys():
                for i,(prob_file, opt_file) in enumerate(files[key]):
                    problem = genetic.KnapsackGeneticProblem(prob_file)
                    agent = genetic.GeneticAlgorithmAgent(
                        problem,
                        population_size_factor=pop_factor,
                        number_iterations_factor=num_ters_factor,
                        expected_items_mutated=1
                    )

                    avg = 0
                    for iter in range(5):
                        score, items = agent.run()
                        avg += score
                    avg /= 5

                    with open(opt_file, 'r') as f:
                        optimal = float(f.readline())
                        percent_avg *= count
                        percent_avg += avg / optimal * 100
                        percent_avg /= count+1
                        print(f"{(pop_factor, num_ters_factor, key[0])} = {percent_avg}")

                    total_avg *= count
                    total_avg += percent_avg
                    total_avg /= count+1

                    count += 1

                    print(f"{(pop_factor, num_ters_factor)}-{count} = {total_avg}")

            print(f"--------------- RES FOR {(pop_factor,num_ters_factor)} -----------------------------")
            print(f"{(pop_factor, num_ters_factor)} = {total_avg}")
            print(f"--------------------------------------------------------------")
            results.append(f"{pop_factor},{num_ters_factor},{total_avg}")

    with open(output_file, 'w') as file:
        file.write(headers + '\n')
        for result in results:
            file.write(result + '\n')


def find_hyper():
    outfile = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\test.txt"
    # filepath = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\knapPI_1_1000_1000_1"
    filepath = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\knapPI_1_100_1000_1"
    filepath = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\knapPI_1_100_1000_1"

    population_sizes = [50, 100, 500]
    number_iterations = [150]  # [10,50,100,120]
    elitism_fractions = [ef / 100.0 for ef in range(20, 55, 5)]  # [0.05,0.1,0.15,0.2,0.25,0.3]
    cross_probs = [0, 0.1, 0.4, 0.7, 1]

    problem = genetic.KnapsackGeneticProblem(filepath)
    mutation_probs = [0, 0.1, 0.4, 0.7, 1]
    inner_mutation_probs = [imp / 100.0 for imp in range(0, 30, 5)]

    start_item_counts = [1]  #[count for count in range(1, len(problem)//10, max(len(problem)//10//10, 1))]

    header_line = "population size,number iterations,elitism fraction,crossover probability,mutation probability,inner mutation probability,score,weight"

    results = []
    for pop_size in [1000]:  #population_sizes:
        for num_iter in [1000]:  #number_iterations:
            for elit_frac in [0.35]:  #elitism_fractions:
                for cross_prob in [0.7]:  #cross_probs:
                    for mut_prob in [1]:  #mutation_probs:
                        for inner_mut_prob in [0.05]:  #inner_mutation_probs:
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

                                parameter_str = f"{pop_size},{num_iter},{elit_frac},{cross_prob},{mut_prob},{inner_mut_prob}"  #,{start_count}"
                                print(f"{parameter_str}  -  {score}")
                                results.append(f"{parameter_str},{score},{total_weight}")

    with open(outfile, 'w') as file:
        file.write(header_line + '\n')
        for result in results:
            file.write(result + '\n')

def crossover_methods():
    crossover_methods = {
        1: "halfway",
        2: "random",
        3: "score based"
    }

    results = []

    headers = "crossover method,score percent"
    output_file = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\crossRes.txt"

    for crossover_method in crossover_methods.values():
        total_avg = 0
        percent_avg = 0
        count = 0
        for key in files.keys():
            for i,(prob_file, opt_file) in enumerate(files[key]):
                problem = genetic.KnapsackGeneticProblem(prob_file)
                agent = genetic.GeneticAlgorithmAgent(
                    problem,
                    cross_method=crossover_method
                )

                avg = 0
                for iter in range(5):
                    score, items = agent.run()
                    avg += score
                avg /= 5

                with open(opt_file, 'r') as f:
                    optimal = float(f.readline())
                    percent_avg *= count
                    percent_avg += avg / optimal * 100
                    percent_avg /= count+1
                    print(f"{(crossover_method, key[0])} = {percent_avg}")

                total_avg *= count
                total_avg += percent_avg
                total_avg /= count+1

                count += 1

                print(f"{(crossover_method)}-{count} = {total_avg}")

        print(f"--------------- RES FOR {(crossover_method)} -----------------------------")
        print(f"{(crossover_method)} = {total_avg}")
        print(f"--------------------------------------------------------------")
        results.append(f"{crossover_method},{total_avg}")

    with open(output_file, 'w') as file:
        file.write(headers + '\n')
        for result in results:
            file.write(result + '\n')

def test_first_gen():
    random_inits = [True,False]

    results = []

    headers = "random init,score percent"
    output_file = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\initRes.txt"

    for random_init in random_inits:
        total_avg = 0
        percent_avg = 0
        count = 0
        for key in files.keys():
            for i,(prob_file, opt_file) in enumerate(files[key]):
                problem = genetic.KnapsackGeneticProblem(prob_file)
                agent = genetic.GeneticAlgorithmAgent(
                    problem,
                    cross_method="halfway",
                    random_init=random_init
                )

                avg = 0
                for iter in range(5):
                    score, items = agent.run()
                    avg += score
                avg /= 5

                with open(opt_file, 'r') as f:
                    optimal = float(f.readline())
                    percent_avg *= count
                    percent_avg += avg / optimal * 100
                    percent_avg /= count+1
                    print(f"{(random_init, key[0])} = {percent_avg}")

                total_avg *= count
                total_avg += percent_avg
                total_avg /= count+1

                count += 1

                print(f"{(random_init)}-{count} = {total_avg}")

        print(f"--------------- RES FOR {(random_init)} -----------------------------")
        print(f"{(random_init)} = {total_avg}")
        print(f"--------------------------------------------------------------")
        results.append(f"{random_init},{total_avg}")

    with open(output_file, 'w') as file:
        file.write(headers + '\n')
        for result in results:
            file.write(result + '\n')

if __name__ == '__main__':
    test_first_gen()

# if __name__ == '__main__':
#     filepath = "C:\\Users\\alonl\\Documents\\GitHub\\AI-final-2\\input\\large_scale\\knapPI_1_100_1000_1"
#     avg_score, avg_time = calc_avg(filepath)
#     print(f"Score: {avg_score}, TIme: {avg_time}")
