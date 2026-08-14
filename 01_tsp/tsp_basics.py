"""
tsp_basics.py
=============
Travelling Salesman Problem (TSP) — the foundation of all routing problems.

Problem:
    Given N cities, find the shortest route that visits every city exactly
    once and returns to the starting city.

This file covers:
    1. Generating a random instance
    2. Building a distance matrix
    3. Nearest Neighbour heuristic (fast, not optimal)
    4. 2-opt improvement (refines the solution)

No solver needed — pure NumPy.
"""

import numpy as np


# ─────────────────────────────────────────────
# 1. INSTANCE GENERATION
# ─────────────────────────────────────────────

def generate_instance(n_cities=15, seed=42):
    """
    Generate random city coordinates in a 100x100 grid.

    Returns:
        coords : np.ndarray of shape (n_cities, 2)
    """
    rng = np.random.default_rng(seed)
    coords = rng.uniform(0, 100, size=(n_cities, 2))
    return coords


# ─────────────────────────────────────────────
# 2. DISTANCE MATRIX
# ─────────────────────────────────────────────

def build_distance_matrix(coords):
    """
    Compute Euclidean distance between every pair of cities.

    dist[i][j] = straight-line distance from city i to city j.

    Returns:
        dist : np.ndarray of shape (n, n)
    """
    n = len(coords)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            diff = coords[i] - coords[j]
            dist[i][j] = np.sqrt(diff @ diff)   # Euclidean distance
    return dist


# ─────────────────────────────────────────────
# 3. NEAREST NEIGHBOUR HEURISTIC
# ─────────────────────────────────────────────

def nearest_neighbour(dist, start=0):
    """
    Build a TSP tour greedily:
        - Start at 'start' city
        - Always go to the closest unvisited city
        - Return to start at the end

    This is fast (O(n²)) but not optimal — typically 20-25% above optimum.

    Returns:
        tour  : list of city indices, e.g. [0, 3, 7, 2, ..., 0]
        total : float, total tour distance
    """
    n = len(dist)
    unvisited = set(range(n))
    current = start
    tour = [current]
    unvisited.remove(current)

    while unvisited:
        # Find nearest unvisited city
        nearest = min(unvisited, key=lambda city: dist[current][city])
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest

    tour.append(start)  # return to depot
    total = tour_distance(tour, dist)
    return tour, total


# ─────────────────────────────────────────────
# 4. TOUR DISTANCE
# ─────────────────────────────────────────────

def tour_distance(tour, dist):
    """
    Compute total distance of a tour.
    tour = [0, 3, 7, 2, ..., 0]  (first and last city are the same)
    """
    return sum(dist[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))


# ─────────────────────────────────────────────
# 5. 2-OPT IMPROVEMENT
# ─────────────────────────────────────────────

def two_opt(tour, dist):
    """
    Improve a TSP tour using 2-opt local search.

    Idea:
        Take two edges (i→i+1) and (j→j+1).
        Remove them. Reconnect by reversing the segment between i+1 and j.
        If the new tour is shorter, keep it.

    Repeat until no improvement is found (local optimum).

    This is O(n²) per iteration but dramatically improves solution quality.

    Returns:
        best_tour     : improved list of city indices
        best_distance : float, improved total distance
    """
    best_tour = tour[:]
    best_distance = tour_distance(best_tour, dist)
    n = len(best_tour) - 1      # exclude the return-to-depot duplicate

    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # Reverse the segment between i and j
                new_tour = best_tour[:i] + best_tour[i:j + 1][::-1] + best_tour[j + 1:]
                new_distance = tour_distance(new_tour, dist)

                if new_distance < best_distance - 1e-10:   # small tolerance for floats
                    best_tour = new_tour
                    best_distance = new_distance
                    improved = True

    return best_tour, best_distance


# ─────────────────────────────────────────────
# 6. PRINT SOLUTION
# ─────────────────────────────────────────────

def print_solution(label, tour, distance):
    route = " → ".join(str(c) for c in tour)
    print(f"\n{label}")
    print(f"  Route    : {route}")
    print(f"  Distance : {distance:.2f}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # --- Setup ---
    N_CITIES = 15
    coords = generate_instance(n_cities=N_CITIES, seed=42)
    dist   = build_distance_matrix(coords)

    print(f"TSP instance: {N_CITIES} cities")
    print(f"Coordinates (first 5):\n{coords[:5].round(2)}")

    # --- Nearest Neighbour ---
    nn_tour, nn_dist = nearest_neighbour(dist, start=0)
    print_solution("Nearest Neighbour", nn_tour, nn_dist)

    # --- 2-opt improvement ---
    opt_tour, opt_dist = two_opt(nn_tour, dist)
    print_solution("After 2-opt", opt_tour, opt_dist)

    # --- Improvement summary ---
    improvement = (nn_dist - opt_dist) / nn_dist * 100
    print(f"\n2-opt improvement: {improvement:.1f}%")
    print(f"Gap closed       : {nn_dist - opt_dist:.2f} distance units")
