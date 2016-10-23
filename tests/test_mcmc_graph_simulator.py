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


    def tearDown(self):
        pass

    def test_000_something(self):
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