from __future__ import annotations

"""COMP6202 - Evolution of Complexity
Holds main execution class [Coevolution] for running a GA.
"""

__authors__ = "David Jones <dsj1n15@ecs.soton.ac.uk>"

import copy
import numpy as np

from typing import List, Tuple

from representation import Population, Individual
from mutation import Mutator
from scoring import Scorer
from selection import Selector, FitnessProportionateSelection


class Coevolution:
    def __init__(
        self,
        scorer: Scorer = Scorer(intransitive=False),
        selector: Selector = FitnessProportionateSelection(),
        mutator: Mutator = Mutator(),
        hof: HOF = None,
    ):
        self.scorer = scorer
        self.selector = selector
        self.mutator = mutator
        self.pops_a = []
        self.pops_b = []
        # Use HOF if provided
        self.hof = hof is not None
        self.hof_a = copy.deepcopy(hof)
        self.hof_b = copy.deepcopy(hof)

    def run(self, pop_a: Population, pop_b: Population, generations: int):
        self.pops_a, self.pops_b = [pop_a], [pop_b]
        self.subj_a, self.subj_b = [], []
        for g in range(generations + 1):
            # Use the last populations
            pop_a = self.pops_a[-1]
            pop_b = self.pops_b[-1]
            # Record average subjective score
            f_ab, f_ba = self.assess_fitness(pop_a, pop_b)
            self.subj_a += [np.mean(f_ab)]
            self.subj_b += [np.mean(f_ba)]
            if self.hof:
                self.hof_a.add(pop_a[np.argmax(f_ab)])
                self.hof_b.add(pop_b[np.argmax(f_ba)])
            if g == generations:
                break
            # Get next generations
            self.pops_a += [self.next_generation(pop_a, f_ab)]
            self.pops_b += [self.next_generation(pop_b, f_ba)]

    def next_generation(self, pop: Population, f: List[float]) -> Population:
        idxs = self.selector.select(f)
        new_pop = Population()
        for idx in idxs:
            new_pop += [self.mutator.mutate(pop[idx])]
        return new_pop

    def assess_fitness(
        self, pop_a: Population, pop_b: Population
    ) -> Tuple[List[float], List[float]]:
        pop_ab = self._assess_fitness(pop_a, pop_b, self.hof_a)
        pop_ba = self._assess_fitness(pop_b, pop_a, self.hof_b)
        return (pop_ab, pop_ba)

    def _assess_fitness(
        self, pop: Population, opponents: Population, hof: HOF = None
    ) -> List[float]:
        pop_scores = []
        for i in pop:
            score = self.scorer.subj_fitness(i, opponents)
            if hof:
                score += hof.scorer.subj_fitness(i, hof.pop)
            pop_scores += [np.mean(score)]
        return pop_scores


class HOF:
    def __init__(self, scorer: Scorer, size: int):
        self.scorer = scorer
        self.size = size
        self.pop = Population()

    def add(self, ind: Individual):
        self.pop += [ind]
        if len(self.pop) > self.size:
            self.pop.pop(0)
