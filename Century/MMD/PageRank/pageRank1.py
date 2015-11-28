# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
from scipy.linalg import norm

import time
import functools

def tictoc(func):
    ''' Get time comsumed by func
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        t0 = time.clock()
        M = func(*args, **kw)
        t1 = time.clock() - t0
        return M, t1
    return wrapper

@tictoc
def getPageMat(fname):
    '''Get Matrix from pd.DataFrame
	
		Args: fname: file name 
		
		Returns: Rank Sparse Matrix: M; DataFrame: webGoogle
    '''
    t0 = time.clock()
    webGoogle = pd.read_csv(fname, sep = '\t', comment = '#', names = ['from', 'to'])
    t1 = time.clock() - t0
    print 'File Loaded, time consumed: %6.3fs' % t1
    data = np.repeat(1, webGoogle.shape[0])
    categ = np.unique(webGoogle.values)
    col_ind = pd.Categorical(webGoogle['from'], categories = categ).codes
    row_ind = pd.Categorical(webGoogle['to'], categories = categ).codes    
    M = csc_matrix((data, (row_ind, col_ind)))
    M = M.multiply(csr_matrix(1.0 / M.sum(axis=0)))	# watch out for div by zero warning
    return M, webGoogle

@tictoc
def getRank(M, beta = 0.8, eps = 1e-6):
    ''' Loop until get right rank
    
    	Args: M: rank matrix; beta: non-teleport weight; eps: epsilon
    	
    	Returns: Each node's Rank
    '''
    # Preparation
    n1, n2 = M.shape
    r1 = 1.0 / n2 * np.ones((n2, 1))
    r0 = np.ones((n2, 1))
    n = 0
    print '|Loop|  epsilon|time(s)|'
    print '|----|---------|-------|'
	# Loop
    while norm(r1 - r0, 1) > eps:
        t0 = time.clock()
        n += 1
        r0 = r1
        r1 = beta * M.dot(r0)
        r1 = r1 + (1 - beta) / n2
        sum_r1 = r1.sum()
        r1 = r1 + (1 - sum_r1) / n2
        t1 = time.clock() - t0
        print '|%4d|%6.3e|%7.3f|' % (n, norm(r1 - r0, 1), t1)
    return r1
    
if __name__ == '__main__':
    (M, webGoogle), t1 = getPageMat('web-Google.txt')
    print 'Mat Gotten, time consumed: %6.3fs' % t1
    r1, t1 = getRank(M, beta = 0.8, eps = 1e-6)
    print 'Rank Gotten, time consumed: %6.3fs' % t1
    categ = np.unique(webGoogle.values)
    print 'Node 99\'s score is %5.3e' % r1[np.nonzero(categ == 99)[0]]