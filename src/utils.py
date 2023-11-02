def tuple_add(t1, t2):
    """
    Takes two tuples of length 2 and adds them to return a new tuple.

    Parameters:
        t1 (tuple[int, int]): the first tuple
        t2 (tuple[int, int]): the second tuple

    Returns:
        (tuple[int, int]): the sum of the input tuples
    """
    x1, y1 = t1
    x2, y2 = t2
    return (x1 + x2, y1 + y2)

def tuple_subtract(t1, t2):
    """
    Takes two tuples of length 2 and subtracts the second tuple from the first
    to return a new tuple.

    Parameters:
        t1 (tuple[int, int]): the first tuple
        t2 (tuple[int, int]): the tuple to be subtracted from the first

    Returns:
        (tuple[int, int]): the difference of the input tuples
    """
    x1, y1 = t1
    x2, y2 = t2
    return (x1 - x2, y1 - y2)

def tuple_avg(t1, t2):
    """
    Takes two tuples of length 2 and averages them to return a new tuple.

    Parameters:
        t1 (tuple[int, int]): the first tuple
        t2 (tuple[int, int]): the second tuple

    Returns:
        (tuple[int, int]): the average of the input tuples
    """
    x1, y1 = t1
    x2, y2 = t2
    x3 = int((x1 + x2)/ 2)
    y3 = int((y1 + y2) / 2)
    return (x3, y3)

def loc_to_idx(loc, board_size):
    """
    Takes a location in the form "E5" and translates it to indices usable
    with the game grid

    Ex: loc_to_idx("B3", 8) -> (5, 1)

    Parameters:
        loc (str): the location in string form (e.g. "E4")
        board_size (int): the side length of the board
    
    Returns:
        (tuple[int, int]): the grid index of the given location
    """
    assert isinstance(loc, str)
    assert sum([d.isdigit() for d in loc]) != 0 # There is at least one number
    assert sum([d.isalpha() for d in loc]) != 0 # There is at least one letter

    # Find division between letters and numbers
    div = 0
    for i, value in enumerate(loc):
        if value.isdigit():
            div = i
            break
    
    # Split string accordingly
    loc_row = int(loc[div:])
    loc_col = loc[:div][::-1] # Reversed for later steps

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    row = board_size - loc_row
    assert 0 <= row and row < board_size

    # Calculate column number from letters
    col = -1
    for i, letter in enumerate(loc_col):
        val = letters.index(letter)
        col += (val + 1) * (26 ** i)
    assert col < board_size

    return row, col

def idx_to_loc(idx, board_size):
    """
    Takes an index in the form "(3, 4)" and translates it to indices usable
    with the game grid

    Ex: loc_to_idx((3, 4), 8) -> "D5"

    Parameters:
        idx (tuple[int, int]): the index of the grid space
        board_size (int): the side length of the board
    
    Returns:
        (str): the location of the space in string form (e.g. "E4")
    """
    assert idx[0] in range(board_size) and idx[1] in range(board_size)

    row = str(board_size - idx[0])

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    idx_col = idx[1]
    col = ""

    if idx_col == 0:
        col = "A"
    else:
        col = letters[idx_col % 26]
        if idx_col >= 26:
            col = letters[idx_col // 26 - 1] + col
    
    return col + row

def col_to_letter(col_idx):
    """
    Takes a column number (zero-indexed) and translates it to the letter(s)
    corresponding to that column

    Ex: col_to_letter(3) -> "D"
        col_to_letter(27) -> "AB"
    
    Parameters:
        col_idx (int): the index of a column
    
    Returns:
        (str): the letter(s) corresponding to that column
    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    col = col_idx
    result = ""

    if col == 0:
        return "A"
    else:
        result = letters[col % 26]
        if col >= 26:
            result = letters[col // 26 - 1] + result
    return result

class Node:
    """
    Class representing a node in a MoveTree
    """
    def __init__(self, loc):
        """
        Initializes a Node with the given location
        """
        self._loc = loc
        self._next_steps = set()
        self._move = None

    def get_loc(self):
        """
        Gets this node's location

        Returns: (Tuple[int, int])
        """
        return self._loc

    def add_next_step(self, next):
        """
        Adds a Node to self._next_steps

        Parameters:
            next (Tuples[int, int]): the step to add
        """
        self._next_steps.add(Node(next))

    def get_next_steps(self):
        """
        Gets this node's next steps

        Returns: (Set[Node])
        """
        return self._next_steps

    def set_move(self, move):
        """
        Sets self._move

        Parameters:
            move (Move): the move corresponding to this Node
        """
        self._move = move

    def get_move(self):
        """
        Gets self._move

        Returns: (Move)
        """
        return self._move

class MoveTree:
    """
    Class representing a decision tree for moves a player could make
    """
    def __init__(self, moves):
        """
        Initializes an empty tree and populates it with the given moves
        """
        self._head = None
        self._populate_tree(moves)
        self._current = self._head

    def _populate_tree(self, moves):
        """
        Adds the Move objects to the tree and attaches each Move to its
        corresponding leaf node (i.e. the leaf of the branch corresponding to
        the sequence of locations in the Move). The moves must all begin at the
        same spot. This method does not check validity of moves.

        Parameters:
            moves (Set[Move]): the set of moves to add to the tree
        """
        for move in moves:
            if self._head is None:
                # If the head hasn't been defined yet
                # Make it the first step of this move
                self._head = Node(move.get_steps()[0])

            locs = move.get_steps()
            current = self._head

            # Trace through Move, adding its steps to the tree
            for i in range(1, len(locs)):
                # For each step
                # Get locations of next Nodes
                next_locs = [nxt.get_loc() for nxt in current.get_next_steps()]
                if locs[i] not in next_locs:
                    # If Move's next step isn't in existing next locations, add it
                    current.add_next_step(locs[i])

                # Set current to the Node corresponding to the next step
                for next_step in current.get_next_steps():
                    if next_step.get_loc() == locs[i]:
                        current = next_step
                        break
                
                # If at a leaf node, set Node's move to the Move that got you there
                if i == len(locs) - 1:
                    current.set_move(move)

    def traverse(self, loc):
        """
        Moves current to Node in next steps whose location is loc and returns
        the Move object associated with the current node (will be a Move if the
        node is a leaf of the tree and None otherwise).

        Parameters:
            loc (Tuple[int, int]): the location to move to
        
        Returns: (Move or None): the Move (or lack thereof) associated with the new node
        """
        # Set current to specified next node
        for next_step in self._current.get_next_steps():
            if next_step.get_loc() == loc:
                self._current = next_step
                # Return the new current Node's move (only not None if this is a leaf node)
                return self._current.get_move()

        # If loc doesn't correspond to a valid next step, raise an error
        raise ValueError

    def _reset(self):
        """
        For debugging purposes, returns current to the root of the tree
        """
        self._current = self._head
    
    def get_current_loc(self):
        """
        Gets the current location

        Returns: (Tuple[int, int])
        """
        return self._current.get_loc()

    def get_next_moves(self):
        """
        Gets the next moves from self._current

        Returns: (Set[Tuple[int, int]])
        """
        next_locs = [nxt.get_loc() for nxt in self._current.get_next_steps()]
        return next_locs
