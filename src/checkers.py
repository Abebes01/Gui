from utils import tuple_add, tuple_subtract, tuple_avg

class CheckerBoard:
    """
    Class for representing a checkerboard.
    """
    def __init__(self, n):
        """
        Constructor

        Parameters:
            n (int): the number of rows or pieces each player should have
        """
        
        # (int): the side length of the board
        self._size = 2 * n + 2

        self._board = Board(self._size, self._size)
        self._populate_board(n)

        # (str): the player who conceded
        self._conceded = None

    def _populate_board(self, n):
        """
        Populates the board with pieces.

        Parameters:
            n (int): the number of rows of pieces each player should have.

        Returns: None
        """
        # Populates the first n rows with black pieces
        for row in range(n):
            for col in range(self._size):
                if (row + col) % 2 == 1:
                    self._board.add_piece(Piece("black"), (row, col))

        # Populates the last n rows with red pieces

        for row in range(self._size - n, self._size):
            for col in range(self._size):
                if (row + col) % 2 == 1:
                    self._board.add_piece(Piece("red"), (row, col))

    def get_piece_moves(self, loc):
        """
        Given a location, if there is a piece there, it returns the set of valid
        locations it can move to. If there is not a piece, return the empty set.

        Parameters:
            loc (tuple[int, int]): the location of the square in question
        
        Returns: 
            (set[Move]): the set of the piece's possible moves
        """
        piece = self._board.get_piece(loc)
        base_move = Move(loc)
        capture_jumps = self._get_piece_moves_helper(base_move, piece) 
        if len(capture_jumps) > 0:
            return capture_jumps
        set_moves = set()
        for direction in piece.get_moves():
            dest = tuple_add(loc, direction)
            if self._board.in_grid(dest) and self._board.get_piece(dest) is None:
                new_move = base_move.copy()
                new_move.add_step(dest)
                set_moves.add(new_move)
        return set_moves
    
    def _get_piece_moves_helper(self, move, piece):
        """
        The recursive call for get_piece_moves.

        Parameters: 
            move (Move): The move being extended
            piece (Piece): The piece corresponding with the move

        Returns: 
            (set[Move]): the set of the piece's possible moves
        """
        set_moves = set()
        capture_dests = []
        cur_loc = move.get_steps()[-1]
        for dir in piece.get_captures():
            capture_dests.append(tuple_add(cur_loc, dir))
        for dest in capture_dests:
            if self.can_capture(move, dest):
                new_move = move.copy()
                new_move.add_step(dest)
                new_set = self._get_piece_moves_helper(new_move, piece)
                set_moves = set_moves.union(new_set)
        if set_moves == set() and len(move.get_steps()) > 1:
            set_moves.add(move)
        return set_moves

    def get_player_moves(self, player_color):
        """
        Given a player, returns a list of all possible moves they can
        make.
        
        Parameters:
            player_color (str): "red" or "black"

        Returns: 
            (set[Move]): the set of all possible moves by a particular player
        """
        capture_moves = set()
        normal_moves = set()
        for row in range(self._size):
            for col in range(self._size):
                piece = self._board.get_piece((row, col))
                if piece is not None and piece.get_color() == player_color:
                    piece_moves = self.get_piece_moves((row, col))
                    if not piece_moves == set():
                        if list(piece_moves)[0].get_captured():
                            capture_moves = capture_moves.union(piece_moves)
                        else:
                            normal_moves = normal_moves.union(piece_moves)
        if capture_moves:
            return capture_moves
        else:
            return normal_moves

    def can_capture(self, move, dest):
        """
        Given a move object, this methods checks whether its piece can perform
        an additional capture action by moving to a specified destination.

        Parameters:
            move (Move): a move object
            dest (tuple[int, int]): the move's next location

        Returns:
            (bool): whether the capture is possible
        """
        if (not self._board.in_grid(dest) or 
                                self._board.get_piece(dest) is not None):
            return False
        piece = self._board.get_piece(move.get_steps()[0])
        # Looking at jumped piece
        jumped_loc = tuple_avg(move.get_steps()[-1], dest)
        jumped = self._board.get_piece(jumped_loc)
        if jumped is None or jumped_loc in move.get_captured():
            return False
        return not piece.get_color() == jumped.get_color()

    def game_over(self):
        """
        Checks if the game is over. If it is, return the player who won.
    
        Parameters: none

        Returns: 
            If there is a winner, return their color. Otherwise, returns None
        """
        if self._conceded == "red":
            return "black"
        if self._conceded == "black":
            return "red"
        red_loses = self.get_player_moves("red") == set()
        black_loses = self.get_player_moves("black") == set()
        if red_loses and black_loses:
            return "draw"
        if red_loses:
            return "black"
        if black_loses:
            return "red"
        return None

    def perform_move(self, move):
        """
        Given a Move object, this method performs the move, moving the piece,
        capturing pieces along the way, and potentially crowning a piece.

        Parameters: 
            move (Move): the move being performed

        Returns: None
        """
        first_dest = move.get_steps()[0]
        final_dest = move.get_steps()[-1]
        piece = self._board.get_piece(first_dest)
        if piece.get_color() == "red" and final_dest[0] == 0:
            piece.crown_piece()
        if piece.get_color() == "black" and final_dest[0] == (self._size -1):
            piece.crown_piece()
        self._board.add_piece(piece, final_dest)
        self._board.remove_piece(first_dest)
        for remove_loc in move.get_captured():
            self._board.remove_piece(remove_loc)

    def get_movable_pieces(self, color):
        """
        Returns the locations of the pieces that can move for a given color.

        Parameters:
            color (str): the player's color

        Returns:
            (set[tuple[int, int]]): set of movable piece locations
        """
        possible_moves = self.get_player_moves(color)
        movable_locs = set()
        for move in possible_moves:
            movable_locs.add(move.get_step(0))
        return movable_locs
    
    def reset(self):
        """
        Resets the board to its original board state.

        Parameters: none

        Returns: None
        """
        self._board.clear_board()
        self._populate_board()

    def get_grid(self):
        """
        Returns the grid representing the checker board

        Parameters: none

        Returns:
            (list[list[Piece or None]]): the grid
        """
        return self._board.get_grid()
    
    def get_size(self):
        """
        Returns the side length of the checker board 

        Parameters: none

        Returns:
            size(int): the side length of the board
        """
        return (self._size)
    
    def get_piece(self, loc):
        """
        Returns the piece at a given location, or None if there is no piece
        there.

        Parameters:
            loc (tuple[int, int]): the location of the object being accessed

        Returns:
            Piece, if the location has a piece, otherwie None
        """
    
        return self._board.get_piece(loc)

    def concede(self, player):
        """
        For use when a player concedes.

        Parameters:
            player (str): the color of the conceding player

        Returns: None
        """
        assert player == "red" or "black"
        self._conceded = player

class Board:
    """
    Class for representing a checkers board.
    """
    def __init__(self, r, c):
        """
        Constructor

        Parameters: 
            r (int): the number of rows the board should have.
            c (int): the number of columns the board should have.
        """

        # (int): number of rows of the board
        self._num_rows = r
        # (int): number of columns of the board
        self._num_cols = c

        # (list[list[Piece or None]]): the grid where pieces are stored
        self._grid = []
        for row in range(self._num_rows):
            self._grid.append([])
            for col in range(self._num_cols):
                self._grid[row].append(None)


    def add_piece(self, piece, loc):
        """
        Adds a piece to the board at a particular location.
        
        Parameters: 
            piece (Piece): the piece object to add
            loc (tuple[int, int]): the location of the new piece

        Returns: None
        """
        row, col = loc
        self._grid[row][col] = piece

    def in_grid(self, loc):
        """
        Checks whether index tuple is within the board's bounds.
    
        Parameters:
            loc (tuple[int, int]): the position to evaluate

        Returns: 
            (bool): whether or not the location is in the grid
        """
        row, col = loc
        return not (row >= self._num_rows or row < 0 or
                     col >= self._num_cols or col < 0)


    def remove_piece(self, loc):
        """
        Removes a piece from the grid based off coordinates.

        Parameters: 
            loc (tuple[int, int]): the location of the piece to remove

        Returns: None
        """
        row, col = loc
        self._grid[row][col] = None

    def get_size(self):
        """
        Returns the size of the board (its side length).

        Parameters: none

        Returns:
            size(tuple[int, int]): the side lengths of the board
        """
        return (self._num_rows, self._num_cols)

    def get_piece(self, loc):
        """
        Returns the piece at a given location, or None if there is no piece
        there.

        Parameters:
            loc (tuple[int, int]): the location of the object being accessed

        Returns:
            Piece, if the location has a piece, otherwie None
        """
        row, col = loc
        return self._grid[row][col]

    def get_grid(self):
        """
        Returns the grid representing the board

        Parameters: none

        Returns:
            (list[list[Piece or None]]): the grid
        """
        return self._grid


    def clear_board(self):
        """
        Clears the board of pieces, setting each space to None.

        Parameters: none

        Returns: None
        """
        for r in range(self._num_rows):
            for c in range(self._num_cols):
                self._remove_piece((r, c))
    
    def __str__(self):
        """
        Returns the string representation of the board. 
        
        Parameters: none

        Returns: 
            (str): the board's string representation
        """
        result = ""

        for r in range(self._num_rows):
            for c in range(self._num_cols):
                cell = self._grid[r][c]

                if cell == None:
                    result += "□ "
                elif isinstance(cell, Piece):
                    result += str(cell) + " "
            result += "\n"
        
        return result

    def __repr__(self):
        """
        Returns the string representation of the board. 
        
        Parameters: none

        Returns: 
            (str): the board's string representation
        """
        return str(self)
    
class Piece:
    """
    Class for representing a checkers piece.
    """
    def __init__(self, color, is_king = False):
        """
        Constructor

        Parameters:
            color (str): red or black
        """
        # (str): the color of the piece
        self._color = color

        # (bool): whether or not the piece is a king
        self._is_king = is_king

    def get_moves(self):
        """
        Returns the types of regular moves this piece can perform as vectors
        (tuples) from an arbitrary location.

        For example, if this piece is red and not a king,
        get_moves would return [(-1, -1), (-1, 1)]

        Parameters: none

        Returns:
            (list[tuple[int, int]]): list of move vectors
        """
        red_moves = [(-1, 1), (-1, -1)]
        black_moves = [(1, 1), (1, -1)]
        if self._is_king:
            return red_moves + black_moves
        if self.get_color() == "red":
            return red_moves
        return black_moves

    def get_captures(self):
        """
        Returns the types of capture moves this piece can perform as vectors
        (tuples) from an arbitrary location.

        For example, if this piece is red and not a king,
        get_captures would return [(-2, -2), (-2, 2)]

        Parameters: none
        
        Returns:
            (list[tuple[int, int]]): list of move vectors
        """
        red_captures = [(-2, 2), (-2, -2)]
        black_captures = [(2,2), (2, -2)]
        if self._is_king:
            return red_captures + black_captures
        elif self.get_color() == "red":
            return red_captures
        return black_captures

    def crown_piece(self):
        """
        Makes this piece a king.

        Parameters: none
        
        Returns: None
        """
        self._is_king = True

    def get_color(self):
        """
        Returns the color of the piece.

        Parameters: none

        Returns: 
            (str): "red" or "black" 
        """
        return self._color

    def get_is_king(self):
        """
        Returns whether this piece is a king.
        
        Parameters: none

        Returns: 
            (bool): whether this piece is a king
        """
        return self._is_king

    def __str__(self):
        """
        Returns a string representation of the piece. Kings are represented by
        capital letters. Red pieces are represented by "r" and "R". Black pieces
        are represented by "b" and "B".

        Parameters: none

        Returns: 
            (str): the string representation
        """    
        color_to_char = {"black": "bB", "red": "rR"}
        int_is_king = int(self._is_king)
        return color_to_char[self._color][int_is_king]

    def __repr__(self):
        """
        Returns a string representation of the piece. Kings are represented by
        capital letters. Red pieces are represented by "r" and "R". Black pieces
        are represented by "b" and "B".

        Parameters: none

        Returns: 
            (str): the string representation
        """
        return str(self)

class Move:
    """
    Class for storing a piece's complete move, including any intermediate
    captures.
    """
    def __init__(self, cur):
        """
        Constructor

        Parameters:
            cur (tuple(int, int)): move's starting space
        """
        # (list[tuple(int, int)]): a list of locations visited during the move,
        #  including the starting square
        self._steps = [cur]

        # (list[tuple(int, int)]): a list of locations of pieces captured
        # during the move
        self._captured = []

    def add_step(self, loc):
        """
        Adds a movement step to a given square, without checking whether the
        step is valid or not. Any squares that are jumped over in the step are
        added to captured.

        Parameters:
            loc (tuple(int, int)): location being stepped to

        Returns: None
        """
        last_loc = self._steps[-1]
        if abs(loc[0] - last_loc[0]) == 2:
            self._captured.append(tuple_avg(last_loc, loc))
        self._steps.append(loc)

    def copy(self):
        """
        Performs a deep copy, returning a new Move object with the same data.

        Parameters: none

        Returns:
            (Move): copied move object
        """
        new_move = Move(self._steps[0])
        for loc in self._steps[1:]:
            new_move.add_step(loc)
        return new_move

    def get_step(self, index):
        """
        Returns the step at a specified index in the move.

        Parameters:
            index (int): the index of the step being accessed

        Returns:
            (tuple(int,int)): the step at the specified index
        """
        return self._steps[index]

    def get_steps(self):
        """
        Returns the path of the move, including starting location.

        Parameters: none
        
        Returns:
            (list[tuple(int, int)]): list of move path
        """
        return self._steps
    
    def get_captured(self):
        """
        Returns the captured pieces of the move.

        Parameters: none
        
        Returns:
            (list[tuple(int, int)]): list of locations of moves captured
        """
        return self._captured
        
    def __str__(self):
        """
        Returns string representation of the move

        Parameters: none

        Returns:
            (str): the string representation
        """
        return ("Steps: " + str(self._steps) + "  Captures: " + 
                str(self._captured))

    def __repr__(self):
        """
        Returns a string representation of the move.

        Parameters: none

        Returns: 
            (str): the string representation
        """
        return str(self)
