"""
streamlit_app.py
================
Interactive UI for the TSP solver.

What it does:
    - User controls number of cities, seed, start city via sliders
    - Clicking "Solve" runs nearest neighbour + 2-opt
    - Shows route map and metrics side by side
    - Compares before/after 2-opt visually

Run with:
    streamlit run app/streamlit_app.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '01_tsp'))

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from tsp_basics import (
    generate_instance,
    build_distance_matrix,
    nearest_neighbour,
    two_opt,
    tour_distance,
)


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="TSP Solver — Inovex Solutions",
    page_icon="🚚",
    layout="wide",
)


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.title("🚚 TSP Solver")
st.markdown(
    "**Travelling Salesman Problem** — nearest neighbour heuristic + 2-opt improvement.  "
    "Part of [routing-optimization-lab](https://github.com/inovex-solutions/routing-optimization-lab) "
    "by Inovex Solutions."
)
st.divider()


# ─────────────────────────────────────────────
# SIDEBAR — USER CONTROLS
# ─────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Problem settings")

    n_cities = st.slider(
        "Number of cities",
        min_value=5,
        max_value=50,
        value=15,
        step=1,
        help="Total cities to visit including depot (city 0)"
    )

    seed = st.slider(
        "Random seed",
        min_value=1,
        max_value=100,
        value=42,
        help="Change seed to generate a different city layout"
    )

    start_city = st.slider(
        "Start city (depot)",
        min_value=0,
        max_value=n_cities - 1,
        value=0,
        help="The vehicle starts and ends here"
    )

    st.divider()
    solve_btn = st.button("▶ Solve", type="primary", use_container_width=True)
    st.caption("Runs nearest neighbour then 2-opt improvement")


# ─────────────────────────────────────────────
# PLOT FUNCTION
# ─────────────────────────────────────────────

def plot_tour(coords, tour, title, color, linestyle):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title(title, fontsize=12, fontweight="bold")

    # Draw route edges
    for i in range(len(tour) - 1):
        a, b = tour[i], tour[i + 1]
        ax.plot(
            [coords[a, 0], coords[b, 0]],
            [coords[a, 1], coords[b, 1]],
            color=color,
            linestyle=linestyle,
            linewidth=1.8,
            alpha=0.75,
        )

    # City markers
    ax.scatter(coords[:, 0], coords[:, 1], color="black", s=60, zorder=5)

    # City labels
    for i, (x, y) in enumerate(coords):
        ax.annotate(str(i), (x, y), xytext=(5, 4),
                    textcoords="offset points", fontsize=7)

    # Depot star
    ax.scatter(
        coords[start_city, 0], coords[start_city, 1],
        color="red", s=180, zorder=6, marker="*", label=f"Depot (city {start_city})"
    )

    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────
# SOLVE + DISPLAY
# ─────────────────────────────────────────────

if solve_btn:

    # Generate and solve
    coords = generate_instance(n_cities=n_cities, seed=seed)
    dist   = build_distance_matrix(coords)

    with st.spinner("Running nearest neighbour..."):
        nn_tour, nn_dist = nearest_neighbour(dist, start=start_city)

    with st.spinner("Running 2-opt improvement..."):
        opt_tour, opt_dist = two_opt(nn_tour, dist)

    improvement = (nn_dist - opt_dist) / nn_dist * 100

    # ── Metrics row ──
    st.subheader("📊 Results")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cities", n_cities)
    col2.metric("NN distance",     f"{nn_dist:.1f}")
    col3.metric("2-opt distance",  f"{opt_dist:.1f}",
                delta=f"-{nn_dist - opt_dist:.1f}", delta_color="inverse")
    col4.metric("Improvement",     f"{improvement:.1f}%")

    st.divider()

    # ── Side-by-side plots ──
    st.subheader("🗺️ Route comparison")
    left, right = st.columns(2)

    with left:
        fig_nn = plot_tour(
            coords, nn_tour,
            title=f"Nearest Neighbour — {nn_dist:.1f}",
            color="#E74C3C", linestyle="--"
        )
        st.pyplot(fig_nn)

    with right:
        fig_opt = plot_tour(
            coords, opt_tour,
            title=f"After 2-opt — {opt_dist:.1f}",
            color="#27AE60", linestyle="-"
        )
        st.pyplot(fig_opt)

    st.divider()

    # ── Route details ──
    st.subheader("📋 Route details")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Nearest Neighbour route**")
        st.code(" → ".join(str(c) for c in nn_tour))

    with col_b:
        st.markdown("**2-opt improved route**")
        st.code(" → ".join(str(c) for c in opt_tour))

else:
    st.info("👈 Configure the problem in the sidebar and click **Solve**.")
