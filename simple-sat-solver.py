import itertools

def load_dimacs(filename):
    clause_set = []
    sat_file = open(filename)
    for line in sat_file:
        if line[0] not in ('cnf', 'p'):
            clause_set.append([int(n) for n in line.split() if n!= '0'])
    return clause_set


def simple_sat_solve(clause_set):
    pure_literals = [] # stores unique literals (ignoring sign)
    for clause in clause_set:
        for literal in clause:
            if abs(literal) not in pure_literals:
                pure_literals.append(abs(literal))
    n = len(pure_literals) # number of unique literals

    assignment = list(itertools.product([False, True], repeat=n))
    # iterating through each truth assignment to find one that satisfies all clauses
    for i in range(2 ** n):
        truth_assignment = [literal if value else -(literal) for literal, value in zip(pure_literals, assignment[i])]
        # constructs all possible truth assignments using all possible combinations of True and False
        # if value is True, keep literal positive, else we negate it

        sat = True # assume current truth assignment results in SAT until proven otherwise
        for clause in clause_set:
            found = False
            for literal in truth_assignment:
                if literal in clause:
                    found = True # a clause is satisfied if at least one literal in the clause is True
            if found == False:
                sat = False
        if sat: #SAT, return satisfying solution
            return truth_assignment
    return False # UNSAT, couldn't find satisfying solution


# examples
clause_set = load_dimacs("sat.txt")
print(simple_sat_solve(clause_set)) # SAT, returns the satisfying solution [1, -2]

clause_set = load_dimacs("unsat.txt")
print(simple_sat_solve(clause_set)) # UNSAT, returns False