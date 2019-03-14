from solution import *
from eightPuzzle import *
from fifteenPuzzle import *

#just some sample problems, ordered in (perceived) difficulty
eight_puzzle_problems = (
    eightPuzzleState("START", 0, None, [5, 2, 1, 4, 8, 3, 7, 6, -1]), #16
    eightPuzzleState("START", 0, None, [1, 4, 3, 7, -1, 8, 6, 5, 2]), #18
    eightPuzzleState("START", 0, None, [6, -1, 8, 4, 3, 5, 1, 2, 7]), #23
    eightPuzzleState("START", 0, None, [1, 6, 4, -1, 3, 5, 8, 2, 7]), #27
    eightPuzzleState("START", 0, None, [6, 3, 8, 5, 4, 1, 7, 2, -1]), #28
    eightPuzzleState("START", 0, None, [1, 8, 5, -1, 2, 4, 3, 6, 7]), #29
    eightPuzzleState("START", 0, None, [8, 6, 7, 2, -1, 4, 3, 5, 1]), #30
    eightPuzzleState("START", 0, None, [8, 6, 7, 2, 5, 4, 3, -1, 1]), #31 -- this is the hardest 8puzzle possible!

)
#started from a solved, did a few steps to get to these
fifteen_puzzle_problems = (
    fifteenPuzzleState("START", 0, None, [2, 5, 3, 4, 1, 7, 11, 8, 9, 6, -1, 12, 13, 14, 15, 10]), #18
    fifteenPuzzleState("START", 0, None, [1, 2, 3, 4, 5, 6, 14, 8, 13, -1, 9, 11, 10, 12, 15, 7]), #23
    fifteenPuzzleState("START", 0, None, [1, 10, 6, 4, 5, 9, 2, 8, 13, 12, -1, 7, 14, 11, 3, 15]), #26
    fifteenPuzzleState("START", 0, None, [5, 1, 3, 2, 10, 6, 15, 7, 9, 8, 11, 4, -1, 13, 14, 12]), #31
    fifteenPuzzleState("START", 0, None, [9, 5, 8, 3, 6, -1, 10, 11, 2, 1, 14, 7, 13, 15, 12, 4]), #34
    fifteenPuzzleState("START", 0, None, [5, 9, 1, 3, -1, 11, 2, 7, 10, 13, 12, 4, 6, 15, 8, 14]), #37
    fifteenPuzzleState("START", 0, None, [7, 8, 1, 10, 2, 4, 5, 13, -1, 9, 3, 6, 11, 14, 15, 12]), #48
)

#these will take 80 moves! Testing these takes far, far too long :(
#source: http://kociemba.org/fifteen/fifteensolver.html
hardest_15_puzzle = (
    fifteenPuzzleState("START", 0, None, [-1, 12, 9, 13, 15, 11, 10, 14, 3, 7, 2, 5, 4, 8, 6, 1]),
    fifteenPuzzleState("START", 0, None, [-1, 12, 10, 13, 15, 11, 14, 9, 3, 7, 2, 5, 4, 8, 6, 1]),
    fifteenPuzzleState("START", 0, None, [-1, 12, 14, 13, 15, 11, 9, 10, 8, 3, 6, 2, 4, 7, 5, 1]),
)

#These are very easy 24 puzzles yet still take a fair amount of time. 24-puzzle is not going to be tested, discussed
#further in Limitations and Obstacles section
sample_24_puzzle = (
    nPuzzleState("START", 0, None, 5, [1,2,3,4,5,6,17,23,24,13,11,8,15,18,10,16,22,9,12,20,21,14,7,19,-1]),
    nPuzzleState("START", 0, None, 5, [1,2,3,4,5,6,7,-1,9,10,11,13,8,14,15,16,12,17,18,19,21,22,23,24,20]),
)
"""
TESTING:
Options to test are below. If you want to use IDA*, toggle use_idastar. Toggle whether you want 8puzzle, 15puzzle or both.
Also choose the heuristic function you want to pass in.

Be careful when testing 24 puzzle, it can take very long!!
Heuristics available:
    - heur_misplaced_tiles
    - heur_manhattan_distance
    - heur_linear_conflict
    - heur_n_maxswap
    - heur_tiles_out_of_row_and_column
"""
#Testing options
print_problems = False
test_alternate = True
timebound = 10
print_final_path = False #this will spam a lot
use_idastar = False
test_8puzzle = True
test_15puzzle = True
test_24puzzle = False
heuristic = heur_manhattan_distance

if use_idastar:
    search = "IDA*"
else:
    search = "A*"

if print_problems:
    for x in eight_puzzle_problems, fifteen_puzzle_problems:
        print(x.state_string())

if test_alternate:
    if test_8puzzle:
        for i in range(0, len(eight_puzzle_problems)):
            print("~~Testing 8-puzzle P{} using {} with {}~~".format(i+1, search, determine_heuristic_name(heuristic)))
            s0 = eight_puzzle_problems[i]

            if use_idastar:
                final = idastar(s0, heur_fn=heuristic, timebound=timebound)
            else:
                se = SearchEngine('astar', 'default')
                se.init_search(s0, goal_fn=npuzzle_goal_state, heur_fn=heuristic)
                final = se.search(timebound=timebound)

            if final and print_final_path:
                final.print_path()
            print("\n")

    if test_15puzzle:
        for i in range(0, len(fifteen_puzzle_problems)):
            print("~~Testing 15-puzzle P{} using {} with {}~~".format(i + 1, search, determine_heuristic_name(heuristic)))
            s0 = fifteen_puzzle_problems[i]

            if use_idastar:
                final = idastar(s0, heur_fn=heuristic, timebound=timebound)
            else:
                se = SearchEngine('astar', 'default')
                se.init_search(s0, goal_fn=npuzzle_goal_state, heur_fn=heuristic)
                final = se.search(timebound=timebound)

            if final and print_final_path:
                final.print_path()
            print("\n")

    if test_24puzzle:
        for i in range(0, len(sample_24_puzzle)):
            print("~~Testing 15-puzzle P{} using {} with {}~~".format(i + 1, search, determine_heuristic_name(heuristic)))
            s0 = sample_24_puzzle[i]

            if use_idastar:
                final = idastar(s0, heur_fn=heuristic, timebound=timebound)
            else:
                se = SearchEngine('astar', 'default')
                se.init_search(s0, goal_fn=npuzzle_goal_state, heur_fn=heuristic)
                final = se.search(timebound=timebound)

            if final and print_final_path:
                final.print_path()
            print("\n")
