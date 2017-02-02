#!/usr/bin/env python
#coding:utf-8
"""
  Purpose:  Stochastic block model
  Created:  01/02/2017
"""
from time import clock
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#----------------------------------------------------------------------
def degreesExpectations(probability_matrix, n_communities, community_labels):
    """Calculate expected degrees of each community"""
    n = [len(np.argwhere(community_labels==i)) for i in xrange(n_communities)] # number of vertices per communities (n1, n2, ..., nk)
    return np.dot(probability_matrix[:n_communities,:n_communities], n) # return [E(d1), E(d2), ..., E[d(k)]]

#----------------------------------------------------------------------
# Stochastic block model parameters
n_vertices = 50  # number of vertices
n_communities = 2  # number of communities
community_labels = np.random.randint(low=0, high=n_communities, size=n_vertices) # community label assigned to each vertex
probability_matrix = np.array([
    [0.0, .1, .1, .01],
    [.1, 0.9, .9, .01],
    [.1, .9, 0.5, .01],
    [.01, .01, .01, 0.1],
]) # matrix of edge probabilities
if(not (probability_matrix.transpose() == probability_matrix).all()):
    raise ValueError("Probability matrix has to be symmetric")
graph_matrix = np.zeros((n_vertices, n_vertices), dtype=int) # adjacency matrix initialization

#----------------------------------------------------------------------
# Adjacency matrix generation (strictly lower triangular as graph is undirected)
t0 = clock()
for i in xrange(n_vertices):
    for j in xrange(i):
        community_i = community_labels[i]
        community_j = community_labels[j]
        val = probability_matrix[community_i][community_j]
        p = np.random.rand()
        if p <= val:
            graph_matrix[i][j] = 1

print("Time taken to generate the graph: " + str((clock() - t0)*1000) + "ms\n")
G = nx.from_numpy_matrix(graph_matrix) # generate networkx graph

#----------------------------------------------------------------------
# Draw generated graph and print communities
color_map = ['cyan', 'red', 'yellow', 'magenta', 'blue', 'green', 'white'][:n_communities]
node_color = [color_map[i] for i in community_labels]
labels = {key: key+1 for key in xrange(n_vertices)} # vertices numbers
nx.draw(G, labels=labels, node_color=node_color, font_size=12)

degrees_expectations = degreesExpectations(probability_matrix, n_communities, community_labels)
for i in xrange(n_communities):
    indices = [j+1 for j, x in enumerate(community_labels) if x == i]
    print("Community C{}, color: {}, E[di] = {}".format(str(i), color_map[i], degrees_expectations[i]))

plt.show()
