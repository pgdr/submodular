from collections import namedtuple as T
import random
import math
import heapq
from itertools import chain, combinations

import simulate

SEED = random.randint(10**6, 10**7)
print(f"{SEED=}")
random.seed(SEED)
calculate = simulate.simulate

Tiltak = T("Tiltak", "radius center cost")


def tiltak_str(self):
    return f"({self.cost} kr, {self.radius})"


Tiltak.__repr__ = tiltak_str

FS = frozenset

Point = T("Point", "x y")
N = 13
THRESHOLD = 80


def generate(width=200, height=100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    radius = random.randint(5, min(width, height) * 0.6)
    cost = max(1, ((random.random() + 0.5) * radius**2) // 10)
    return Tiltak(radius, Point(x, y), cost)


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def cost(S):
    return sum(s.cost for s in S)


def derivative(e, S):
    Se = S | {e}
    return round(calculate(Se) - calculate(S), 1)


def cost_derivative(e, S):
    Se = S | {e}
    return round((calculate(Se) - calculate(S)) / e.cost, 3)


def pop(Q, S):
    if not Q:
        raise ValueError("Empty queue")
    if len(Q) == 1:
        return heapq.heappop(Q)[1]

    while True:
        d, e = heapq.heappop(Q)
        d_next, e_next = heapq.heappop(Q)
        d_new = -cost_derivative(e, S)
        if d_new <= d_next:
            heapq.heappush(Q, (d_next, e_next))
            return e
        else:
            heapq.heappush(Q, (d_next, e_next))
            heapq.heappush(Q, (d_new, e))

    d_next, e_next = heapq.heappop(Q)
    return e


C = []
for i in range(N):
    C.append(generate())

# Greedy PQ strategy

S = FS()
Q = [(-cost_derivative(e, S), e) for e in C]
heapq.heapify(Q)
while calculate(S) < THRESHOLD and Q:
    print("=>", Q, S)
    e = pop(Q, S)
    print(e, S)
    S |= {e}


GREEDY_S = S
GREEDY_SCORE = calculate(S)
GREEDY_COST = cost(S)

print("\n\n\n=== SOLUTION ===\n")
print("len  :", len(S))
print("S    :", S)
print("score:", calculate(S))
print("cost :", cost(S))
print("evals:", simulate.SIM_COUNTER)

print("\n\n\n=== Exact brute force ===\n\n")

n = 0
current_best_cost = 10**10
for S in powerset(C):
    if len(S) > n:
        n = len(S)
        print("...", n)
    c = cost(S)
    score = calculate(S)
    if score >= THRESHOLD and c < current_best_cost:
        print("score", score)
        print("cost", c)
        current_best_cost = c
        print("len", len(S))
        break

print("evals:", simulate.SIM_COUNTER)
if GREEDY_COST < current_best_cost:
    print(f"Greedy won: {GREEDY_COST} < {current_best_cost}")
else:
    ratio = round((GREEDY_COST / current_best_cost - 1) * 100, 3)
    print("Cost ratio:", ratio, "% appx")
print(f"{SEED=}")
