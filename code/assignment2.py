"""COMP6202

Reimplementation of the paper:
    Coevolutionary Dynamics in a Minimal Substrate (Watson and Pollack, 2001)

Extension:
    Implementation of 'Hall of Fame'... TODO

File to execute as main to start coevolution.
"""
__authors__ = "David Jones <dsj1n15@ecs.soton.ac.uk>"


import os
import cv2 as cv
import matplotlib.pyplot as plt

from coevolution import Coevolution, HOF
from representation import Generator
from mutation import Mutator
from scoring import Scorer, F0Scorer

from plot import Plotter
from utils import seed_random


def run():
    plotter = Plotter(show_avgs=True, plot_elites=True)
    fig_1 = 1
    fig_2 = 1
    fig_3 = 1
    fig_4 = 1
    fig_5 = 1

    use_fixed_seed = 1
    enable_hof = 0
    generations = 600
    export_folder = "../report/plots/"
    generator_a = Generator(100, 1)
    generator_b = Generator(10, 10)
    generator_c = Generator(50, 2)
    mutator = Mutator(mutation_rate=0.005, bit_flip=False)
    n = 25

    if enable_hof:
        hof = HOF(scorer=Scorer(sample_size=5), size=50)
    else:
        hof = None

    if fig_1:
        seed = seed_random(0, use_fixed_seed)
        description = "Figure 1 : [Seed {}]".format(seed)
        print(description)
        pop_a = generator_a.population(n, 0)
        pop_b = generator_a.population(n, 100)
        executor = Coevolution(scorer=F0Scorer())
        executor.run(pop_a, pop_b, generations)
        plotter.make_plot(
            executor,
            fig_name=description,
            export_path=os.path.join(export_folder, "fig1.pdf"),
        )

    if fig_2:
        seed = seed_random(1, use_fixed_seed)
        description = "Figure 2 : [Seed {}]".format(seed)
        print(description)
        pop_a = generator_a.population(n, 0)
        pop_b = generator_a.population(n, 0)
        executor = Coevolution(mutator=mutator, hof=hof)
        executor.run(pop_a, pop_b, generations)
        plotter.make_plot(
            executor,
            fig_name=description,
            export_path=os.path.join(export_folder, "fig2.pdf"),
        )

    if fig_3:
        seed = seed_random(8486058433753192762, use_fixed_seed)
        description = "Figure 3 : [Seed {}]".format(seed)
        print(description)
        pop_a = generator_a.population(n, 0)
        pop_b = generator_a.population(n, 0)
        executor = Coevolution(mutator=mutator, scorer=Scorer(sample_size=1), hof=hof)
        executor.run(pop_a, pop_b, generations)
        plotter.make_plot(
            executor,
            fig_name=description,
            export_path=os.path.join(export_folder, "fig3.pdf"),
        )

    if fig_4:
        seed = seed_random(59759543964706904, use_fixed_seed)
        description = "Figure 4 : [Seed {}]".format(seed)
        print(description)
        pop_a = generator_b.population(n, 0)
        pop_b = generator_b.population(n, 0)
        executor = Coevolution(mutator=mutator, hof=hof)
        executor.run(pop_a, pop_b, generations)
        plotter.make_plot(
            executor,
            fig_name=description,
            export_path=os.path.join(export_folder, "fig4.pdf"),
        )

    if fig_5:
        seed = seed_random(5706501168717675099, use_fixed_seed)
        description = "Figure 5 : [Seed {}]".format(seed)
        print(description)
        pop_a = generator_c.population(n, 0)
        pop_b = generator_c.population(n, 0)
        executor = Coevolution(
            mutator=mutator, scorer=Scorer(intransitive=True), hof=hof
        )
        executor.run(pop_a, pop_b, generations)
        plotter.make_plot(
            executor,
            fig_name=description,
            export_path=os.path.join(export_folder, "fig5.pdf"),
        )


def run_loop(repeat: bool = False, executions: int = 1):
    while True:
        for e in range(executions):
            run()
        plt.show()
        cv.waitKey()
        if not repeat:
            break

if __name__ == "__main__":
    run_loop()
