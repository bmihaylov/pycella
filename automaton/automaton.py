from collections import deque
from itertools import chain
from math import sqrt
import sys


class CA:
    def __init__(self, buff, rules, empty_cell, bounded=True):
        self._width = len(buff[0]) + 2
        self._height = len(buff) + 2

        first_row = list(empty_cell() for _ in range(self._width))
        middle_rows = [[empty_cell()] + row + [empty_cell()] for row in buff]
        last_row = list(empty_cell() for _ in range(self._width))
        self._buffer = [first_row] + middle_rows + [last_row]

        self._rules = rules
        self._empty_cell = empty_cell
        self._bounded = bounded
        self._generation = 0
        self._proxy = CA.Proxy(self)

    def __getitem__(self, coords):
        return self._buffer[coords[0]][coords[1]]

    def __iter__(self):
        for i in range(1, self._height-1):
            for j in range(1, self._width-1):
                yield self._buffer[i][j]

    @property
    def width(self):
        """
        :returns: the effective width of the buffer
        """
        return self._width - 2

    @property
    def height(self):
        """
        :returns: the effective height of the buffer
        """
        return self._height - 2

    def _boundary_check(self):
        """
        :returns: True iff there is a a non empty cell at any of the boundaries
        """
        buff = self._buffer
        for i in range(1, self._width-1):
            if buff[1][i] != self._empty_cell():
                return True
            if buff[self._height-2][i] != self._empty_cell():
                return True
        for i in range(1, self._height-1):
            if buff[i][1] != self._empty_cell():
                return True
            if buff[i][self._width-2] != self._empty_cell():
                return True
        return False

    def _expand(self, factor=2):
        """
        Create a roughly two times larger buffer and
        copy and current buffer in the center of the new one
        """
        factor = sqrt(factor)
        width = self._width - 2
        height = self._height - 2
        new_width = int(width*factor + 2)
        new_height = int(height*factor + 2)
        new_buffer = [[self._empty_cell() for i in range(new_width)]
                      for j in range(new_height)]
        h_margin = int((new_height - height) / 2)
        w_margin = int((new_width - width) / 2)
        for i in range(height):
            for j in range(width):
                new_buffer[h_margin+i][w_margin+j] = self._buffer[1+i][1+j]
        self._buffer = new_buffer
        self._width = new_width
        self._height = new_height

    def step(self):
        """
        Apply the rules to every cell in the buffer.
        Equivalent to placing the new cells in a new buffer.
        """
        if not self._bounded and self._boundary_check():
            self._expand()

        width = self._width
        height = self._height
        update_buffer = deque()
        self._generation += 1

        #get a head start with the first two rows
        #the proxy starts from (1, 1)
        for i in range(1, 3):
            for j in range(1, width-1):
                update_buffer.append(self._apply_rules(self._proxy))
                self._proxy.move()
        #update cells at a safe distance from the read position
        #and push new updates in the update_buffer
        for i in range(1, height-3):
            for j in range(1, width-1):
                self._buffer[i][j] = update_buffer.popleft()
                update_buffer.append(self._apply_rules(self._proxy))
                self._proxy.move()
        #push the updates left in the update_buffer
        for i in range(height-3, height-1):
            for j in range(1, width-1):
                self._buffer[i][j] = update_buffer.popleft()
        self._proxy._reset()

    def _apply_rules(self, proxy):
        """
        :returns: a new cell that is the result of applying
            the rules to the cell pointed to by the proxy at 
            that moment
        """
        
        return self._rules(proxy)

    class Proxy:
        """
        An iterator that provides read access to a current cell and it's
        neighbors to the external rules function.
        """
        def __init__(self, CA):
            self._ca = CA
            self._i = 1
            self._j = 1

        def __getitem__(self, deltas):
            if abs(deltas[1]) > 1 or abs(deltas[0]) > 1:
                raise IndexError
            return self._ca[self._i + deltas[0], self._j + deltas[1]]

        def move(self):
            """
            Moves one position forward in the two dimensional buffer.
            Changes rows automaticaly.
            """
            self._j += 1
            j_is_too_large = self._j + 1 >= self._ca._width
            if j_is_too_large:
                self._j = 1
            self._i += j_is_too_large
            if self._i + 1 > self._ca._height:
                raise IndexError

        def _reset(self):
            self._i = 1
            self._j = 1

        @property
        def neighbors(self):
            """
            :returns: a list of all the neighbor cells of the current position
            """
            i = self._i
            j = self._j
            ca = self._ca
            return [ca[i-1, j-1], ca[i-1, j], ca[i-1, j+1],
                    ca[i, j-1], ca[i, j+1],
                    ca[i+1, j-1], ca[i+1, j], ca[i+1, j+1]]
