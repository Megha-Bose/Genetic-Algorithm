from genetic import FitnessFunc, mutation, population_fitness, run_evolution
from client import *
# from random import choices, randint, randrange, random
import random
import numpy as np

# API_ENDPOINT = 'http://10.4.21.156'
# MAX_DEG = 11
# SECRET_KEY='jg3q0CzLVQl9Jsf4PmLIUjuxMK4yU7Vh4b6FzthUbocuLqpvGG'

POPULATION_SIZE = 15
MATING_POOL_SIZE = 8
GENE_LENGTH = 11
MUTATION_PROB = 0.3
TRAIN_WT = 0.6

# vector_overfit = [0.0, -1.457990220064754e-12, -2.2898007842769645e-13, 4.620107525277624e-11, -1.7521481289918844e-10, -1.8366976965696096e-15, 8.529440604118815e-16, 2.2942330256117977e-05, -2.0472100298772093e-06, -1.597928341587757e-08, 9.982140340891233e-10]
population = []
child_population = []
mating_pool = []
# [(genome, [fitness, error1, error2])]

def generate_genome():
    return [0.0 for _ in range(GENE_LENGTH)]
    # return [random.uniform(-10.0, 10.0) for _ in range(GENE_LENGTH)]

def find_fitness(genome):
    # return [0, 0, 0]
    error = get_errors(SECRET_KEY, list(genome))
    fitness = abs(error[0] * TRAIN_WT + error[1])

    return [fitness, error[0], error[1]]

def generate_population():
    
    global population
    population = []
    tmp =  [generate_genome() for _ in range(POPULATION_SIZE)]
    for i in range(0, len(tmp)):
        tmp[i] = mutation(tmp[i])
        population.append((tmp[i], find_fitness(tmp[i])))
    

# create_population():
#     generate POPULATION_SIZE no. of vectors that are initially zero, but then mutated
#     calculate the fitness 
#     Population's format will be this: [([coeffi.], [fitness, errors])] 
#     return

def compare(xx):
    return xx[1][0]
    # return (xx[1][0] < yy[1][0])

def generate_mating_pool():
    global population
    global mating_pool
    population = sorted(population, key=compare)
    mating_pool = population[:MATING_POOL_SIZE+1]
    # population_fitness = population_fitness[np.argsort(population_fitness[:,-1])]
    # pool = population_fitness[:MATING_POOL_SIZE]
    # return pool

def single_point_crossover(parent1, parent2):
    split_point = random.randint(1, GENE_LENGTH - 1)
    return parent1[0:split_point] + parent2[split_point:], parent2[0:split_point] + parent1[split_point:]


def reproduce():
    int p1 = random.randint(0, MATING_POOL_SIZE)
    int p2 = random.randint(0, MATING_POOL_SIZE)

    ch1, ch2 = single_point_crossover(mating_pool[p1], mating_pool[p2])

    #save children
    ch1 = mutation(ch1)
    ch2 = mutation(ch2)

    #save mutated children

    child_population.append([(ch1, find_fitness(ch1))])
    child_population.append([(ch2, find_fitness(ch2))])
    

def get_mutated_value(index):
    
    return vector_overfit[index] * random.uniform(0.7, 1.3)

def mutation(genome):
    for _ in range(GENE_LENGTH):
        index = random.randrange(len(genome))
        genome[index] = genome[index] if random.random() > MUTATION_PROB else get_mutated_value(index)
    return genome

def eliminate():
    new_generation = np.concatenate((population, child_population))
    new_generation = sorted(new_generation, key=compare)
    # new_generation = new_generation[np.argsort(new_generation[:,1])]
    new_generation = new_generation[:POPULATION_SIZE]

def run_evolution(gen_from = 1, gen_to = 1):
    global population
    global child_population
    global mating_pool
    if gen_from < gen_to:
        return
    # don't generate population now
    # generate_population()
    population = [([0.0, 0.0, -2.1739141281531437e-13, 0.0, -1.4561868231662278e-10, -1.5842073079191948e-15, 0.0, 0.0, 0.0, 0.0, 0.0], [3202326122322.816, 1671604981369.1196, 2199363133501.344]), ([0.0, 0.0, -2.200983436642408e-13, 0.0, -1.6545482466998874e-10, 0.0, 0.0, 0.0, 0.0, 0.0, 1.2012131290102736e-09], [1787501852962423.8, 708690771137648.6, 1362287390279834.5]), ([0.0, -1.3718695642164273e-12, -2.86133490083856e-13, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [4843747391685.002, 2031280283262.1824, 3624979221727.693]), ([0.0, 0.0, 0.0, 5.613079885787623e-11, 0.0, 0.0, 0.0, 0.0, 0.0, -2.0084714835345754e-08, 0.0], [149293156155848.7, 64596995175366.9, 110534959050628.53]), ([0.0, -1.254797393636453e-12, 0.0, 0.0, -1.9816456649250936e-10, -1.4862867833593057e-15, 0.0, 1.6139079295651645e-05, 0.0, -1.5381735682487136e-08, 0.0], [28838463071035.438, 15140527616923.943, 19754146500881.074]), ([0.0, -1.824992247402601e-12, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.4063916859032531e-08, 1.123813084074328e-09], [897215076546148.8, 360811513772808.06, 680728168282463.9]), ([0.0, -1.8129626145758811e-12, -2.973783231827174e-13, 0.0, 0.0, -1.955994378414344e-15, 0.0, 0.0, -2.0863021928616105e-06, 0.0, 0.0], [876533167437959.5, 359409914383397.4, 660887218807921.1]), ([0.0, -1.3993610988331725e-12, 0.0, 0.0, 0.0, 0.0, 6.065471086558722e-16, 0.0, -2.6480494438847392e-06, -1.2287590644834781e-08, 0.0], [2018753293010257.5, 800139320577396.9, 1538669700663819.2]), ([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.30852298462043e-16, 0.0, 0.0, -1.4660991952706303e-08, 0.0], [71683202274045.36, 32365392945814.82, 52263966506556.47]), ([0.0, 0.0, 0.0, 0.0, 0.0, -1.4722462805110977e-15, 8.007410689738932e-16, 0.0, 0.0, -1.7547439065939982e-08, 0.0], [132154022512029.9, 60035923475319.05, 96132468426838.47]), ([0.0, -1.8181338920696735e-12, 0.0, 0.0, 0.0, 0.0, 1.0525064451094843e-15, 0.0, 0.0, -2.0246369703864914e-08, 0.0], [152044657086393.12, 65731802901156.64, 112605575345699.12]), ([0.0, 0.0, 0.0, 0.0, 0.0, -1.3262998900637332e-15, 8.806472082009527e-16, 0.0, 0.0, 0.0, 0.0], [3266688980915.4097, 1604752921194.4478, 2303837228198.741]), ([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.9688775070167554e-08, 0.0], [142661107705871.4, 61860101103981.71, 105545047043482.38]), ([0.0, 0.0, 0.0, 0.0, -2.218190564099299e-10, 0.0, 8.479603830964833e-16, 0.0, -1.951988168094533e-06, -1.1987831452245436e-08, 8.883025950187915e-10], [24834923737395.79, 9610995233228.566, 19068326597458.65]), ([0.0, 0.0, 0.0, 4.710860523699774e-11, 0.0, -1.831653523429603e-15, 0.0, 0.0, -1.8157959296073442e-06, -1.6157715518106916e-08, 0.0], [1356563206368001.0, 549459462101533.0, 1026887529107081.2])]
    generate_mating_pool()
    print()
    print(mating_pool)
    print()
    # return
    #save_pop

    for i in range(gen_from, gen_to+1):
        child_population = []
        mating_pool = generate_mating_pool()
        #save_pool

        for j in range(5):
            reproduce()
        
        eliminate()


if __name__ == "__main__":
    run_evolution(1, 1)
    # print()
    # print(population)
    # print()
    # generate_population()
    # print(population)


# [([], [])] 


# def find_fitness(parent):
#     error = get_errors(SECRET_KEY, list(parent))
#     fitness = abs(error[0] * TRAIN_WT + error[1])

#     return [fitness, error[0], error[1]]


# def population_fitness(population):
#     fitness = np.zeros(POPULATION_SIZE)
#     for i in range(POPULATION_SIZE):
#         error = get_errors(SECRET_KEY, list(population[i]))
#         fitness[i] = abs(error[0] * TRAIN_WT + error[1])


# mating_pool():
#     return an array that with 10 best vectors that's randomly shuffled

# reproduce():
#     randomly choose two vectors from the mating pool and then cross them
#     get the ChildProcessError
#     # mutate the child

#     find fitness
#     add the child to child_population (similar to population)

# mutate_children():
#     mutate children in child_population


# create_population():
#     generate POPULATION_SIZE no. of vectors that are initially zero, but then mutated
#     calculate the fitness 
#     Population's format will be this: [([coeffi.], [fitness, errors])] 
#     return

# main:
#     call run_evolution(no of generations)

# eliminate():
#     eliminate some people with the least fitness or using some heuristics
#     and update population

# run_evolution(gen_from=1, gen_to):
#     create a population

#     save_population

#     loop from gen_from to gen_to times:
#         clear child_population
#         mat_pool = mating_pool()
#         save_pool()
    
#         loop POOL_SIZE/2:
#             reproduce(mat_pool)
#         save_children()
#         mutate_children()
#         save_mutated_children()
#         eliminate()

#         save_population()


# {
#     generation:
#     initial_population: []
#     children: 
#     mutated_children:
#     final_population:
#     best_vector:
# }
