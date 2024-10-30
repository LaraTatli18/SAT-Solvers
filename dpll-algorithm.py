import numpy as np
import time

start = time.time()
def load_dimacs(filename):
    clause_set = []
    sat_file = open(filename)
    for line in sat_file:
        if line[0] not in ('cnf', 'p'):
            clause_set.append([int(n) for n in line.split() if n!= '0'])
    return clause_set

def unit_propagate_helper(unit_literal, clause_set):
    # helper function, propagates a single unit literal and simplifies clause set
    new_clause_set = []
    for clause in clause_set:
        if -unit_literal in clause: # if clause contains negation of unit_literal, remove negation from clause
            new_clause = [literal for literal in clause if literal != -unit_literal]
            new_clause_set.append(new_clause) # could probably optimise this further
        # if clause doesn't contain unit_literal or its negation, keep it unchanged
        elif unit_literal not in clause and -unit_literal not in clause:
            new_clause_set.append(clause)
    return new_clause_set


def unit_propagate(clause_set):
    # main unit propagation function: iteratively applies on the clause set (identifies unit clauses/single literals and calls helper function for each one)
    contprop = True # flag to control continue propagation
    while contprop == True:
        contprop = False # assume no more unit clauses; will be set to True if any are found
        for clause in clause_set:
            if len(clause) == 1: # found a unit clause (contains single literal)
                contprop = True # continue propagation since new unit clauses may have been created by removing literals from other clauses
                unit_literal = clause[0] # extract unit literal
                clause_set = unit_propagate_helper(unit_literal, clause_set) # call helper to simplify clause_set based on this unit literal
    return clause_set


def unit_propagate_literals(clause_set):
    # this also performs unit propagation, but additionally collects each unit literal it finds into listofliterals.
    # returns listofliterals to include in partial_assignment as initial, necessary assignments before branching
    listofliterals
    while contprop == True:
        contprop = False
        for clause in clause_set:
            if len(clause) == 1:
                contprop = True
                unit_literal = clause[0]
                if unit_literal not in listofliterals:
                    listofliterals.append(unit_literal)
                clause_set = unit_propagate_helper(unit_literal, clause_set)
            # here i could have streamlined code by not performing full unit propagation; only collecting unique literals
    return listofliterals

def dpll_sat_solve(clause_set, partial_assignment=[]):
    # combines unit propagation with recursive branching
    # first, perform unit propagation to simplify clause set and gather assignments
    listofliterals = unit_propagate_literals(clause_set)
    partial_assignment = partial_assignment + listofliterals

    clause_set = unit_propagate(clause_set) # unit_propagate and unit_propagate_helper are iteratively applied until obtaining a fully simplified clause_set

    if len(clause_set) == 0:
        # if not clause_set:
        return partial_assignment  # base case: this is when the clause set is empty so the partial assignment satisfies it
    for clause in clause_set:
        # check for unsatisfied clauses within the current partial assignment
        unsat = True
        for literal in clause: # a clause is satisfied if any literal in it is satisfied
            if literal > 0 and literal not in partial_assignment or literal < 0 and -literal not in partial_assignment:
                unsat = False # mark as satisfied, stop checking further
                break
        if unsat: # if any clause is unsatisfied by this assignment
            return False

    # branch on an unassigned literal
    chooselit = None
    for clause in clause_set:
        for literal in clause: # select the first unassigned literal
            if abs(literal) not in [abs(x) for x in partial_assignment]: # find a literal not yet assigned in the partial assignment
                chooselit = abs(literal)
                break
        if chooselit is not None:
            break
    if chooselit is None:
        # if there are no literals left to assign, UNSAT
        return False

    # branching step 1: first, try assigning chooselit = True
    true_assignment = partial_assignment + [chooselit]
    true_clauses = [[i for i in clause if i != chooselit and i != -chooselit] for clause in clause_set if
                    chooselit not in clause]
    # key line: create a reduced clause set by removing all satisfied clauses and removing negated literals from remaining clauses
    true_result = dpll_sat_solve(true_clauses, true_assignment)  # function calls itself recursively here
    if true_result != False: # if true assignment is successful, return the solution, SAT
        return true_result

    # if assigning chooselit = True fails, backtrack and try assigning False
    false_assignment = partial_assignment + [-chooselit]
    false_clauses = [[i for i in clause if i != chooselit and i != -chooselit] for clause in clause_set if
                     -chooselit not in clause] # as previous, reduce the clause set
    false_result = dpll_sat_solve(false_clauses, false_assignment)  # recursively solve with the new clause set and updated partial assignment
    # if false assignment is successful, return the solution, else UNSAT since neither branch yields a solution
    if false_result != False:
        return false_result
    # if both branches fail to satisfy, return False (no solution found along this path)
    return False

end = time.time()

# example using 8 queens
clause_set = load_dimacs("8queens.txt")
solution = dpll_sat_solve(clause_set, partial_assignment=[])
numpy_solution = np.array(solution)
print(np.sort(numpy_solution))
print("Time taken =", end - start)
