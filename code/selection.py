"""COMP6202 - Evolution of Complexity

Holds different selection classes.
"""

__authors__ = "David Jones <dsj1n15@ecs.soton.ac.uk>"

import random
import numpy as np

from typing import List

DEFAULT_BIAS = 0.000001


class Selector:
    def select(self, fs: List[float], k: int = None) -> List[int]:
        pass


class FitnessProportionateSelection(Selector):
    def __init__(self, bias: float = DEFAULT_BIAS):
        self.bias = bias

    def select(self, fs: List[float], k: int = None) -> List[int]:
        if not k:
            k = len(fs)
        # Make wheel
        total = 0
        wheel = []
        for f in fs:
            total += f + self.bias
            wheel += [total]
        # Spin wheel
        selected = []
        for s in range(k):
            i = 0
            pick = random.random() * total
            while wheel[i] < pick:
                i += 1
            selected += [i]
        return selected


class StochasticUniversalSampling(Selector):
    def __init__(self, bias: float = DEFAULT_BIAS):
        self.bias = bias

    def select(self, fs: List[float], k: int = None) -> List[int]:
        if not k:
            k = len(fs)

        # Make wheel
        total = 0
        wheel = []
        for f in fs:
            total += f + self.bias
            wheel += [total]
        # Make pointers
        dist = total / k
        start = random.random() * dist
        pointers = [start + i * dist for i in range(k)]
        # Select
        selected = []
        for p in pointers:
            i = 0
            while wheel[i] < p:
                i += 1
            selected += [i]
        return selected


class TournamentSelection(Selector):
    def __init__(self, n: int):
        self.n = n

    def select(self, fs: List[float], k: int = None) -> List[int]:
        if not k:
            k = len(fs)
        selected = []
        for s in range(k):
            tournament = random.choices(list(enumerate(fs)), k=self.n)
            winner = max(tournament, key=lambda x: x[1])
            selected += [winner[0]]
        return selected


class VirulenceSelector(Selector):
    def __init__(self, selector: Selector, lamb: float, normalise: bool = True):
        self.selector = selector
        self.do_normalise = normalise
        self.lamb = lamb

    def select(self, fs: List[float], k: int = None) -> List[int]:
        fs = np.array(fs)
        if self.do_normalise:
            fs = VirulenceSelector.normalise(fs)
        la = self.lamb
        fs = 2 * fs / la - np.square(fs) / (la * la)
        # Use base selection scheme
        return self.selector.select(fs, k)

    @staticmethod
    def normalise(vals: List[float]):
        mi = min(vals)
        vals = vals - mi
        mx = max(vals)
        if mx > 0:
            vals = vals / mx
        return vals
