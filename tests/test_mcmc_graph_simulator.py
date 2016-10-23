#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mcmc_graph_simulator
----------------------------------

Tests for `mcmc_graph_simulator` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner
import networkx as nx

from mcmc_graph_simulator.mcmc_graph_simulator import *
from mcmc_graph_simulator import cli



class TestMcmc_graph_simulator(unittest.TestCase):

    def setUp(self):
        self.nodes = [(1,2), (3,3), (5,5), (0,0)]
        self.mcmc = mcmc_graph(self.nodes)
        self.g = self.mcmc.current_graph
        pass

    def test__init__(self):
        self.assertTrue(nx.is_connected(self.g))
        for edge in self.g.edges_iter(None, True, True):
            self.assertIsNotNone(edge[2]['weight'])
            self.assertNotEqual(edge[2]['weight'], 0)
        pass

    def test_connectedness(self):
        self.assertTrue(nx.is_connected(self.g))

    def test_distance_calculator(self):
        point1 = (0,0)
        point2 = (3,4)
        self.assertEqual(self.mcmc.get_distance(point1, point2), 5)

        badpoint = (100,0,0)
        with self.assertRaises(ValueError):
            self.mcmc.get_distance(point1, badpoint) #Should raise error for not being in the same dimensions

    def test_bridges(self):
        graph = nx.Graph()

        path1 = [(3,4),(3,3),(3,2),(2,2),(2,3)]
        path2 = [(0,0),(1,1),(4,4)]

        graph.add_path(path1)
        graph.add_path(path2)

        with self.assertRaises(ValueError):
            self.mcmc.get_bridges(graph) #Should raise error since graph is not connected

        graph.add_edge((1,1), (2,2))
        graph.add_edge((2,2), (3,3)) #connect the graph

        bridges = self.mcmc.get_bridges(graph)

        self.assertNotEqual(len(bridges), 0)

    def test_calculate_theta(self):
        graph = nx.Graph()

        graph.add_edge((0,0), (3,4), weight = 5)
        graph.add_edge((3,4), (6,0), weight = 5)
        graph.add_edge((3,4), (0,6), weight = 5)

        theta = self.mcmc.calculate_theta(graph, (0,0), r = 1)
        self.assertEqual(theta, 40)

    def test_mutate_remove(self):
        graph = nx.Graph()

        graph.add_edge((0,0), (0,2), weight = 2)

        with self.assertRaises(ValueError):
            self.mcmc.mutate(graph, False) #Should raise error since all edges are bridges

        graph.add_edge((0,0), (4,0), weight = 4)
        graph.add_edge((4,0), (4,2), weight = 2)
        graph.add_edge((4,2), (0,2), weight = 2)
        graph.add_edge((0,0), (-2,0), weight = 2)

        self.mcmc.mutate(graph, False)

        self.assertEqual(len(graph.edges()), 4)
        self.assertTrue(((0,0), (-2,0)) in graph.edges())

    def test_mutate_add(self):
        graph = nx.Graph()
        graph.add_edge((0,0), (3,0), weight = 3)
        graph.add_edge((0,0), (0,4), weight = 4)

        self.mcmc.mutate(graph, True)

        self.assertTrue(((3,0),(0,4)) in graph.edges()) #Check that only possible edge has been added

        with self.assertRaises(ValueError):
            self.mcmc.mutate(graph, True)

        self.assertTrue(graph[(0,4)][(3,0)]['weight'] == 5) #Check that weight of added edge is correct

    def tearDown(self):
        pass
'''
    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'mcmc_graph_simulator.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output'''