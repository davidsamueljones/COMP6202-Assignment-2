"""COMP6202 - Evolution of Complexity
Holds subjective scoring classes: Scorer, F0Scorer.
"""

__authors__ = "David Jones <dsj1n15@ecs.soton.ac.uk>"

import operator
import random

from typing import List
from representation import Population, Individual


class Scorer:
    """Scorer that implements `score2` and `score3`.
    """

    def __init__(self, sample_size: int = 15, intransitive: bool = False):
        if intransitive:
            self.op = operator.lt
        else:
            self.op = operator.gt
        self.sample_size = sample_size

    def score(self, a: Individual, b: Individual) -> int:
        a = a.values
        b = b.values
        mi = 0
        for (i, (ta, tb)) in enumerate(zip(a, b)):
            delta = abs(tb - ta)
            if self.op(delta, abs(a[mi] - b[mi])):
                mi = i
        return Scorer._score(a[mi], b[mi])

    @staticmethod
    def _score(a: int, b: int) -> int:
        return 1 if a > b else 0

    def subj_fitness(self, a: Individual, pop: Population) -> List[int]:
        """Calculate the subjective fitness for an individual using an
        opponent population.

        Args:
            a (Individual): The individual to score against the opponents.
            pop (Population): The population to select opponents from.

        Returns:
            List[int]: The individual score against each selected individual
                in the population. This will be a list of length sample size.
        """
        if len(pop) == 0:
            return []
        # Allow repeats, same as applet
        pop = random.choices(pop, k=self.sample_size)
        return list(map(lambda b: self.score(a, b), pop))


class F0Scorer(Scorer):
    """Scorer that always returns 0 for subjective score (Experiment 0).
    """

    def subj_fitness(self, *args) -> int:
        return 0
