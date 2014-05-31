import unittest
from itertools import chain
from operator import getitem
from random import randint

from pycella.automaton.automaton import CA
from pycella.automaton.rules import life_rules, seeds_rules


class TestAutomaton(unittest.TestCase):
    def setUp(self):
            self.MAX = 100
            self.empty_cell = lambda: 0

    def test_creation(self):
        buff = [[0, 0, 1],
                [1, 1, 0],
                [0, 1, 0]]
        ca = CA(buff, life_rules, self.empty_cell)
        expected_buffer = [[0, 0, 0, 0, 0],
                           [0, 0, 0, 1, 0],
                           [0, 1, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 0]]
        self.assertEqual(expected_buffer, ca._buffer)

    def test_indexing(self):
        buff = [[0, 0, 0],
                [0, 0, 1],
                [0, 0, 19]]
        ca = CA(buff, seeds_rules, self.empty_cell)
        self.assertEqual(1, ca[2, 3])
        self.assertEqual(19, ca[3, 3])
        self.assertRaises(IndexError, lambda i: getitem(ca, i), (19, 0))

    def test_iteration(self):
        buff = [list(range(5*i, 5*i + 5)) for i in range(7)]
        ca = CA(buff, life_rules, self.empty_cell)
        expected_content = list(chain(*buff))
        content = []
        for cell in ca:
            content.append(cell)
        self.assertEqual(expected_content, content)

    def test_equality(self):
        width = randint(1, self.MAX)
        height = randint(1, self.MAX)
        buff = [[randint(0, self.MAX) for i in range(width)]
                for j in range(height)]
        first = CA(buff, seeds_rules, self.empty_cell)
        second = CA(buff, seeds_rules, self.empty_cell)
        internal_buffer = [[0]*(width + 2)] +\
                          [[0] + line + [0] for line in buff] +\
                          [[0]*(width + 2)]
        second._buffer = internal_buffer
        self.assertTrue(first == second)

    def test_dimensions(self):
        for i in range(10):
            width = randint(1, self.MAX)
            height = randint(1, self.MAX)
            buff = [list(range(width)) for _ in range(height)]
            ca = CA(buff, seeds_rules, self.empty_cell)
            self.assertEqual(width, ca.width)
            self.assertEqual(height, ca.height)

    def test_boundary_check(self):
        for i in range(10):
            width = randint(1, self.MAX)
            height = randint(1, self.MAX)
            buff = [[0] * width for _ in range(height)]

            ca = CA(buff, life_rules, self.empty_cell)
            self.assertFalse(ca._boundary_check())

            column = randint(0, width-1)
            buff[height-1][column] = 1
            ca = CA(buff, life_rules, self.empty_cell)
            self.assertTrue(ca._boundary_check())

            buff[height-1][column] = 0
            row = randint(0, height-1)
            buff[row][width-1] = 1
            ca = CA(buff, life_rules, self.empty_cell)
            self.assertTrue(ca._boundary_check())

    def test_expand(self):
        for i in range(10):
            width = randint(1, self.MAX)
            height = randint(1, self.MAX)
            buff = [[0] * width for _ in range(height)]
            ca = CA(buff, seeds_rules, self.empty_cell)
            ca._expand()
            self.assertGreater(ca.width, width)
            self.assertGreater(ca.height, height)

    def test_step_with_life_1(self):
        initial_state = [[0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]
        before = CA(initial_state, life_rules, self.empty_cell)
        after = CA(initial_state, life_rules, self.empty_cell)
        after.step()
        self.assertEqual(before, after)

    def test_step_with_life_2(self):
        initial_state = [[0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0],
                         [0, 1, 1, 1, 0],
                         [0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0]]

        expected_state = [[0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0]]
        calculated_ca = CA(initial_state, life_rules, self.empty_cell)
        calculated_ca.step()
        expected_ca = CA(expected_state, life_rules, self.empty_cell)
        self.assertEqual(calculated_ca, expected_ca)

    def test_step_with_life_3(self):
        initial_state = [[0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 1, 1, 0, 0],
                         [0, 0, 1, 0, 1, 0, 0],
                         [0, 0, 1, 1, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0]]

        expected_state = [[0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 1, 0, 1, 0, 0],
                          [0, 1, 0, 0, 0, 1, 0],
                          [0, 0, 1, 0, 1, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0]]
        calculated_ca = CA(initial_state, life_rules, self.empty_cell)
        calculated_ca.step()
        expected_ca = CA(expected_state, life_rules, self.empty_cell)
        self.assertEqual(calculated_ca, expected_ca)

    def test_step_with_life_4(self):
        initial_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        expected_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        calculated_ca = CA(initial_state, life_rules, self.empty_cell)
        calculated_ca.step()
        expected_ca = CA(expected_state, life_rules, self.empty_cell)
        self.assertEqual(calculated_ca, expected_ca)

    def test_step_with_life_5(self):
        initial_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        expected_state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                          [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        calculated_ca = CA(initial_state, life_rules, self.empty_cell)
        for i in range(4):
            calculated_ca.step()
        expected_ca = CA(expected_state, life_rules, self.empty_cell)
        self.assertEqual(calculated_ca, expected_ca)

    def test_step_with_seeds_1(self):
        initial_state = [[0, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 0]]

        expected_state = [[0, 0, 0, 0],
                          [0, 0, 1, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 0]]
        calculated_ca = CA(initial_state, seeds_rules, self.empty_cell)
        calculated_ca.step()
        expected_ca = CA(expected_state, seeds_rules, self.empty_cell)
        self.assertEqual(calculated_ca, expected_ca)

    def test_step_with_seeds_2(self):
        initial_state = [[0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 1, 0, 0],
                         [0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 0]]

        expected_state = [[0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 1, 0, 0],
                          [0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0]]
        calculated_ca = CA(initial_state, seeds_rules, self.empty_cell)
        calculated_ca.step()
        expected_ca = CA(expected_state, seeds_rules, self.empty_cell)
        self.assertEqual(calculated_ca, expected_ca)



