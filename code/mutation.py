"""COMP6202 - Evolution of Complexity
Holds mutation class for mutating an individual.
"""

__authors__ = "David Jones <dsj1n15@ecs.soton.ac.uk>"

import copy
import random

from representation import Individual


class Mutator:
    def __init__(self, mutation_rate: float = 0.005, bit_flip: bool = False):
        self.mutation_rate = mutation_rate
        self.bit_flip = bit_flip

    def mutate(self, i: Individual, inplace: bool = False) -> Individual:
        if not inplace:
            i = copy.deepcopy(i)
        for t in i.traits:
            set_bits = t.value
            unset_bits = t.total_bits - set_bits
            t.value = 0
            for b in range(set_bits):
                t.value += self._mutate_bit(1)
            for b in range(unset_bits):
                t.value += self._mutate_bit(0)
        return i

    def _mutate_bit(self, bit_value: int) -> int:
        if random.uniform(0, 1) > self.mutation_rate:
            # No mutation
            return bit_value
        # Return new bit value
        if self.bit_flip:
            return not bit_value
        else:
            return random.choice([0, 1])
