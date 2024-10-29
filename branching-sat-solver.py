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

def branching_sat_solve(clause_set, partial_assignment=[]):
    if len(clause_set) == 0:
        return partial_assignment  # base case: this is when the clause set is empty so the partial assignment satisfies it

    for clause in clause_set:
        # check for unsatisfied clauses with the current partial assignment
        unsat = True
        for literal in clause: # a clause is satisfied if any literal in it is in the partial assignment
            if literal > 0 and literal not in partial_assignment or literal < 0 and -literal not in partial_assignment: # inverted logic: checks if a literal in the clause is unsatisfied by the current partial_assignment.
                unsat = False # mark as satisfied, stop checking further
                break # the dual negative is quite counterintuitive; since the code sets unsat = True at the start and then flips it to False upon finding a satisfying literal
        if unsat: # if any clause is unsatisfied by this assignment
            return False

    # branch on an unassigned literal
    chooselit = None
    for clause in clause_set:
        for literal in clause: # select the first unassigned literal (usually the smallest)
            if abs(literal) not in [abs(x) for x in partial_assignment]: # check the literal not yet assigned in the partial assignment
                chooselit = abs(literal) # literal, i choose you! 
                break
        if chooselit is not None:
            break
    if chooselit is None:
        # if there are no literals left to assign, UNSAT
        return False

    # branching step 1: first, try assigning chooselit = True
    true_assignment = partial_assignment + [chooselit] # add chosen literal to the partial assignment
    true_clauses = [[i for i in clause if i != chooselit and i != -chooselit] for clause in clause_set if
                    chooselit not in clause]
    # key line: create a reduced clause set by removing all satisfied clauses and removing negated literals from remaining clauses
    true_result = branching_sat_solve(true_clauses, true_assignment)  # function calls itself recursively here
    # if true assignment is successful, return the solution
    if true_result != False:
        return true_result

    # if assigning chooselit = True fails, backtrack and try assigning False
    false_assignment = partial_assignment + [-chooselit]
    false_clauses = [[i for i in clause if i != chooselit and i != -chooselit] for clause in clause_set if
                     -chooselit not in clause] # as previous, reduce the clause set
    false_result = branching_sat_solve(false_clauses, false_assignment) # recursively solve with the new clause set and updated partial assignment
    # if false assignment is successful, return the solution, else UNSAT since neither branch yields a solution
    if false_result != False:
        return false_result
    return False

end = time.time()

# example
clause_set = load_dimacs("LNP-6.txt")
solution = branching_sat_solve(clause_set, partial_assignment=[])
#numpy_solution = np.array(solution)
#print(np.sort(numpy_solution))
print(solution)
print("Time taken =", end - start)