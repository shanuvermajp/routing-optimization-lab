# routing-optimization-lab

A structured learning progression through vehicle routing optimization — from TSP basics to CVRPTW with exact solvers.

Built and maintained by **Inovex Solutions**.

---

## Structure

| Folder | Topic | Concepts |
|---|---|---|
| `01_tsp/` | Travelling Salesman Problem | Distance matrix, nearest neighbour, 2-opt |
| `02_cvrp/` | Capacitated VRP | Vehicle capacity, multiple routes |
| `03_cvrptw/` | VRP with Time Windows | Time feasibility, scheduling |
| `04_ortools/` | Exact solver | OR-Tools, optimal solutions |
| `05_benchmarks/` | Solomon instances | Industry-standard benchmarking |

---

## Setup

```bash
git clone https://github.com/inovex-solutions/routing-optimization-lab
cd routing-optimization-lab
pip install -r requirements.txt
```

## Run

```bash
# Step 1 — TSP basics (terminal output)
python 01_tsp/tsp_basics.py

# Step 1 — Visualize (saves PNG)
python 01_tsp/tsp_visualize.py

# Streamlit UI (opens in browser at http://localhost:8501)
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
