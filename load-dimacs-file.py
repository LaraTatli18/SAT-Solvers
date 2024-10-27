def load_dimacs(filename):
    clause_set = []
    sat_file = open(filename)
    for line in sat_file:
        if line[0] not in ('cnf', 'p'): # don't process lines with comments (c) or parameters (p)
            clause_set.append([int(n) for n in line.split() if n!= '0']) # convert each line to list of integers, ignoring 0s which indicate end of clause
    return clause_set

# examples
print(load_dimacs("sat.txt"))
print(load_dimacs("unsat.txt"))
print(load_dimacs("4queens.txt"))
print(load_dimacs("8queens.txt"))