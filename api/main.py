"""
main.py
=======
FastAPI REST API for the TSP solver.

What it does:
    - Exposes the TSP solver as an HTTP API
    - Client sends problem parameters → API returns solution as JSON
    - Industry standard: this is how optimization solvers are deployed in production

Endpoints:
    GET  /              → health check
    POST /solve/tsp     → solve a TSP instance, returns tour + distance
    GET  /instance      → generate a random instance (for testing)

Run with:
    uvicorn api.main:app --reload

Then open:
    http://127.0.0.1:8000/docs   ← automatic interactive documentation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '01_tsp'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import numpy as np

from tsp_basics import (
    generate_instance,
    build_distance_matrix,
    nearest_neighbour,
    two_opt,
    tour_distance,
)


# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────

app = FastAPI(
    title="TSP Solver API",
    description=(
        "Travelling Salesman Problem solver — nearest neighbour + 2-opt.  \n"
        "Part of **routing-optimization-lab** by Inovex Solutions."
    ),
    version="1.0.0",
)


# ─────────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# Pydantic validates all inputs automatically
# ─────────────────────────────────────────────

class TSPRequest(BaseModel):
    """What the client sends to /solve/tsp"""

    n_cities: int = Field(
        default=10,
        ge=3, le=100,
        description="Number of cities (3–100)"
    )
    seed: Optional[int] = Field(
        default=42,
        description="Random seed for reproducibility. Omit for random instance."
    )
    start_city: int = Field(
        default=0,
        ge=0,
        description="Depot city index — tour starts and ends here"
    )
    use_two_opt: bool = Field(
        default=True,
        description="Apply 2-opt improvement after nearest neighbour"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "n_cities": 15,
                "seed": 42,
                "start_city": 0,
                "use_two_opt": True,
            }
        }


class TSPResponse(BaseModel):
    """What the API sends back"""

    n_cities: int
    seed: int
    start_city: int

    nn_tour: List[int]
    nn_distance: float

    opt_tour: List[int]
    opt_distance: float

    improvement_pct: float
    two_opt_applied: bool

    coordinates: List[List[float]]


class InstanceResponse(BaseModel):
    """Random instance for testing"""
    n_cities: int
    seed: int
    coordinates: List[List[float]]


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/", summary="Health check")
def root():
    """Check the API is running."""
    return {
        "status": "ok",
        "service": "TSP Solver API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get(
    "/instance",
    response_model=InstanceResponse,
    summary="Generate a random TSP instance"
)
def get_instance(n_cities: int = 10, seed: int = 42):
    """
    Generate a random set of city coordinates.
    Use this to preview a problem before solving.
    """
    if not (3 <= n_cities <= 100):
        raise HTTPException(status_code=400, detail="n_cities must be between 3 and 100")

    coords = generate_instance(n_cities=n_cities, seed=seed)
    return InstanceResponse(
        n_cities=n_cities,
        seed=seed,
        coordinates=coords.round(2).tolist(),
    )


@app.post(
    "/solve/tsp",
    response_model=TSPResponse,
    summary="Solve a TSP instance"
)
def solve_tsp(request: TSPRequest):
    """
    Solve the Travelling Salesman Problem.

    Steps:
    1. Generate random city coordinates using the given seed
    2. Build the distance matrix
    3. Run nearest neighbour heuristic
    4. Optionally apply 2-opt improvement

    Returns both the raw NN solution and the 2-opt improved solution
    so you can compare them.
    """
    # Validate start city
    if request.start_city >= request.n_cities:
        raise HTTPException(
            status_code=400,
            detail=f"start_city ({request.start_city}) must be < n_cities ({request.n_cities})"
        )

    seed = request.seed if request.seed is not None else np.random.randint(0, 10000)

    # Build instance
    coords = generate_instance(n_cities=request.n_cities, seed=seed)
    dist   = build_distance_matrix(coords)

    # Solve
    nn_tour, nn_dist = nearest_neighbour(dist, start=request.start_city)

    if request.use_two_opt:
        opt_tour, opt_dist = two_opt(nn_tour, dist)
    else:
        opt_tour, opt_dist = nn_tour, nn_dist

    improvement = (nn_dist - opt_dist) / nn_dist * 100 if nn_dist > 0 else 0.0

    return TSPResponse(
        n_cities=request.n_cities,
        seed=seed,
        start_city=request.start_city,
        nn_tour=nn_tour,
        nn_distance=round(nn_dist, 4),
        opt_tour=opt_tour,
        opt_distance=round(opt_dist, 4),
        improvement_pct=round(improvement, 2),
        two_opt_applied=request.use_two_opt,
        coordinates=coords.round(2).tolist(),
    )
