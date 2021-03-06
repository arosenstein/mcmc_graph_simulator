# -*- coding: utf-8 -*-
from math import sqrt, e
import networkx as nx
import numpy as np
from random import choice, random
import multiprocessing as mp

class mcmc_graph:

	markov_chain = []
	avg_node0_connections = None
	avg_total_edges = None
	avg_longest_shortest_path = None


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
		self.node0 = (0,)*len(nodes[0])
		graph = nx.Graph()

		#graph.add_path(nodes)

		for i in range(len(nodes) - 1):
			graph.add_edge(nodes[i], nodes[i+1], weight = self.get_distance(nodes[i], nodes[i+1]))

		self.markov_chain.append(graph)
		self.current_graph = graph

		self.avg_node0_connections = len(graph[self.node0])
		self.avg_total_edges = len(graph.edges())
		self.avg_longest_shortest_path = self.get_longest_shortest_path(graph, self.node0)

	def get_longest_shortest_path(self, graph, anchor = None):
		'''Calculates the longest dijkstra path in a graph with respect to the anchor node.
		
		Parameter
		-----

			graph: networkx Graph

			anchor: tuple
				node in graph to reference points from


		Return
		-----

			length: float
				Length of the longest shortest path in the graph
		'''
		if(not nx.is_connected(graph)):
			raise ValueError("Graph is not connected")

		if anchor is None:
			anchor = self.node0
		
		d = nx.single_source_dijkstra_path_length(graph, source = anchor, weight = 'weight')

		value = 0
		for item in d:
			value = max(value, d[item])

		return value




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
	    '''Calculates distance between two points
	    
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
	    
	    distance = 0
	    
	    for i in range(len(point1)):
	        distance += (point1[i] - point2[i])**2

	    return sqrt(distance)


	def calculate_theta(self, graph, anchor = None, r = 1):
		'''This function sums the edge weights and all of the shortest paths from an anchor node (node0) to every other node

		Parameters
		-----
			graph: a networkx graph
			
		Return
		-----
			Theta value calculated for the graph
		'''
		
		if anchor is None:
			anchor = self.node0

		sum_of_weights = 0

		for u, v, d in graph.edges(data = True):
			sum_of_weights += d['weight']

		sum_of_paths = 0
		for n in graph.nodes():
			shortest_path = nx.shortest_path(graph, anchor, n, weight = 'weight') #returns a list of the shortest path
			
			#now add up the weights of that path
			for i in range(len(shortest_path) - 1):
				sum_of_paths += graph[shortest_path[i]][shortest_path[i+1]]['weight']

		return r * sum_of_weights + sum_of_paths

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
				else:
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

	def determine_mutation(self, graph):
		'''This function changes the graph, either adding or removing an edge

		Parameters
		-----
			graph: a networkx graph
			
		Return
		-----
			0 if removing edge
			1 if adding edge
		'''

		n = len(graph.nodes())
		e = len(graph.edges())
		max_edges = n * (n - 1) / 2
		min_edges = n - 1

		p = (max_edges - e)/(max_edges - min_edges)

		if random() < p:
			return 1

		else:
			return 0

	def update_mean(self, mean, count, new_value):
		'''This is an online algorithm to calculate the mean of a set of values.
		The value of mean is updated
		
		Parameters
		-----
			mean: float
				the current mean of a set of n values
			
			count: int
				the number of values to calulate the mean

			new_value: float

			
		Return
		-----
			mean: float
				the updated mean value

		'''
		mean = (mean * count + new_value) / (count + 1)
		return mean

	def run(self, iterations):
		'''This is the 'main' function to run the MCMC program. It returns all relevant statistics.
		
		Parameters
		-----
			iterations: int
				the number of iterations to preform the MCMC simulation
			
		Return
		-----
			node0_connections: float
				the expected value of nodes connected to node0

			total_edges: float
				the expected value of the total edges in the graph

			longest_shortest_path: float
				the expected value of the longest shortest path in the graph

			top_1_percent : list
				a list of the  top 1% most occuring graphs in the Markov Chain

		'''

		for i in range(iterations):
			self.predict_next()

		stats = []

		stats.append(self.avg_node0_connections)
		stats.append(self.avg_total_edges)
		stats.append(self.avg_longest_shortest_path)
		stats.append(self.quantile(self.markov_chain))

		return stats

	def quantile(self, graphs, percentile = 99):
		'''Calculates the top 1% most commonly occuring graphs
		
		Parameters
		-----
			graphs: list
				the graphs from MCMC to quantile

			percentile: int, optional
				the percentile above which the most occuring graphs are desired
			
		Return
		-----
			top_1_percent : list
				a list of the  top 1% most occuring graphs in the Markov Chain
		'''

		uniques = {}
		#create dictionary where keys are the graphs, and values are the count

		for graph in graphs:

			if graph not in uniques:
				uniques[graph] = 1

			else:
				uniques[graph] += 1

		#Obtain the graphs in the top desired percentile
		counts = [uniques[k] for k in uniques]
		p = .01 * percentile * len(graphs)
		
		total = len(graphs)
		sorted(counts)

		top_1_counts = []

		while(sum(counts) >= p):
			top_1_counts.append(counts.pop(0))

		top_1_percent = []

		for k, v in uniques.items():
			if v in top_1_counts:
				top_1_percent.append(k)

		return top_1_percent



	def predict_next(self):
		'''This function ties together all other functions, and using the Metropolis-Hastings algorithm, predicts the next graph.

		It performs the following steps:
			1. Creates a new proposed graph by changing the state of one of the edges of the current graph
			2. Calculates the Metropolis-Hastings acceptance probability
			3. Generates a random number from 0 to 1
			4. Determines whether or not to accept proposed graph
			
		Return
		-----
			Mutated graph
		'''

		graph = self.current_graph

		#create a new object for the proposed graph, and copy current graph
		proposed_graph = nx.Graph()
		proposed_graph.add_edges_from(graph.edges(data = True))

		#mutate proposed graph
		self.mutate(proposed_graph, self.determine_mutation(proposed_graph) == 1)

		#calculate f(X_i, X_j)
		anchor = graph.nodes()[0]
		theta_i = self.calculate_theta(graph, anchor, self.r)
		theta_j = self.calculate_theta(proposed_graph, anchor, self.r)

		f_xi_xj = e**(-(theta_i - theta_j)/self.T)

		n = len(graph.nodes())
		q_i_j = 1 / (n * (n - 1) / 2 - len(self.get_bridges(graph)))
		q_j_i = 1 / (n * (n - 1) / 2 - len(self.get_bridges(proposed_graph)))

		#Calculated Metropolis-Hastings acceptance probability
		a_ij = min(f_xi_xj * q_i_j / q_j_i, 1)

		U = random()

		accepted_graph = None

		if (U <= a_ij):
			#accept proposed graph
			self.markov_chain.append(proposed_graph)
			self.current_graph = proposed_graph
			accepted_graph = self.current_graph

		else:
			#reject proposed graph
			self.markov_chain.append(graph)
			accepted_graph = graph

		#update statistics

		count = len(self.markov_chain) - 1

		self.update_mean(self.avg_node0_connections, count, len(accepted_graph[self.node0]))

		self.update_mean(self.avg_total_edges, count, len(accepted_graph.edges()))
		
		ls_path = self.get_longest_shortest_path(accepted_graph, self.node0)
		self.update_mean(self.avg_longest_shortest_path, count, ls_path)

		return accepted_graph


class parallel_mcmc:
	'''Runs multiple mcmc simulations in parallel'''

	def __init__(self, nodes, r = 1, T = 1):
		self.nodes = nodes
		self.r = r
		self.T = T

	def run(self, iterations):
		#Run n simulations each with the number of iterations specified in parallel, and average the result statistics
		#Returns the same statistics as mcmc_graph class, just averaged out over all parallel processes
		iterations = 10
		count = mp.cpu_count()

		params = [iterations]*count
		p = mp.Pool()
		result = p.map(self._run, params)
		p.close()
		
		avg_node0_connections = []
		avg_total_edges = []
		avg_longest_shortest_path = []
		
		for r in result:
			avg_node0_connections.append(r[0])
			avg_total_edges.append(r[1])
			avg_longest_shortest_path.append(r[2])

		return np.mean(avg_node0_connections), np.mean(avg_total_edges), np.mean(avg_longest_shortest_path)


	def _run(self, iterations):
		mcmc = mcmc_graph(self.nodes, self.r, self.T)
		return mcmc.run(iterations)

