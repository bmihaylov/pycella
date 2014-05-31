import unittest
from operator import getitem
from random import randint

from pycella.automaton.automaton import CA
from pycella.automaton.rules import life_rules, seeds_rules


class TestProxy(unittest.TestCase):
    def setUp(self):
        self.size = 10
        buff = [list(range(10*i, 10*(i+1))) for i in range(10)]
        self.ca = CA(buff, life_rules, lambda: 0)
        self.proxy = self.ca._proxy

    def test_indexing(self):
        self.assertRaises(IndexError, lambda: getitem(self.proxy, (10, 0)))
        self.assertRaises(IndexError, lambda: getitem(self.proxy, (0, -10)))
        # this is for independance from move correctness
        self.proxy._i = 2
        self.proxy._j = 2
        print(self.proxy[0, 0])
        for i in range(-1, 2):
            self.assertEqual(1+i, self.proxy[-1, i])
            self.assertEqual(self.size+1+i, self.proxy[0, i])
            self.assertEqual(2*self.size+1+i, getitem(self.proxy, (1, i)))

    def test_move(self):
        for i in range(10):
            self.proxy._reset()
            steps = randint(0, self.size**2-1)
            for j in range(steps):
                self.proxy.move()
            self.assertEqual(steps, self.proxy[0, 0])

    def test_neighbors_in_middle(self):
        for i in range(10):
            self.proxy._reset()
            i = randint(1, self.size-2)
            j = randint(1, self.size-2)
            self.proxy._i = 1 + i
            self.proxy._j = 1 + j
            size = self.size
            expected_neighbors = list(range((i-1)*size+j-1, (i-1)*size+j+2)) +\
                                 [i*size + j-1, i*size + j+1] +\
                                 list(range((i+1)*size+j-1, (i+1)*size+j+2))
            self.assertEqual(expected_neighbors, self.proxy.neighbors)

    def test_neighbors_in_outer_ring(self):
        for i in range(10):
            self.proxy._reset()
            offset = randint(0, self.size-1)
            # test first row
            self.proxy._i, self.proxy._j = 1, 1+offset
            self.assertEqual([0, 0, 0], self.proxy.neighbors[:3])
            # test last row
            self.proxy._i, self.proxy._j = self.size, 1+offset
            self.assertEqual([0, 0, 0], self.proxy.neighbors[-3:])
            # test first column
            self.proxy._i, self.proxy._j = 1+offset, 1
            left_neighbors = [self.proxy.neighbors[j] for j in [0, 3, 5]]
            self.assertEqual([0, 0, 0], left_neighbors)
            # test last column
            self.proxy._i, self.proxy._j = 1+offset, self.size
            right_neighbors = [self.proxy.neighbors[j] for j in [2, 4, 7]]
            self.assertEqual([0, 0, 0], left_neighbors)
