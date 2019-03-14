import sys

from nPuzzle import *
from search import *


def heur_misplaced_tiles(state):
    """
    https://heuristicswiki.wikispaces.com/Misplaced+Tiles
    """
    hval = 0
    size = state.size
    goal = state.get_goal_state()
    for idx in range(0, size**2):
        if goal[idx] is not state.positions[idx] and state.positions[idx] is not -1:
            hval += 1
    return hval

def get_xy(size, idx):
    """ ~~HELPER~~
    Given size and index, will get you to the xy from a 1D list.
    Ex, [3, 4, 6, 2, -1, 8, 1, 7, 5] and we want xy of index 5 (which is 8)
     3 4 6
     2 _ 8
     1 7 5
    Will return (3,2)
    :param size:
    :param idx:
    :return:
    """
    x = idx % size + 1
    y = idx // size + 1
    return x, y

def heur_manhattan_distance(state):
    """
    https://heuristicswiki.wikispaces.com/Manhattan+Distance
    Manhattan distance of each tile from its current position to desired position in goal (not including blank)
    """
    hval = 0
    size = state.size
    goal = state.get_goal_state()
    for idx in range(0, size**2):
        if goal[idx] is not state.positions[idx] and state.positions[idx] is not -1:
            x1, y1 = get_xy(size, idx)

            goal_index = goal.index(state.positions[idx])
            x2, y2 = get_xy(size, goal_index)

            hval += (abs(x1 - x2) + abs(y1 - y2))
    return hval

def heur_linear_conflict(state):
    """
    https://heuristicswiki.wikispaces.com/Linear+Conflict

    Two tiles tj and tk are in a linear conflict if tj and tk are in the same line,
    the goal positions of tj and tk are both in that line,
    tj is to the right of tk and goal position of tj is to the left of the goal position of tk.
    """
    #start with the manh dist
    hval = 0
    pos = state.positions
    goal = state.get_goal_state()
    size = int(len(pos) ** 0.5)

    for j in range(0, len(pos)):
        for k in range(j, len(pos)):
            if lin_conflict(j, k, goal.index(pos[j]), goal.index(pos[k]), len(pos)):
                hval += 1
            if lin_conflict(k, j, goal.index(pos[k]), goal.index(pos[j]), len(pos)):
                hval += 1
    return hval

def lin_conflict(tj, tk, tj_goal, tk_goal, n):
    if tj // n == tk // n:  # Tiles are on the same row
        return tj // n == tj_goal // n and tj_goal // n == tk_goal // n and tj > tk and tj_goal < tk_goal
    elif tj % n == tk % n:  # Tiles are in the same column
        return tj % n == tj_goal % n and tj_goal % n == tk_goal % n and tj > tk and tj_goal < tk_goal
    else:
        return False

def heur_n_maxswap(state):
    """
        https://heuristicswiki.wikispaces.com/N-MaxSwap
        [3,2,1,4,5,6,7,8,-1], goal = [1,2,3,4,5,6,7,8,-1]
        So swap
    """
    hval = 0
    goal = state.get_goal_state()
    P = state.positions.copy()

    # Until we reach the goal state, swap iteratively P[B[n]] with P[B[B[n]]]
    while P != goal:

        if P.index(-1) is goal.index(-1): #if the blank is in it's correct place
            for i in range(0,len(P)):
                if P.index(P[i]) is not goal.index(P[i]): #a mismatched tile
                    P = swap(i, P.index(-1), P)
                    break
        else: #blank is wrong place
            blank_index = P.index(-1)
            actual_index = P.index(goal[blank_index])
            P = swap(blank_index, actual_index, P)

        hval+=1

    return hval

def swap(index1, index2, lst):
    l = lst.copy()
    l[index1], l[index2] = l[index2], l[index1]
    return l

def heur_tiles_out_of_row_and_column(state):
    """
    https://heuristicswiki.wikispaces.com/Tiles+out+of+row+and+column
    """
    hval = 0
    positions = state.positions
    goal = state.get_goal_state()
    size = state.size

    for i in range(0, len(positions)):
        #i = this index
        cur_column, cur_row = get_xy(size, i)
        goal_column,goal_row = get_xy(size, goal.index(positions[i]))
        if cur_column is not goal_column:
            hval += 1
        if cur_row is not goal_row:
            hval += 1

    return hval

def idastar(initial_state, heur_fn, timebound=10):
    """
    Need to do a DFS and cut off things based on f-value (g + h)
    At each iteration of the search, the cutoff value becomes the smallest f-value that exceeded the cutoff in last iteration
    curBound = an f-value such that any node with a larger f-value is pruned
    smallestNotExplored =
    """
    timeleft = timebound

    se = SearchEngine('depth_first', 'full')
    solution = False
    #let's just start costbound at f-val of initial_state (g-val is 0 so just h-val of initial_state)
    currbound = (sys.maxsize, sys.maxsize, heur_fn(initial_state))
    init_time = os.times()[0]

    while timeleft > 0:
        se.init_search(initial_state, goal_fn=npuzzle_goal_state, heur_fn=heur_fn)
        solution = se.search(timeleft, costbound=currbound)

        if solution:
            print("Total time elapsed for all iterations of IDA*:", timebound - timeleft)
            return solution

        # introduce a cost bound for pruning
        currbound = (sys.maxsize, sys.maxsize, se.smallestNotExplored)
        timeleft -= (os.times()[0] - init_time)
        init_time = os.times()[0]

    print("Total time elapsed for all iterations of IDA*: {}", timebound - timeleft)
    return solution

def determine_heuristic_name(heuristic):
    #Just a helper to be able to print heuristic names
    if heuristic == heur_misplaced_tiles:
        return "Misplaced tile heuristic"
    elif heuristic == heur_manhattan_distance:
        return "Manhattan distance heuristic"
    elif heuristic == heur_linear_conflict:
        return "Linear conflict heuristic"
    elif heuristic == heur_n_maxswap:
        return "N-MaxSwap heuristic"
    elif heuristic == heur_tiles_out_of_row_and_column:
        return "Tiles out of row and column heuristic"
