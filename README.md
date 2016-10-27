#mcmc_graph_simulator


[![Documentation Status](https://readthedocs.org/projects/mcmc-graph-simulator/badge/?version=latest)](http://mcmc-graph-simulator.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/arosenstein/mcmc_graph_simulator/shield.svg)](https://pyup.io/repos/github/arosenstein/mcmc_graph_simulator/)
[![Build Status - Master](https://travis-ci.org/arosenstein/mcmc_graph_simulator.svg?branch=master)](https://travis-ci.org/arosenstein/mcmc_graph_simulator)
[![Build Status - Develop](https://travis-ci.org/arosenstein/mcmc_graph_simulator.svg?branch=develop)](https://travis-ci.org/arosenstein/mcmc_graph_simulator)
[![Coverage Status](https://coveralls.io/repos/github/arosenstein/mcmc_graph_simulator/badge.svg?branch=master)](https://coveralls.io/github/arosenstein/mcmc_graph_simulator?branch=master)


This is a Markov-Chain Monte Carlo (MCMC) simulator for evaluating graphs using python.

* Documentation: https://mcmc-graph-simulator.readthedocs.io.


##Features

* Using MCMC graph structures are predicted using relative probabilities.

* This is achieved using the [Metropolis-Hastings](https://en.wikipedia.org/wiki/Metropolis–Hastings_algorithm) algorithm

* Implementation of an online expected value calculation algorithm

* Gives examples of the top 1% of graphs in the stationary distribution

* Calculates expected maximum dijkstra path in each graph in the Markov Chain

##Running the Code

There are two main steps for a user to run the simulation.

1. Construct an instance of the mcmc_graph object by passing a list of graph verticies (2-D cartesian coordinates), r, and T (temperature) parameters
    
    ```python
    nodes = [(0,0), (0,2), (0,4), (22, 100), (-4, 4)]
    r = 0.3
    T = 2
    mcmc = mcmc_graph(nodes, r, T)
    ```

2. Run the simulation using the desired number of timesteps

	```python
	timesteps = 10000
	stats = mcmc.run(timesteps)
	```

3. A list `stats` is returned. It contains the following information

	* The expected value of nodes connected to node0

	* The expected value of the total edges in the graph

	* The expected value of the longest shortest path in the graph

	* A list of the  top 1% most occuring graphs in the Markov Chain

For specific information on how the calculations are performed, please refer to the appropriate docstring

##Unit Testing

In order to run the unit tests, execute:
	
	$ python setup.py test

The unit tests achieve 100% code coverage.

##TODO

Expand simulation to cover n-dimensional coordinate systems

* This has already been mostly achieved, it is however not yet fully covered in the testing. Most of the current methods are generalized for n-dimensional systems

* Add an option for the user to observe the graphs generated

Credits & License
---------

* Free software: MIT license


This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter-pypackage) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.

