import random

from typing import List


class Selector:
    def __init__(self, bias: int = 0.000001):
        self.bias = bias

    def select(self, fs: List[int], k: int = None) -> List[int]:
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
