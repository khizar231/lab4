# CAI601400 — Artificial Intelligence Lab 4

## Important graph assumption
The task refers to a supplied campus graph and heuristic, but those were not attached in the message. To keep this package reproducible without pretending to know the course handout, the package uses the explicit graph in `campus_graph.json`. Compare it with your supplied graph and replace the data if needed before submission.

## Graph and successor order
Start S, goal G. Successor order:
- S: A, B, C
- A: D, G
- B: G
- C: G
- D: G
- G: none

Edge costs: S→A=1, S→B=4, S→C=2, A→D=2, A→G=9, B→G=3, C→G=5, D→G=2.
Original heuristic: h(S)=5, h(A)=3, h(B)=3, h(C)=4, h(D)=1, h(G)=0.
Overestimate experiment changes only h(C) from 4 to 10.

## Files
- `lab4_astar_audit.py`: A*, UCS control, path-cost verification, heuristic overestimate run.
- `campus_graph.json`: graph, weights, successor order and heuristic.
- `Lab4_Report.docx`: manual calculations, result comparison, heuristic audit and reflection.
- `outputs.txt`: captured console outputs.

## Run
Python 3.10+; no third-party packages required.
```bash
python lab4_astar_audit.py
```

## Counting convention
Expansion count includes each non-stale node when popped and processed, including goal G. Stale or duplicate entries skipped are not counted. Priority ties are resolved by insertion counter, preserving successor insertion order.

## Submission checklist
Compare graph and heuristic with the course handout first. Commit the source, input JSON, report, README and outputs. Do not commit credentials, private data or virtual environments. Give the instructor access and submit repository URL plus final commit identifier.
