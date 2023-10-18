import pygad
import numpy
from random import randint
from time import sleep
import time
import matplotlib.pyplot as plt

num_rank=8
function_inputs = range(0,num_rank,1) # Function inputs. from 0 to n-1
desired_output = 0 # Function output.

# https://stackoverflow.com/questions/8713620/appending-to-one-list-in-a-list-of-lists-appends-to-all-other-lists-too
# be carefule of this, modify one, modify all
def get_exec_time(function_inputs):
    print(function_inputs)
    # run the particle advection to get exec time
    # psudu code, sleep random time
    start = time.time()
    # sleep(randint(1,3)/1000)
    # generate a assign_options.config according to input
    assignment_list=[[] for _ in range(len(function_inputs))]
    for index, v in enumerate(function_inputs):
        #print(index, v)
        assignment_list[v].append(index)
    #print(assignment_list)

    # write out plan
    f = open("assign_options.config",'w')
    for index, blocks in enumerate(assignment_list):
        #print(index, blocks)
        if len(blocks)==0:
            f.write("\n")
            continue
        for i, bid in enumerate(blocks):
            if i==0:
                f.write(str(bid))
            else:
                f.write(" "+str(bid))
        f.write("\n")
    f.close() 
    # call the particle advection based on plan
    
    
    end = time.time()
    exec_time = end-start 
    return exec_time

def fitness_func(ga_instance, solution, solution_idx):
    output = get_exec_time(function_inputs)
    fitness = 1.0 / numpy.abs(output - desired_output + 0.001)
    return fitness


print(get_exec_time([1,1,1,1,5,6,7,7]))

# num_generations = 500 # Number of generations.
# num_parents_mating = 10 # Number of solutions to be selected as parents in the mating pool.

# sol_per_pop = 20 # Number of solutions in the population.
# num_genes = len(function_inputs)

# last_fitness = 0
# def on_generation(ga_instance):
#     global last_fitness
#     print(f"Generation = {ga_instance.generations_completed}")
#     print(f"Fitness    = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]}")
#     print(f"Change     = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness}")
#     last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

# ga_instance = pygad.GA(num_generations=num_generations,
#                        num_parents_mating=num_parents_mating,
#                        sol_per_pop=sol_per_pop,
#                        num_genes=num_genes,
#                        fitness_func=fitness_func,
#                        on_generation=on_generation)

# # Running the GA to optimize the parameters of the function.
# ga_instance.run()

# ga_instance.plot_fitness()

# # Returning the details of the best solution.
# solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
# print(f"Parameters of the best solution : {solution}")
# print(f"Fitness value of the best solution = {solution_fitness}")
# print(f"Index of the best solution : {solution_idx}")

# prediction = numpy.sum(numpy.array(function_inputs)*solution)
# print(f"Predicted output based on the best solution : {prediction}")

# if ga_instance.best_solution_generation != -1:
#     print(f"Best fitness value reached after {ga_instance.best_solution_generation} generations.")

# # Saving the GA instance.
# filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
# ga_instance.save(filename=filename)

# # Loading the saved GA instance.
# loaded_ga_instance = pygad.load(filename=filename)
# loaded_ga_instance.plot_fitness()
