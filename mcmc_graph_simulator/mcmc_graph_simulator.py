# -*- coding: utf-8 -*-
from math import sqrt, e
import networkx as nx
import numpy as np


class Graph:

	adjacency_matrix = []


	def __init__(self, nodes):
		'''
		Creates a new connected networkx Graph with the specified nodes 
	
		Params
		------
		nodes : list of touples
	
		'''
		self.nodes = []
		self.edges = []

		for node in nodes:
			self.nodes.append(node)

		for i in range(len(nodes) - 1):
			self.edges.append((nodes[i], nodes[i+1]))



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









