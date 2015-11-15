pagerank.py - compute a pagerank score of a graph with 875713 nodes and 5105039 edges.
web-Google.txt - original file contains remark
web-Google1.txt - modified file with only FromNodeID and ToNodeID
output-info.txt - total time cost and loop information presented.

Algorithm is introduced in the course "Mining Massive Datasets" in Coursera. Data comes from the course's Program Assignment.

SOME POINTS NEEDED TO CARE
1 The node name in the data file is not continue, that is the real node name may be 0,1,2,3,5,6,7,8,10. This should be considered when you construct a Sparse Matrix and when you comput the matrix multiplicaiton. You should not use the name as index, because name may greater than index.
2 There may be some deadend node, who direct to no other node. About this, the lecture has dealed with it clearly ¡ª¡ª one should normalize the score vector after the teleport calculation.
3 Based on the lecture, the teleport part is same for every node, so we can add the teleport part without any matrix complex operation.
4 Last but not the least, FromNode index is the column index, ToNode index is the same as row index.

Note:
pagerank.py is a croase impletation, with no optimization. It use dict to represent vector, this made the computation is very time-comsuming. Maybe a hash table which maps name to index can be useful.
we can also refer this site, https://class.coursera.org/mmds-003/forum/thread?thread_id=152, use pandas and numpy to improve performence.