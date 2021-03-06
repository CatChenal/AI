"""
Module solution.py contains:
  A. The search space reduction strategies:
     eliminate(values)
     only_choice(values)
     naked_twins(values)
  B. The function that runs all the strategies:
     reduce_puzzle(values)
  C. The search function implementing depth-fist-search for
     unsolved puzzle post-reduction:
     search(values)
  D. A wrapper function to solve a game from an input string
     representing the Sudoku grid:
     solve(grid)
  E. The main function executed when the module is run (with
     a sample grid) at the command line:
     main()
"""

from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

d1 = [r+c for (r, c) in list(zip(rows, cols)) ]
d2 = [r+c for (r, c) in list(zip(rows, cols[::-1]))]
diag_units = [d1] + [d2]

unitlist = row_units + column_units + square_units + diag_units

units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle.
    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        Resulting Sudoku in dictionary form after eliminating values from peers.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            if len(values[peer]) > 1:
                values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle.
    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)
    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # This is the translation of the pseudocode provided in pseudocode.md, but without
    # copying the dict, and further amended as per reviewer.

    # Gather the boxes of length 2:
    twos = [b for b in values.keys() if len(values[b]) == 2]
    
    # Gather the same twins from the twos and their peers:
    twins = ( [[boxA, peerA] for boxA in twos
                             for peerA in peers[boxA]
                             if set(values[boxA]) == set(values[peerA])] )

    for boxA, peerA in twins:
        # Delete the two digits from all common peers:
        for p in set(peers[boxA]).intersection(set(peers[peerA])):
            for dgit in values[boxA]:
                values = assign_value(values, p, values[p].replace(dgit,''))
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        n_prev_solved_values = len([box for box in values.keys() if len(values[box]) == 1])
        
        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Naked twins Strategy
        values = naked_twins(values)
        
        # Use the Only Choice Strategy
        values = only_choice(values)
        
        # Check how many boxes have a determined value, to compare
        n_post_solved_values = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = n_prev_solved_values == n_post_solved_values
        
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            #print('\t:: reduce_puzzle :: There is a box with zero available values.')
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    if values is False:
        return False ## Failed earlier
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed
        
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    _, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and 
    # if one returns a value (not False), return that answer!
    for v in values[s]:
        new_values = values.copy()
        
        # does not update history, scope problem?
        #new_values = assign_value(new_values, s, v)
        new_values[s] = v

        result = search(new_values)
        if result: 
            return result


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


def main():
    
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    if result:
        display(result)
    
    
if __name__ == "__main__":
    
    main()

    # Animation?
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
