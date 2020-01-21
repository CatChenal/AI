#from collections import defaultdict


rows = 'ABCDEFGHI'
cols = '123456789'

# boxes == cells of the game board
boxes = [r + c for r in rows for c in cols]

# history must be declared here so that it exists in the assign_values scope
history = {}


def cross(a, b):
    "Cross product of str elements in A and elements in B."
    return [sa+sb for sa in a for sb in b]


def extract_units(unitlist, boxes):
    """Initialize a mapping from box names to the units that the boxes belong to

    Parameters
    ----------
    unitlist(list)
        a list containing "units" (rows, columns, diagonals, etc.) of boxes

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")
    """
    # From Novig's code:
    units = dict((b, [u for u in unitlist if b in u]) for b in boxes)
    return units


def extract_peers(units, boxes):
    """Initialize a mapping from box names to a list of peer boxes (i.e., a flat list
    of boxes that are in a unit together with the key box)

    Parameters
    ----------
    units(dict)
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a set
        containing all boxes that are peers of the key box (boxes that are in a unit
        together with the key box)
    """
    # From Novig's code:              
    peers = dict((b, set(sum(units[b],[]))-set([b])) for b in boxes)                    
    return peers


def display(values):
    """
    Display the values as a 2-D grid.
    :Input: The sudoku in dictionary form
    :Output: str on stdout
    """
    width = 1 + max(len(values[b]) for b in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def grid2values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' for empties.

    Parameters
    ----------
    grid(string)
        Sudoku grid in string form, 81 characters long. Examples:
        
        '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        '2000..........62....1....7...6..8...3...9...7...6..4...4....8....52.....0000....3'
    
    Returns
    -------
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8' or '123456789' if the box has no value.
    """
    if len(grid) != 81:
        msg = 'Wrong len(grid): expected 81 chars, found: {}.'.format(len(grid))
        raise ValueError(msg)

    # in case str has '0' for empties:
    if grid.find('0') > -1:
        grid = grid.replace('0','.')
        
    # this will disqualify a blank board!
    if not grid.replace('.', '').isdigit():
        raise TypeError('Non-digit found in values.')
        
    values = []
    for c in grid:
        if c in cols:
            values.append(c)
        else:
            values.append(cols)
  
    assert len(values) == 81
    return dict(zip(boxes, values))


def values2grid(values):
    """Convert the dictionary board representation to as string

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    """
    lst = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            lst.append(v if len(v) == 1 else '.')
    return ''.join(lst)


def assign_value(values, box, value):
    """You must use this function to update your values dictionary if you want to
    try using the provided visualization tool. This function records each assignment
    (in order) for later reconstruction.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    prev = values2grid(values)
    values[box] = value
    
    if len(value) == 1:
        history[prev] = (prev, (box, value))
        
    return values


def reconstruct(values, history):
    """Returns the solution as a sequence of value assignments 

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    history(dict)
        a dictionary of the form {key: (key, (box, value))} encoding a linked
        list where each element points to the parent and identifies the value
        assignment that connects from the parent to the current state

    Returns
    -------
    list
        a list of (box, value) assignments that can be applied in order to the
        starting Sudoku puzzle to reach the solution
    """
    path = []
    prev = values2grid(values)
    while prev in history:
        prev, step = history[prev]
        path.append(step)
    return path[::-1]
