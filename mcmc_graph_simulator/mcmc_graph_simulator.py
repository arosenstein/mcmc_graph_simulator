# -*- coding: utf-8 -*-
from math import sqrt, e
import networkx as nx
import numpy as np
from random import choice


class mcmc_graph:

	markov_chain = []


	def __init__(self, nodes, r = 1, T = 1):
		'''
		Creates a new connected networkx Graph with the specified nodes 
	
		Params
		------
		nodes : list of touples

		r : float
		T : float
			-both constants in the MCMC equations
	
		'''

		self.r = r
		self.T = T
		self.markov_chain = []
		self.node0 = nodes[0]
		graph = nx.Graph()

		#graph.add_path(nodes)

		for i in range(len(nodes) - 1):
			graph.add_edge(nodes[i], nodes[i+1], weight = self.get_distance(nodes[i], nodes[i+1]))

		self.markov_chain.append(graph)
		self.current_graph = graph


	def get_bridges(self, graph):
		'''Calculates number of bridges in a graph by removing an edge, and seeing if the graph is still connected.
		
		Parameter
		-----

			graph: networkx Graph

		Return
		-----

			bridges: list
				List of edges that are bridges
		'''

		if(not nx.is_connected(graph)):
			raise ValueError("Graph is not connected")
			return

		bridges = []

		for u, v, d in graph.edges(data = True):
			#remove edge
			graph.remove_edge(u, v)

			#check if graph is connected
			if(not nx.is_connected(graph)):
				bridges.append((u,v))

			#add edge back into graph
			if d != {}:
				graph.add_edge(u,v, weight = d['weight'])
			else:
				graph.add_edge(u,v)

		return bridges


	def get_distance(self, point1, point2):
	    '''Calculate distance between two point
	    
	    Parameters
	    -----
	        point1: tuple
	        
	        point2: tuple    
	        
	    Return
	    -----
	        distance: float
	    '''
	    
	    if(len(point1) != len(point2)):
	        raise ValueError("Points are not of the same dimension")
	        return
	    
	    distance = 0
	    
	    for i in range(len(point1)):
	        distance += (point1[i] - point2[i])**2

	    return sqrt(distance)


	def calculate_theta(self, graph, anchor, r = 1):
		'''This function sums the edge weights and all of the shortest paths from an anchor node (node0) to every other node

		Parameters
		-----
			graph: a networkx graph
			
		Return
		-----
			Theta value calculated for the graph
		'''
		
		sum_of_weights = 0

		for u, v, d in graph.edges(data = True):
			sum_of_weights += d['weight']

		sum_of_paths = 0
		for n in graph.nodes():
			shortest_path = nx.shortest_path(graph, anchor, n, weight = 'weight') #returns a list of the shortest path
			
			#now add up the weights of that path
			for i in range(len(shortest_path) - 1):
				sum_of_paths += graph[shortest_path[i]][shortest_path[i+1]]['weight']

		return self.r * sum_of_weights + sum_of_paths

	def mutate(self, graph, add = True):
		'''This function changes the graph, either adding or removing an edge

		Parameters
		-----
			graph: a networkx graph

			add: boolean
				True to add an edge, false to remove one
			
		Return
		-----
			Mutated graph
		'''

		if(add):
			#select random nodes
			node1 = choice(graph.nodes())
			node2 = choice(graph.nodes())

			#throw error if graph cannot have any more edges
			number_of_nodes = len(graph.nodes())
			if(len(graph.edges()) == number_of_nodes * (number_of_nodes - 1)/2):
				raise ValueError('Cannot add unique edge to complete graph')

			while(node1 == node2 or node2 in graph[node1]):
				#loop until edge is selected that is not yet in graph
				if(len(graph[node1]) + 1 == len(graph.nodes())):
					#select a different node for node1 if it is connected to every other node
					node1 = choice(graph.nodes())
				node2 = choice(graph.nodes())

			graph.add_edge(node1, node2, weight = self.get_distance(node1, node2))

			return graph

		else:
			bridges = self.get_bridges(graph)

			if(len(bridges) == len(graph.edges())):
				raise ValueError('Cannot remove edge and keep graph connected')

			u, v = choice(graph.edges())
			while((u,v) in bridges):
				u, v = choice(graph.edges())

			graph.remove_edge(u,v)

			return graph






