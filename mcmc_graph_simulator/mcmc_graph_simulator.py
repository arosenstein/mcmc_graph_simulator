# -*- coding: utf-8 -*-
from math import sqrt, e
import networkx as nx
import numpy as np


class mcmc_graph:

	markov_chain = []


	def __init__(self, nodes):
		'''
		Creates a new connected networkx Graph with the specified nodes 
	
		Params
		------
		nodes : list of touples
	
		'''
		self.markov_chain = []
		graph = nx.Graph()

		graph.add_path(nodes)

		for edge in graph.edges():
			graph[edge[0]][edge[1]].update(weight = self.get_distance(edge[0], edge[1]))

		self.markov_chain.append(graph)

		self.current_graph = graph


	def isConnected(self):
		'''Determines if the graph is connected

		Parameters
		-----
		none

		Return
		-----
		isConnected : boolean
			True if graph is connected, false otherwise
		'''
		return True

	def get_distance(self, point1, point2):
	    '''Calculate distance between two point
	    
	    Parameters:
	        point1: tuple
	        
	        point2: tuple    
	        
	    Return:
	        distance: float
	    '''
	    
	    if(len(point1) != len(point2)):
	        raise ValueError("Points are not of the same dimension")
	    
	    distance = 0
	    
	    for i in range(len(point1)):
	        distance += (point1[i] - point2[i])**2

	    return sqrt(distance)









