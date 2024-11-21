from collections import namedtuple as T
import random
import math

from itertools import chain, combinations

import simulate


Tiltak = T("Tiltak", "radius center cost")
FS = frozenset

Point = T("Point", "x y")


def generate(width=200, height=100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    radius = random.randint(1, int(math.hypot(width, height)))
    cost = ((random.random() + 0.5) * radius**2) // 10
    return Tiltak(radius, Point(x, y), cost)


C = []
for i in range(10):
    C.append(generate())


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


for idx, S in enumerate(powerset(C)):
    S = FS(S)
    print(idx, S, simulate.simulate(S))
