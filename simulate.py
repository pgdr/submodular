#!/usr/bin/env python3
# COPYRIGHT PER AUSTRIN 2021

import random


from functools import cache

SIM_COUNTER = 0


@cache
def simulate(C, width=200, height=100, ITERS=1 << 9):
    global SIM_COUNTER
    SIM_COUNTER += 1

    area = width * height
    hits = 0
    for _ in range(ITERS):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        hits += any(
            (x - t.center.x) ** 2 + (y - t.center.y) ** 2 <= t.radius**2 for t in C
        )

    return round(100 * (hits / ITERS), 2)
