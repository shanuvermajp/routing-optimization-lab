# routing-optimization-lab

A structured learning progression through vehicle routing optimization — from TSP basics to CVRPTW with exact solvers.

Built and maintained by **[Inovex Solutions](https://github.com/shanuvermajp)**.

---

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://routing-optimization-lab-fbuuoop2zlchxpxqhejywb.streamlit.app/)

> Try the live TSP solver — adjust cities, seed, and start city, then click Solve to see the route comparison.

---

## What this project covers

| Folder | Topic | Concepts |
|---|---|---|
| `01_tsp/` | Travelling Salesman Problem | Distance matrix, nearest neighbour, 2-opt |
| `02_cvrp/` | Capacitated VRP | Vehicle capacity, multiple routes |
| `03_cvrptw/` | VRP with Time Windows | Time feasibility, scheduling |
| `04_ortools/` | Exact solver | OR-Tools, optimal solutions |
| `05_benchmarks/` | Solomon instances | Industry-standard benchmarking |

---

## API

The solver is also exposed as a REST API using FastAPI.

**Run locally:**
```bash
uvicorn api.main:app --reload
```

**Endpoints:**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/instance` | Generate a random TSP instance |
| POST | `/solve/tsp` | Solve TSP, returns tour + distance |

**Example request:**
```json
POST /solve/tsp
{
  "n_cities": 15,
  "seed": 42,
  "start_city": 0,
  "use_two_opt": true
}
```

**Example response:**
```json
{
  "n_cities": 15,
  "nn_distance": 339.38,
  "opt_distance": 313.00,
  "improvement_pct": 7.8,
  "opt_tour": [0, 10, 12, 8, 13, 7, 4, 14, 2, 5, 6, 3, 11, 1, 9, 0]
}
```

---

## Setup

```bash
git clone https://github.com/shanuvermajp/routing-optimization-lab
cd routing-optimization-lab
pip install -r requirements.txt
```

## Run

```bash
# TSP solver (terminal output)
python 01_tsp/tsp_basics.py

# Route visualizer (saves PNG)
python 01_tsp/tsp_visualize.py

# Streamlit UI (opens at http://localhost:8501)
streamlit run app/streamlit_app.py

# FastAPI (opens at http://127.0.0.1:8000/docs)
uvicorn api.main:app --reload
```

---

## Progress

- [x] 01 — TSP: nearest neighbour + 2-opt
- [ ] 02 — CVRP: capacity constraints
- [ ] 03 — CVRPTW: time windows
- [ ] 04 — OR-Tools exact solver
- [ ] 05 — Solomon benchmark

---

## About

This repository is part of Inovex Solutions' open-source optimization toolkit.  
Contact: shanuverma.jp@gmail.com
