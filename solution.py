
ASSIGNMENTS = []

ROWS = 'ABCDEFGHI'
COLS = '123456789'
TL_BR_DIAG = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
BL_TR_DIAG = ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']
DIAG_UNITS = [TL_BR_DIAG, BL_TR_DIAG]

def cross(val1, val2):
    "Cross product of elements in A and elements in B."
    return [x+y for x in val1 for y in val2]

BOXES = cross(ROWS, COLS)

ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
UNIT_LIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAG_UNITS
UNITS = dict((s, [u for u in UNIT_LIST if s in u]) for s in BOXES)
PEERS = dict((s, set(sum(UNITS[s], []))-set([s])) for s in BOXES)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        ASSIGNMENTS.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The BOXES, e.g., 'A1'
            Values: The value in each box, e.g., '8'.
            If the box has no value, then the value will be '123456789'.
    """
    all_digits = '123456789'
    values = []
    for val in grid:
        if val == '.':
            values.append(all_digits)
        elif val in all_digits:
            values.append(val)
    assert len(values) == 81
    grid_dict = dict(zip(BOXES, values))
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in BOXES)
    line = '+'.join(['-'*(width*3)]*3)
    for row in ROWS:
        print(''.join(values[row+c].center(width)+('|' if c in '36' else '')
                      for c in COLS))
        if row in 'CF':
            print(line)
    return

def find_naked_twins(values):
    """Loop through all the boxed in grid and determin if they are twins within each box's peers.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        a dictionary of the form {'naked_twin_box_name': [array of the unit the twin was found in]}
    """
    result = {}
    for box in BOXES:
        for unit in UNITS[box]:
            for peer in unit:
                # Identify a twin if it is not the same box and
                # it is only 2 digits long and
                # the digits match
                if values[box] == values[peer] and len(values[box]) == 2 and box != peer:
                    result[box] = unit
    return result

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from PEERS.
    """

    # Find all instances of naked twins
    naked_twin_boxes = find_naked_twins(values)
    # Eliminate the naked twins as possibilities for their PEERS
    for naked_twin_box in naked_twin_boxes.keys():
        naked_twin_box_unit = naked_twin_boxes[naked_twin_box]
        digits = values[naked_twin_box]
        for digit in digits:
            for peer in naked_twin_box_unit:
                if values[peer] != values[naked_twin_box] and len(values[peer]) > 1:
                    values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in PEERS[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values

def only_choice(values):
    for unit in UNIT_LIST:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return {}
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    vals = reduce_puzzle(values)
    if vals == {}:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in BOXES):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    box_len, box = min((len(values[s]), s) for s in BOXES if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[box]:
        new_sudoku = vals.copy()
        new_sudoku = assign_value(new_sudoku, box, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    DIAG_SUDOKU_GRID = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(DIAG_SUDOKU_GRID))

    try:
        from visualize import visualize_assignments
        visualize_assignments(ASSIGNMENTS)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
