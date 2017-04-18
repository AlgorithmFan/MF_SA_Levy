#from deap import base, creator
import random
from deap import tools
import numpy as np
import utils
from cs_nmf_base import *
#from scipy.stats import levy_stable as levys
from scipy.special import gamma
from math import sin, pi

dataset = ('movelens 100k', '../resources/ml-100k/final_set.csv')
#dataset = ('movelens 1m', '../resources/ml-1m/ratings.dat')
train, test, mSize = utils.read_data_to_train_test(dataset[1], zero_index = False)

V = utils.create_matrix(train, mSize)
maskV = np.sign(V)

r_dim = 20

def generate_ind():
    #r = np.random.rand(r_dim)
    #r = np.random.uniform(5./r_dim, 0, size = r_dim)
    r = np.random.normal(5./r_dim, .1, size = r_dim)
    #r = np.random.randn(r_dim)*.1
    return r
  
def evaluate_ind(ind):
    W, H = ind[:mSize[0]], ind[mSize[0]:]
    predV = maskV * W.dot(H.T)

    fit = utils.rmse(V, predV, len(train))#np.linalg.norm(V-predV)
    
    return fit,
    
def mantegna_levy_step(_lambda=1.5, size=None):
    sigma = gamma(1+_lambda) * sin(pi*_lambda/2.)
    sigma /= _lambda * gamma((1+_lambda)/2.) * 2**((_lambda-1)/2.)
    sigma = sigma**(1./_lambda)
    u = np.random.randn(size[0], size[1])*sigma #normal(scale=sigma, size=size)
    v = np.absolute(np.random.randn(size[0], size[1]))
    step = u/np.power(v, 1./_lambda)
    
    sStep = np.sign(step)
    step = np.abs(step)
    step = np.maximum(step, 2)
    step = step*sStep
    
    return step

def levy_grw( _lambda=1.5, stepSize=0.01, cuckoo=None, step=None):
    levy = _lambda * gamma(_lambda)*sin(pi*_lambda/2)/(pi*step**(2))
    cuckoo += stepSize * levy 
    
    return cuckoo
 
def levy_lrw( _lambda=1.5, pa = 0.25, stepSize=0.01, c1=None, c2=None, step=None):  
    c1 += stepSize * step * (c1-c2) * np.random.randn(c1.shape[0], c1.shape[1])
    return c1
    
    
if __name__ == '__main__':
    pa = 0.3
    nIter = 100
    nCuckoos = 10
    l_rw = levy_lrw #levy_lrw_withBest #rand_cuckoos #
    g_rw = levy_grw
    stepFunction = mantegna_levy_step
    select = tools.selBest # selTour #
    _lambda = 1.5
    maxS = 1e-1
    minS = 1e-2
    method_name = "CS"
    
    cs = CS_NMF()
    cuckoos = cs.run_cs(pa = pa, nIter = nIter, ind_size = mSize[0]+mSize[1], nCuckoos = nCuckoos, ind_gen = generate_ind,
                l_rw = l_rw, g_rw = g_rw, select = select, evaluate = evaluate_ind, stepFunction = stepFunction,
                _lambda = _lambda, max_stepSize = maxS, min_stepSize = minS, curve_label = method_name)
                
    #printng results:
    minInd = min(cuckoos , key = lambda ind: ind.fitness.values[0])
    W, H = minInd[:mSize[0]], minInd[mSize[0]:].T
    ga_results = utils.print_results(uMat = W, iMat = H, nFeatures = r_dim, 
                                    train_data = train, test_data = test, 
                                    method_name = method_name, nIterations = nIter, 
                                    dataset_name = dataset[0],
                                    method_details = [('nCuckoos',nCuckoos),
                                        ('local random walk', l_rw.__name__),
                                        ('global random walk',g_rw.__name__),
                                        ('step function', stepFunction.__name__),
                                        ('random walk selection', select.__name__),
                                        ('pa', pa),
                                        ('lambda', _lambda),
                                        ('stepSize', (maxS,minS))]
                                    )
    
    
    