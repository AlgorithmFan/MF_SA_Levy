#from deap import base, creator
import random
from deap import tools
import numpy as np
import utils
import ga_nmf_base as ga

#V = [[0,1,0,1,0],
#     [1,0,1,0,1],
#     [0,1,0,0,0],
#     [1,0,0,0,1],
#     [0,1,0,1,0]]

#V = [[0,1,0],
#     [1,0,1],
#     [0,1,0]]

V =[[0,1,0,1,0,0,0,1],
    [1,0,1,0,0,0,0,0],
    [0,1,0,1,1,0,0,0],
    [1,0,1,0,0,0,0,1],
    [0,0,1,0,0,1,0,0],
    [0,0,0,0,1,0,0,1],
    [0,0,0,0,0,0,0,1],
    [1,0,0,1,0,1,1,0]]

#V = utils.read_matrix_edgeList('../resources/facebook_4039N.txt')

r_dim = 5

def genIndividual():
    return np.random.rand(len(V), r_dim)
    
def evaluate_ind(individual):
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
    
pop = ga.run_ga(ind_gen = genIndividual, mate = mCX, mutate = mMut, evaluate = evaluate_ind)

#print pop

minInd = min(pop , key = lambda ind: ind.fitness.values[0])