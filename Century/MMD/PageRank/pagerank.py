# coding:utf-8
def loadFile(fname = 'web_Google1.txt'):
	'''read file and generate data needed to construct sparse matrix
	
	Args:
		fname: file name to read
		
	Returns:
		Three dicts which represent Matrix and node weight
		li: key = Matrix's row, value = node list which direct to key
		wj: key = Matrix's column, value = weight of key(Matrix's elements)
		r : key = all nodes, value = original weight
		
	Raises:
		IOError: An error occured if fnmae is not found.
	'''
	li = {}
	wj = {}
	r = {}
	N = 875713	# number of node
	f = open(fname, 'r')
	line = f.readline()
	while line:
		# parse each line
		tmp = line.split()
		i = int(tmp[1])
		j = int(tmp[0])
		# construct li
		if li.has_key(i):
			li[i].append(j)
		else:
			li[i] = [j,]
		# construct wj
		if wj.has_key(j):
			wj[j] += 1
		else:
			wj[j] = 1
		# construct r
		if not r.has_key(i):
			r[i] = 1.0/N
		if not r.has_key(j):
			r[j] = 1.0/N
		line = f.readline()
	f.close()
	# modify wj to weight
	for k in wj.keys():
		wj[k] = 1.0/wj[k]
	return li, wj, r

def mnorm(d1, d2):
	'''Compute the 1 norm of two diffrent directary
	
	Args:
		d1: one directory
		d2: the other directory
		
	Returns:
		res: 1 norm of d1 - d2 (same as d2 - d1)
	'''
	res = 0.0
	for k in d1.keys():
		diff = d1[k] - d2[k]
		res += diff if diff>0 else -diff
	return res
	
def msum(d1):
	'''Compute sumation of a dict's value
	
	Args:
		d1: a dict whose value is a number
	
	Returns:
		res: summation of d1's value
	'''
	res = 0.0
	for k in d1.keys():
		res += d1[k]
	return res
	
def mmul(d1, b):
	'''Change di's value to b*d1.value
		d1.value *= b
	'''
	for k in d1.keys():
		d1[k] *= b
		
def madd(d1, b):
	'''Change di's value to b + d1.value
		d1.value = b + d1.value
	'''
	for k in d1.keys():
		d1[k] += b
		
def massign(d1, d2):
	'''asign the second dict d2 to the first dict d1
		d1 = d2
	'''
	for k in d1.keys():
		d1[k] = d2[k]
		
def mclear(d1):
	'''change d1.value to 0
		d1.value = 0
	'''
	for k in d1.keys():
		d1[k] = 0
	
if __name__ == '__main__':
	import time
	try:
		import cPickle as pickle
	except ImportError:
		import pickle
	# 0 some constant can be provided
	beta = 0.8 # probability of 1 - p(teleport)
	N = 875713 # number of nodes
	# 1 load data
	start = time.clock()
	li, wj, r1 = loadFile('web-Google1.txt')
	end = time.clock()
	print 'load file and get Mat:\t %8.5f s'%(end - start)
	# 2.0 set r0(to record previous r in every iterate)
	r0 = {}
	for k in r1.keys():
		r0[k] = 0
	print 'norm(r1) = %f, norm(r0) = %f' %(msum(r1), msum(r0))
	print 'Difference between two dict is: %f' % mnorm(r0, r1)
	# 2.1 loop untill converge
	n = 0
	print 'LoopN \t Diff \t\t norm1 \t\t norm0 \t\t time(s)'
	start = time.clock()
	while mnorm(r0, r1) > 1e-8:
		start1 = time.clock()
		# update r0
		massign(r0, r1)
		mclear(r1)
		# main loop to compute new score of node k
		for k in li.keys():
			l = li[k]
			for x in l:
				r1[k] += wj[x]*r0[x]
		# result with no teleport
		mmul(r1, beta)
		# result with teleport(change here to acheive a Topic-Specific PageRank)
		madd(r1, (1 - beta) / N)
		# result with normalization because of the existence of deadend
		madd(r1, (1 - msum(r1)) / N)
		# iterate number
		n += 1
		end1 = time.clock()
		print '%d \t %10.6e \t %10.6e \t %10.6e \t %10.8f' %(n, mnorm(r0, r1), msum(r1), msum(r0), end1-start1)
	end = time.clock()
	print 'Number of Loop : %d' % n
	print 'Time Consumnption : %8.5f s' % (end - start)
	# 3.0 print result
	print 'result is r1[99] is %.6e...' %r1[99]
	# 3.1 save every nodes' score
	f = open('r1-8.dat','wb')
	pickle.dump(r1, f)
	f.close()