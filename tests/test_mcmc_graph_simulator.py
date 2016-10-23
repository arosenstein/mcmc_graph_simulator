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

from mcmc_graph_simulator.mcmc_graph_simulator import *
from mcmc_graph_simulator import cli



class TestMcmc_graph_simulator(unittest.TestCase):

    def setUp(self):
        self.nodes = [(1,2), (3,3), (5,5), (0,0)]
        self.g = Graph(self.nodes)
        pass

    def test__init__(self):
        self.assertEqual(len(self.g.nodes), len(self.nodes)) #Graph should have all of the nodes inserted
        self.assertEqual(len(self.g.edges), len(self.nodes) - 1)  #Graph should have n - 1 edges

    def test_connectedness(self):
        self.assertTrue(self.g.isConnected())

    def test_distance_calculator(self):
        point1 = (0,0)
        point2 = (3,4)
        self.assertEqual(self.g.get_distance(point1, point2), 5)

        badpoint = (100,0,0)
        with self.assertRaises(ValueError):
            self.g.get_distance(point1, badpoint)


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