"""
sudoku_solver.py

Implement the function `solve_sudoku(grid: List[List[int]]) -> List[List[int]]` using a SAT solver from PySAT.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List

def solve_sudoku(grid: List[List[int]]) -> List[List[int]]:
    """Solves a Sudoku puzzle using a SAT solver. Input is a 2D grid with 0s for blanks."""

    # TODO: implement encoding and solving using PySAT

    cnf = CNF()
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                cnf.append([(i+1)*100 + (j+1)*10 + grid[i][j]])


    # Each row contains atleast one occurence of each number from 1 to 9
    for i in range(1,10):
        for k in range(1,10):
            clause = list()
            for j in range(1,10):
                clause.append(i*100+j*10+k)
            cnf.append(clause)

    # Each column contains atleast one occurence of each number from 1 to 9
    for j in range(1,10):
        for k in range(1,10):
            clause=list()
            for i in range(1,10):
                clause.append(i*100+j*10+k)
            cnf.append(clause)
    
    for k in range(1,10):
        for i in [1,4,7]:
            for j in [1,4,7]:
                clause = list()
                clause.append(i*100+j*10+k)
                clause.append(i*100+(j+1)*10+k)
                clause.append(i*100+(j+2)*10+k)
                clause.append((i+1)*100+j*10+k)
                clause.append((i+1)*100+(j+1)*10+k)
                clause.append((i+1)*100+(j+2)*10+k)
                clause.append((i+2)*100+j*10+k)
                clause.append((i+2)*100+(j+1)*10+k)
                clause.append((i+2)*100+(j+2)*10+k)
                cnf.append(clause)

    for i in range(1,10):
        for j in range(1,10):
            for k in range(1,10):
                for l in range(1,k):
                    cnf.append([-(i*100 + j*10 + k),-(i*100 + j*10 + l)])

    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf.clauses)
        if solver.solve():
            model = solver.get_model()
            correct_clauses = [i for i in model if i>0]
            for i in correct_clauses:
                grid[int(i/100)-1][int(i/10)%10-1] = i%10
        else:
            pass

    return grid