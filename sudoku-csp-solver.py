# ========================================
#         HOMEWORK 3 QUESTION 1
# ========================================
#  formulation of sudoku as a csp
#      (csp is immutable to simplify implementation)
#      (this makes it run much slower, but the fairly complex inference step lets it take few iterations)
#  solved using a general csp solver
#      (but with a specialized inference step)
# ========================================
#  variables:      one per square (if unassigned)
#
#  domain:         0-9 per square (if unassigned and unconstrained)
#
#  constraints:    all squares in each row are different
#                  all squares in each column are different
#                  all squares in each sub-grid are different
#
#  choose vars:    most constrained variable
#                      tie broken with most constraining variable
#
#  choose values:  smallest first
#
#  inference:      1) enforce consistency of hyper-arc with newly assigned variable
#                      (remove inconsistent values from domains)
#                  2) find singletons on each hyper-arc:
#                      (naked singles heuristic)
#                  3) enforce consistency across intersecting hyper-arcs
#                      the intersection of hyper-arcs constrains both the differences of the sets
#                      (equivalent to several other heuristics combined)
#                  4) repeat until no changes left
# ========================================
#  to run code:    just run it
#  test cases:     see (str) input below
# ========================================
#  1000215 Avery Khoo
#  1000*** Su****** Gu*********
# ========================================
#  test cases and runtimes: see readme


import time
from copy import deepcopy

assign_count = 0


class CSP:
    def __init__(self, variables, domains, constraints, assignments=None):
        """
        represents a CSP
        immutable so that the search is easier to code
        :param variables: <set/list/tuple>  unique hashable ids (representing each variable)
        :param domains: <dict> variable -> set of values
        :param constraints: <dict> hyper arc -> function taking list of assigned values of hyper-arc, true if holds
        :param assignments: <dict> variable -> value
        """
        self.variables = set(variables)
        self.domains = domains
        self.constraints = constraints
        self.assignment = assignments or dict()
        # assert isinstance(self.variables, set)
        assert isinstance(self.domains, dict), 'domains must be a dict'
        assert isinstance(self.constraints, dict), 'constraints must be a dict'
        assert isinstance(self.assignment, dict), 'assignment must be a dict'

    def deepcopy(self):
        return CSP(self.variables, deepcopy(self.domains), self.constraints, deepcopy(self.assignment))

    def count_constrained_variables(self, variable):
        others = set()
        for hyper_arc in self.constraints:
            if variable in hyper_arc:
                others.update(set(hyper_arc))
        others.remove(variable)
        return len(others)

    def most_constrained_variables(self):
        unassigned_variables = self.variables.difference(set(self.assignment.keys()))
        best_value_count = 1e99
        best_variables = []

        # find most constrained variables
        for variable in unassigned_variables:
            value_count = len(self.domains[variable])
            if value_count == 0:
                return [variable]  # branch fails, return early
            if value_count < best_value_count:
                best_variables = [variable]
            elif value_count == best_value_count:
                best_variables += [variable]

        return best_variables

    def select_unassigned_variable(self):
        best_variables = self.most_constrained_variables()

        # order from least to most constraining variable
        best_variables = sorted(best_variables, key=self.count_constrained_variables)

        # return the most constraining variable of the most constrained variables
        return best_variables[-1]

    def count_conflicts(self, variable, value):
        conflicts = 0
        for hyper_arc in self.constraints:
            if variable in hyper_arc:
                assigned_values = [self.assignment[var] for var in hyper_arc if var in self.assignment] + [value]
                if not self.constraints[hyper_arc](*assigned_values):
                    conflicts += 1
        return conflicts

    def assign(self, variable, value):
        global assign_count
        assign_count += 1
        # sanity check
        assert not self.count_conflicts(variable, value)

        # inference step
        csp_copy = self.infer(variable, value)

        # assign the thing and return
        csp_copy.assignment[variable] = value
        return csp_copy

    def infer(self, variable, value):
        # clone because immutable
        csp_copy = self.deepcopy()

        # remove conflicting values in constrained variables
        for hyper_arc in self.constraints:
            if variable in hyper_arc:
                for var in hyper_arc:
                    for val in self.domains[var]:
                        if val in csp_copy.domains[var] and not self.constraints[hyper_arc](val, value):
                            csp_copy.domains[var].remove(val)

        return csp_copy


def backtracking_search(problem):
    """
    recursive
    don't try to solve puzzles with a thousand or more variables
    """
    assert isinstance(problem, CSP)
    # print( 'assigned', len(problem.assignment), 'out of', len(problem.variables))

    # check completion and return
    if len(problem.assignment) == len(problem.variables):
        return problem.assignment

    # select next variable
    variable = problem.select_unassigned_variable()

    # for value in order-domain-values
    for value in problem.domains[variable]:
        # try assigning if valid
        if not problem.count_conflicts(variable, value):
            problem_copy = problem.assign(variable, value)
            result = backtracking_search(problem_copy)
            if result is not None:
                return result
    return None


class SudokuCSP(CSP):
    def deepcopy(self):
        return SudokuCSP(self.variables, deepcopy(self.domains), self.constraints, deepcopy(self.assignment))

    def infer(self, variable, value):
        # clone because immutable
        csp_copy = self.deepcopy()

        # enforce consistency of hyper-arc (remove conflicting values in constrained variables)
        for hyper_arc in self.constraints:
            if variable in hyper_arc:
                for var in hyper_arc:
                    for val in self.domains[var]:
                        if val in csp_copy.domains[var] and not self.constraints[hyper_arc](val, value):
                            csp_copy.domains[var].remove(val)

        change = True
        while change:
            temp = deepcopy(csp_copy.domains)

            # find singletons
            for hyper_arc in self.constraints:

                # invert the variable-value mapping
                co_domains = dict()
                for var in hyper_arc:
                    for val in csp_copy.domains[var]:
                        if val not in co_domains:
                            co_domains[val] = set()
                        co_domains[val].add(var)

                # find singletons
                for val, vars in co_domains.items():
                    if len(vars) == 1:
                        csp_copy.domains[vars.pop()] = {val}

            # interference between intersecting hyper-arcs
            for hyper_arc_1 in self.constraints:
                for hyper_arc_2 in self.constraints:
                    if hyper_arc_1 < hyper_arc_2:  # for every pair of groups

                        # sets of variables in each hyper arc
                        vars_1 = set(hyper_arc_1)
                        vars_2 = set(hyper_arc_2)

                        # boolean split into 3 segments
                        vars_0 = vars_1.intersection(vars_2)
                        vars_1.difference_update(vars_0)
                        vars_2.difference_update(vars_0)

                        # if not intersecting, skip to next pair
                        if len(vars_0) == 0:
                            continue

                        # values in each segment
                        vals_0 = {val for var in vars_0 for val in csp_copy.domains[var]}
                        vals_1 = {val for var in vars_1 for val in csp_copy.domains[var]}
                        vals_2 = {val for var in vars_2 for val in csp_copy.domains[var]}
                        vals_0.update({csp_copy.assignment[var] for var in vars_0 if var in csp_copy.assignment})
                        vals_1.update({csp_copy.assignment[var] for var in vars_1 if var in csp_copy.assignment})
                        vals_2.update({csp_copy.assignment[var] for var in vars_2 if var in csp_copy.assignment})

                        # take advantage of fact that intersection is doubly constrained
                        vals_2.difference_update(vals_0.difference(vals_1))
                        vals_1.difference_update(vals_0.difference(vals_2))

                        # remove things that were inferred impossible
                        for var in vars_0:
                            csp_copy.domains[var].intersection_update(vals_0)
                        for var in vars_1:
                            csp_copy.domains[var].intersection_update(vals_1)
                        for var in vars_2:
                            csp_copy.domains[var].intersection_update(vals_2)
            change = csp_copy.domains != temp
        return csp_copy


class Sudoku:
    def __init__(self, puzzle_data):
        self.domains = {}
        self.assignment = {}

        # convert from dict, which is returned by csp solver
        if isinstance(puzzle_data, dict):
            puzzle_data = ''.join(str(puzzle_data[i]) for i in range(81))

        # parse string
        if isinstance(puzzle_data, str):
            i = 0
            for char in puzzle_data:
                if char in '123456789':
                    self.domains[i] = {int(char)}
                    self.assignment[i] = int(char)
                    i += 1
                elif char in '.?0*':
                    self.domains[i] = set(range(1, 10))
                    i += 1
            assert i == 81, 'invalid puzzle input'

    def __str__(self):
        out = ''
        for cell_index in range(81):
            values = self.domains[cell_index]

            # print( grid)
            if cell_index and not cell_index % 27:
                out += '\n------+-------+------'
            if cell_index % 9 and not cell_index % 3:
                out += '| '
            if cell_index and not cell_index % 9:
                out += '\n'

            # print( values)
            if len(values) == 1:
                out += str(list(values)[0]) + ' '
            elif len(values):
                out += '. '
            else:
                out += '! '
        return out

    def make_csp(self):
        # make constraint function
        def constraint(*args):
            for num in set(args):
                if args.count(num) > 1:
                    return False  # constraint failed
            return True  # constraint held

        # make groups
        r = range(9)
        g1 = [tuple(range(i * 9, i * 9 + 9)) for i in r]
        g2 = [tuple(i // 3 * 27 + i % 3 * 3 + j // 3 * 9 + j % 3 for j in r) for i in r]
        groups = g1 + list(zip(*g1)) + g2

        problem = SudokuCSP(self.domains.keys(), self.domains, dict.fromkeys(groups, constraint))

        for var, val in self.assignment.items():
            problem = problem.assign(var, val)

        return problem


def solve_sudoku(sudoku_string):
    # print( formatting)
    print('=' * 40)

    # get data
    sudoku = Sudoku(sudoku_string)
    print('INITIAL')
    print(sudoku)
    sudoku_csp = sudoku.make_csp()
    # print( 'CSP DOMAINS', sudoku_csp.domains)

    # solve
    global assign_count
    assign_count = 0
    t = time.time()
    solution = backtracking_search(sudoku_csp)
    t = time.time() - t

    # print(
    print('SOLUTION')
    print(Sudoku(solution))
    print('TIME (seconds):', t)
    print('ASSIGNMENTS (tries):', assign_count)

    # print( formatting)
    print('=' * 40)
    print('')


# if __name__ == '__main__':
inputs = """
ESCARGOT
    1****7*9*
    *3**2***8
    **96**5**
    **53**9**
    *1**8***2
    6****4***
    3******1*
    *41*****7
    **7***3**

DIABOLICAL
    *9*7**86*
    *31**5*2*
    8*6******
    **7*5***6
    ***3*7***
    5***1*7**
    ******1*9
    *2*6**35*
    *54**8*7*

HARDER
    4173698*5
    *3*******
    ***7*****
    *2*****6*
    ****8*4**
    ****1****
    ***6*3*7*
    5**2*****
    1*4******

MODERATE
    **62*1***
    8******71
    **17***32
    **7*3**4*
    *5*****8*
    *8**4*7**
    46***58**
    17******4
    ***4*65**

GENTLE
    *1*42***5
    **2*71*39
    *******4*
    2*71****6
    ****4****
    6****74*3
    *7*******
    12*73*5**
    3***82*7*

GUESSING
    ***7****3
    *96******
    2**85****
    17*2*4*36
    *6**7**4*
    *826*351*
    ****17**8
    ******25*
    9****2***

SOLVED PUZZLE (CHECK FOR WEIRD ERRORS)
    483921657967345821251876493548132976729564138136798245372689514814253769695417382

BADLY POSED PUZZLE
    483921657...............................................................695417382

BLANK PUZZLE
    .................................................................................

SUPPOSEDLY HARD PUZZLE
    8 ? ? | ? ? ? | ? ? ?
    ? ? 3 | 6 ? ? | ? ? ?
    ? 7 ? | ? 9 ? | 2 ? ?
    - - - + - - - + - - -
    ? 5 ? | ? ? 7 | ? ? ?
    ? ? ? | ? 4 5 | 7 ? ?
    ? ? ? | 1 ? ? | ? 3 ?
    - - - + - - - + - - -
    ? ? 1 | ? ? ? | ? 6 8
    ? ? 8 | 5 ? ? | ? 1 ?
    ? 9 ? | ? ? ? | 4 ? ?

LOOK A FLOWER
    . 2 6 . . . 8 1 .
    3 . . 7 . 8 . . 6
    4 . . . 5 . . . 7
    . 5 . 1 . 7 . 9 .
    . . 3 9 . 5 1 . .
    . 4 . 3 . 2 . 5 .
    1 . . . 3 . . . 2
    5 . . 2 . 4 . . 9
    . 3 8 . . . 4 6 .


""".strip().split('\n\n')

for index, sudoku_data in enumerate(inputs):
    print('TEST CASE', index + 1)
    solve_sudoku(sudoku_data)
