from __future__ import annotations

"""COMP6202 - Evolution of Complexity

Holds individual representation and population holder.
"""

from collections import UserList
from typing import List, Tuple


class Generator:
    def __init__(self, trait_bits: int, trait_count: int):
        self.trait_bits = trait_bits
        self.trait_count = trait_count

    def individual(self, value: int) -> Individual:
        traits = []
        for i in range(self.trait_count):
            traits += [Trait(value, self.trait_bits)]
        return Individual(traits)

    def population(self, n: int, value: int) -> Population:
        return Population([self.individual(value)] * n)


class Population(UserList):
    """ Populations are just lists of individuals.
    """

    def __init__(self, elements: List[Individual] = [], **kwargs):
        super().__init__(elements, **kwargs)


class Individual:
    def __init__(self, traits: List[Trait]):
        """[summary]

        Args:
            traits (List[Trait]): [description]
        """
        self.traits = traits

    @property
    def values(self) -> Tuple[int]:
        return tuple(map(lambda x: x.value, self.traits))

    @property
    def value(self) -> int:
        return sum(self.values)

    @property
    def total_bits_by_trait(self) -> Tuple[int]:
        return tuple(map(lambda x: x.total_bits, self.traits))

    @property
    def total_bits(self) -> int:
        return sum(self.total_bits_by_trait)

    def as_bits(self):
        bits = []
        for t in self.traits:
            bits += t.as_bits()
        return bits

    def __repr__(self) -> str:
        return str(self.traits)


class Trait:
    def __init__(self, value: int, total_bits: int):
        """Each trait's bitstring represented by their unitations i.e.
        the number of set bits. The total number of bits must be tracked.

        Args:
            value (int): Number of set bits.
            total_bits (int): Total number of bits in the trait.
        """
        if value > total_bits or value < 0:
            raise ValueError("Value > total_bits or < 0")
        self._value = value
        self.total_bits = total_bits

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = max(0, min(value, self.total_bits))

    def as_bits(self):
        return [1] * self.value + [0] * (self.total_bits - self.value)

    def __repr__(self) -> str:
        return str(self.value)
