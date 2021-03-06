from deap import base, creator
import random
from deap import tools
import numpy as np
import utils

V = [[0,1,0,1,0],
     [1,0,1,0,1],
     [0,1,0,0,0],
     [1,0,0,0,1],
     [0,1,0,1,0]]

#V = [[0,1,0],
#     [1,0,1],
#     [0,1,0]]

#V =[[0,1,0,1,0,0,0,1],
#        [1,0,1,0,0,0,0,0],
#        [0,1,0,1,1,0,0,0],
#        [1,0,1,0,0,0,0,1],
#        [0,0,1,0,0,1,0,0],
#        [0,0,0,0,1,0,0,1],
#        [0,0,0,0,0,0,0,1],
#        [1,0,0,1,0,1,1,0]]

#V = utils.read_matrix_edgeList('../resources/facebook_4039N.txt')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", np.ndarray, fitness=creator.FitnessMin)

IND_SIZE = 1#len(V), len(V[0])


def genIndividual():
    return np.random.rand(len(V), 100)

toolbox = base.Toolbox()
###########
#import multiprocessing
#multiprocessing.freeze_support()
#pool = multiprocessing.Pool()
#toolbox.register("map", pool.map)
#from scoop import futures
#
#toolbox.register("map", futures.map)
############

toolbox.register("attribute", genIndividual)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    ind_ = individual[0]
    V_ = ind_.dot(ind_.T)
    dis = V-V_
    fit = np.linalg.norm(dis)
    return fit,

def mCX(ind1_, ind2_):
    ind1, ind2 = ind1_[0], ind2_[0]
    cX_point = random.randint(1,len(ind1))#len(ind1)/2
    ind1[:cX_point], ind2[:cX_point] = ind2[:cX_point].copy(), ind1[:cX_point].copy()
    return ind1_, ind2_
    
def mMut(ind, mu, sigma, indpb):
    rInd = ind[0].reshape(len(ind[0])*len(ind[0][0]))
    tools.mutGaussian(rInd, mu, sigma, indpb)
    return ind

toolbox.register("mate", mCX) #tools.cxTwoPoint)
toolbox.register("mutate", mMut, mu=0, sigma=1, indpb=0.2)#tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

# statistics registeration
stats = tools.Statistics(key=lambda ind: ind.fitness.values)
#stats.register("avg", np.mean)
#stats.register("std", np.std)
stats.register("min", np.min)
#stats.register("max", np.max)
#

def main():
    pop = toolbox.population(n=5000)
    CXPB, MUTPB, NGEN = 0.9, 0.2, 50

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)
        
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # printing statistics
        record = stats.compile(pop)
        print "gen #%d: stats:%s"%(g, str(record['min']))
    return pop

if __name__ == '__main__':
    import time

    start = time.time()
    
    import multiprocessing
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()
    toolbox.register("map", pool.map)
    multiprocessing.freeze_support()
    pop = main()
    
    end = time.time()
    print(end - start)

#print pop

    minInd = min(pop , key = lambda ind: ind.fitness.values[0])
