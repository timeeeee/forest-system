"""
graph average tree growth through many generations, across growth and lightning rates!

does a higher lightning rate move the peak significantly towards a lower growth rate?
Does the size of the board matter?
In higher dimensions (2nd, 3rd... 4th?!) is the peak noticeably sharper?
How is it different including/excluding diagonal neighbors?
one full round is trees grow, lightning kills contiguous groups.
What does the graph of a forest over time look like?
  will populations tend to build up and die off at a regular frequency?
How to model this as a system? How well can the corresponding mathematical model approximate it?

todo: make forest use an arbitrary number of dimensions
"""

from itertools import product
from random import random

from flood_fill import flood_fill


class Forest(object):
    def __init__(self, shape, growth_rate=.1, lightning_rate=.01):
        self.width = shape[0]
        self.height = shape[1]
        self.grid = [
            [0 for _ in range(self.width)] for _ in range(self.height)]

        self.growth_rate = growth_rate
        self.lightning_rate = lightning_rate

    def step(self):
        """Grow trees, kill off some with lightning."""
        self.grow()
        self.lightning()

    def grow(self, growth_rate=None):
        """Add new trees according to growth rate"""
        if growth_rate is None:
            growth_rate = self.growth_rate
        for row in range(self.height):
            for col in range(self.width):
                if random() < growth_rate:
                    self.grid[row][col] = 1

    def lightning(self, lightning_rate=None):
        """Strike some trees with lightning and burn any contiguous ones"""
        if lightning_rate is None:
            lightning_rate = self.lightning_rate
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == 1 and random() < lightning_rate:
                    flood_fill(self.grid, (row, col), 0)

    def __str__(self):
        return "\n".join(
            "".join("T" if tree else "." for tree in row) for row in self.grid)

    def count(self):
        return sum(sum(row) for row in self.grid)


generations = 1000
for growth_rate in [.1 * n for n in range(1, 10)]:
    for lightning_rate in [.01 * n for n in range(1, 11)]:
        forest = Forest((10, 10), growth_rate, lightning_rate)
        total_production = 0
        for _ in range(generations):
            forest.step()
            total_production += forest.count()
        print "growth rate {}, lightning rate {}:".format(
            growth_rate, lightning_rate)
        print "    average production = {}".format(
            float(total_production) / generations)
