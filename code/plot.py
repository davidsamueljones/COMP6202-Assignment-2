"""COMP6202 - Evolution of Complexity
Plotting methods for coevolution report graphs.
"""

__authors__ = "David Jones <dsj1n15@ecs.soton.ac.uk>"

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os

from typing import List
from matplotlib.pyplot import figure
from representation import Population
from coevolution import Coevolution


class Plotter:
    def __init__(self, show_avgs: bool = True, plot_elites: bool = False):
        self.show_avgs = show_avgs
        self.show_elite_plots = plot_elites

        self.a_color = "darkred"
        self.a_avg_color = "orangered"
        self.b_color = "midnightblue"
        self.b_avg_color = "dodgerblue"
        if not show_avgs:
            self.a_color = self.a_avg_color
            self.b_color = self.b_avg_color

    def make_plot(
        self, coevolution: Coevolution, fig_name: str = None, export_path: str = None
    ) -> figure:
        # Prepare data
        generations = len(coevolution.pops_a)
        total_bits = coevolution.pops_a[-1][0].total_bits
        avgs_x = range(generations)
        raw_x, a_raw, b_raw, a_avgs, b_avgs = ([] for i in range(5))
        for g in range(generations):
            pop_a = list(map(lambda x: x.value, coevolution.pops_a[g]))
            pop_b = list(map(lambda x: x.value, coevolution.pops_b[g]))
            # X axis
            raw_x += [g] * len(pop_b)
            # Append raw data
            a_raw += pop_a
            b_raw += pop_b
            # Record averages
            a_avgs += [np.mean(pop_a)]
            b_avgs += [np.mean(pop_b)]

        # Use LaTeX fonts in the plot
        plt.rc("text", usetex=True)
        plt.rc("font", family="serif")

        w, h = plt.figaspect(0.88)
        fig = plt.figure(fig_name, figsize=(w, h))
        ax = fig.subplots(3, 1, sharex=True, gridspec_kw={"height_ratios": [16, 1, 1]})
        fig.subplots_adjust(hspace=0.11)
        # Fix all x axis limits (shared axis)
        ax[0].set_xlim([0, generations])

        # Configure Objective Score Plot
        plt.subplot(ax[0])
        ax[0].set_ylim([0, total_bits])
        ax[0].tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        ax[0].set_ylabel(r"\textbf{objectv fitness}", fontsize=11)
        ax[0].spines["right"].set_visible(False)
        plt.hlines(total_bits / 2, 0, generations, colors="black", linewidth=1)

        # Plot Raw
        plt.scatter(raw_x, a_raw, s=1, c=self.a_color, alpha=1, lw=0)
        plt.scatter(raw_x, b_raw, s=1, c=self.b_color, alpha=1, lw=0)
        # Plot Averages
        if self.show_avgs:
            plt.plot(a_avgs, c=self.a_avg_color, lw=1)
            plt.plot(b_avgs, c=self.b_avg_color, lw=1)

        # Make a legend
        plt.plot([], [], c=self.a_avg_color, label="$P_A$")
        plt.plot([], [], c=self.b_avg_color, label="$P_B$")
        plt.legend()
        # Plot Subjective Score (A)
        plt.subplot(ax[1])
        plt.scatter(avgs_x, coevolution.subj_a, c=self.a_avg_color, s=2)
        plt.setp(ax[1].get_xticklabels(), visible=False)
        ax[1].set_ylim([0, 1])
        ax[1].spines["bottom"].set_visible(False)
        ax[1].spines["right"].set_visible(False)
        ax[1].spines["top"].set_visible(False)
        ax[1].tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        # Plot Subjective Score (B)
        plt.subplot(ax[2], sharey=ax[1])
        plt.scatter(avgs_x, coevolution.subj_b, c=self.b_avg_color, s=2)
        ax[2].set_xlabel(r"\textbf{Generations}", fontsize=11)
        ax[2].set_ylim([0, 1])
        ax[2].figure.text(
            0.05, 0.2, r"\textbf{subj fitness}", fontsize=11, va="center", rotation=90,
        )
        ax[2].spines["right"].set_visible(False)
        ax[2].spines["top"].set_visible(False)

        # Plot elites
        if self.show_elite_plots:
            self.plot_elites(fig_name + "- Elites [A]", coevolution.pops_a)
            self.plot_elites(fig_name + "- Elites [B]", coevolution.pops_b)

        # Export
        if export_path:
            folder_path = "/".join(export_path.split("/")[0:-1])
            if folder_path and not os.path.exists(folder_path):
                os.makedirs(folder_path)
            fig.savefig(export_path, bbox_inches="tight")
        return fig

    def plot_elites(self, fig_name: str, pops: List[Population]):
        elites = [max(pop, key=lambda x: x.value) for pop in pops]
        bitmap = None
        for elite in elites:
            bits = elite.as_bits()
            if bitmap is None:
                bitmap = bits
            else:
                bitmap = np.vstack((bitmap, elite.as_bits()))
        bitmap = bitmap.astype(float)
        show_bitmap = cv.resize(
            bitmap, (0, 0), fx=7.5, fy=0.25, interpolation=cv.INTER_NEAREST
        )
        cv.imshow(fig_name, show_bitmap)
