# SAT Solvers in Python

## Description
A computational project completed in my 1st year of undergraduate studies as part of an elective Computer Science module. I explored different approaches to solving SAT problems in Python by implementing and testing 3 different solvers, ranging from a simple brute-force approach to the more optimised DPLL algorithm, using a variety of pre-prepared DIMACS files. This progression highlights the challenges of SAT problems and the effectiveness of optimisation techniques.

## Project Files

### Text Files
- `sat.txt`: A basic DIMACS file for testing solvers on a satisfiable (SAT) problem.
- `unsat.txt`: A basic DIMACS file representing an unsatisfiable (UNSAT) problem.
- Additional files (`4queens.txt`, `8queens.txt`, etc.) are also provided.

## Preparation Files
- `load-dimacs-file.py`: Reads and parses a DIMACS file into a readable data structure (list format) that the SAT solvers can process.

### SAT Solvers
- `simple-sat-solver.py`: Implements a brute-force approach that tests all possible truth assignments. Limited to very small problems due to exponential complexity.
- `branching-sat-solver.py`: Uses recursion and backtracking to explore assignments, but may still require substantial branching for larger problems.
- `dpll-sat-solver.py`: Implements the DPLL algorithm with unit propagation, iteratively simplifying the problem. This approach is optimised for larger SAT problems and is more efficient.

