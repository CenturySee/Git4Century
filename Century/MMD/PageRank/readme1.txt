This file is an description of pageRank1.py

1 Method in pageRank1 mainly refers information present in this page:
https://class.coursera.org/mmds-003/forum/thread?thread_id=152
In that page, a detailed procedure was proposed by Hannes De Valkeneer.

2 During the completion, I found that some basic operation about numpy.ndarray and pandas.DataFrame are very easy to use.
Such as:
	data = np.repeat(1, webGoogle.shape[0])
    categ = np.unique(webGoogle.values)
    col_ind = pd.Categorical(webGoogle['from'], categories = categ).codes
    row_ind = pd.Categorical(webGoogle['to'], categories = categ).codes 
this briefly get the indice needed to construct the sparse matrix

3 ndarray and matrix are easy to use too. The slice operation is very efficient.

4 transformation from matrix and ndarray to list are described in http://stackoverflow.com/questions/5183533/how-to-make-list-from-numpy-matrix-in-python
as below:
	a = numpy.matrix([[ 0.16666667, 0.66666667, 0.16666667]])
	list(numpy.array(a).reshape(-1,))
	or
	numpy.array(a).reshape(-1,).tolist()
	or
	numpy.array(a)[0].tolist()
Another point is that matrix is always 2d.

5 operations about scipy.sparse.cs*_matrix are very efficient. So use build-in function rather than element wise operations to handle with sparse matrix. Especially when you encounter a very large sparse matrix, because such matrix may trigger memory error if you use different operation sequence.