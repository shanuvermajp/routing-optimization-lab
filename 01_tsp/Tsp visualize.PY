"""
tsp_visualize.py
================
Visualize TSP solutions using Matplotlib.

Shows:
    - City positions
    - Route before 2-opt (red dashed)
    - Route after 2-opt  (green solid)
    - Distance comparison in title

Run after tsp_basics.py — imports functions from it.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tsp_basics import (
    generate_instance,
    build_distance_matrix,
    nearest_neighbour,
    two_opt,
    tour_distance,
)


def plot_tour(ax, coords, tour, color, linestyle, label, linewidth=1.5):
    """Draw a tour on a matplotlib axis."""
    for i in range(len(tour) - 1):
        a, b = tour[i], tour[i + 1]
        ax.plot(
            [coords[a, 0], coords[b, 0]],
            [coords[a, 1], coords[b, 1]],
            color=color,
            linestyle=linestyle,
            linewidth=linewidth,
            alpha=0.7,
        )
    # Draw city markers
    ax.scatter(coords[:, 0], coords[:, 1], color="black", s=60, zorder=5)

    # Label each city
    for i, (x, y) in enumerate(coords):
        ax.annotate(
            str(i),
            (x, y),
            textcoords="offset points",
            xytext=(6, 4),
            fontsize=8,
            color="black",
        )

    # Highlight depot (city 0)
    ax.scatter(coords[0, 0], coords[0, 1], color="red", s=120, zorder=6, marker="*")


def visualize(coords, nn_tour, nn_dist, opt_tour, opt_dist):
    """
    Side-by-side plot:
        Left  → Nearest Neighbour solution
        Right → After 2-opt improvement
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("TSP: Nearest Neighbour vs 2-opt", fontsize=14, fontweight="bold")

    # Left: Nearest Neighbour
    axes[0].set_title(f"Nearest Neighbour\nDistance: {nn_dist:.2f}", fontsize=11)
    plot_tour(axes[0], coords, nn_tour, color="#E74C3C", linestyle="--", label="NN")
    axes[0].set_xlim(-5, 105)
    axes[0].set_ylim(-5, 105)
    axes[0].set_aspect("equal")
    axes[0].grid(True, alpha=0.3)

    # Right: 2-opt improved
    axes[1].set_title(f"After 2-opt\nDistance: {opt_dist:.2f}", fontsize=11)
    plot_tour(axes[1], coords, opt_tour, color="#27AE60", linestyle="-", label="2-opt")
    axes[1].set_xlim(-5, 105)
    axes[1].set_ylim(-5, 105)
    axes[1].set_aspect("equal")
    axes[1].grid(True, alpha=0.3)

    # Legend
    depot_marker = mpatches.Patch(color="red", label="Depot (city 0)")
    for ax in axes:
        ax.legend(handles=[depot_marker], loc="upper right", fontsize=8)

    improvement = (nn_dist - opt_dist) / nn_dist * 100
    fig.text(
        0.5, 0.01,
        f"2-opt improved distance by {improvement:.1f}%  "
        f"({nn_dist:.2f} → {opt_dist:.2f})",
        ha="center",
        fontsize=10,
        color="#555555",
    )

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig("tsp_comparison.png", dpi=150, bbox_inches="tight")
    print("Saved: tsp_comparison.png")
    plt.show()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":

    N_CITIES = 15
    coords   = generate_instance(n_cities=N_CITIES, seed=42)
    dist     = build_distance_matrix(coords)

    nn_tour,  nn_dist  = nearest_neighbour(dist, start=0)
    opt_tour, opt_dist = two_opt(nn_tour, dist)

    visualize(coords, nn_tour, nn_dist, opt_tour, opt_dist)
