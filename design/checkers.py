"""
Classes for implementing Checkers.

Examples:
    1) Creating a board::
        board = CheckerBoard(3)
    2) Check whether a move is feasible for a given piece::
        loc = (2, 1)
        dest = (4, 3)
        feasible = board.can_move(loc, dest) or
        board.can_capture(loc, dest)  
    3) Given a piece on the board, get all valid moves::
        loc = (2, 1)
        valid_moves = board.get_piece_moves(loc)  
    4) Obtain a list of all moves a player can make::
        player = "red"
        board.get_player_moves(player) 
    5) Check if someone has won, find who it is::
        if board.game_over() == "red":
            print("Red wins!")
        elif board.game_over() == "black":
            print("Black wins!")
        elif board.game_over() == "draw":
            print("It's a draw!!")
        else:
            print("The game is not over yet!")
"""
  
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
        raise NotImplementedError
    
    def get_piece_moves(self, loc):
        """
        Given a location, if there is a piece there, it returns the set of valid
        locations it can move to. If there is not a piece, return the empty set.

        Parameters:
            loc (tuple[int, int]): the location of the square in question
        
        Returns: 
            (set[Move]): the set of the piece's possible moves
        """
        raise NotImplementedError
    
    def _get_piece_moves_helper(self, move, piece):
        """
        The recursive call for get_piece_moves.

        Parameters: 
            move (Move): The move being extended
            piece (Piece): The piece corresponding with the move

        Returns: 
            (set[Move]): the set of the piece's possible moves
        """
        raise NotImplementedError
    
    def get_player_moves(self, player_color):
        """
        Given a player, returns a list of all possible moves they can
        make.
        
        Parameters:
            player_color (str): "red" or "black"

        Returns: 
            (set[Move]): the set of all possible moves by a particular player
        """
        raise NotImplementedError

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
        raise NotImplementedError
    
    def game_over(self):
        """
        Checks if the game is over. If it is, return the player who won.
    
        Parameters: none

        Returns: 
            If there is a winner, return their color. Otherwise, returns None
        """
        raise NotImplementedError
    
    def perform_move(self, move):
        """
        Given a Move object, this method performs the move, moving the piece,
        capturing pieces along the way, and potentially crowning a piece.

        Parameters: 
            move (Move): the move being performed

        Returns: None
        """
        raise NotImplementedError
    
    def get_movable_pieces(self, color):
        """
        Returns the locations of the pieces that can move for a given color.

        Parameters:
            color (str): the player's color

        Returns:
            (set[tuple[int, int]]): set of movable piece locations
        """
        raise NotImplementedError
        
    def reset(self):
        """
        Resets the board to its original board state.

        Parameters: none

        Returns: None
        """
        raise NotImplementedError
    
    def get_grid(self):
        """
        Returns the grid representing the checker board

        Parameters: none

        Returns:
            (list[list[Piece or None]]): the grid
        """
        raise NotImplementedError
        
    def get_size(self):
        """
        Returns the side length of the checker board 

        Parameters: none

        Returns:
            size(int): the side length of the board
        """
        raise NotImplementedError
        
    def get_piece(self, loc):
        """
        Returns the piece at a given location, or None if there is no piece
        there.

        Parameters:
            loc (tuple[int, int]): the location of the object being accessed

        Returns:
            Piece, if the location has a piece, otherwie None
        """
    
        raise NotImplementedError
    
    def concede(self, player):
        """
        For use when a player concedes.

        Parameters:
            player (str): the color of the conceding player

        Returns: None
        """
        raise NotImplementedError
    
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
        raise NotImplementedError
    
    def in_grid(self, loc):
        """
        Checks whether index tuple is within the board's bounds.
    
        Parameters:
            loc (tuple[int, int]): the position to evaluate

        Returns: 
            (bool): whether or not the location is in the grid
        """
        raise NotImplementedError

    def remove_piece(self, loc):
        """
        Removes a piece from the grid based off coordinates.

        Parameters: 
            loc (tuple[int, int]): the location of the piece to remove

        Returns: None
        """
        raise NotImplementedError

    def get_size(self):
        """
        Returns the size of the board (its side length).

        Parameters: none

        Returns:
            size(tuple[int, int]): the side lengths of the board
        """
        raise NotImplementedError

    def get_piece(self, loc):
        """
        Returns the piece at a given location, or None if there is no piece
        there.

        Parameters:
            loc (tuple[int, int]): the location of the object being accessed

        Returns:
            Piece, if the location has a piece, otherwie None
        """
        raise NotImplementedError

    def get_grid(self):
        """
        Returns the grid representing the board

        Parameters: none

        Returns:
            (list[list[Piece or None]]): the grid
        """
        raise NotImplementedError


    def clear_board(self):
        """
        Clears the board of pieces, setting each space to None.

        Parameters: none

        Returns: None
        """
        raise NotImplementedError
    
    def __str__(self):
        """
        Returns the string representation of the board. 
        
        Parameters: none

        Returns: 
            (str): the board's string representation
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Returns the string representation of the board. 
        
        Parameters: none

        Returns: 
            (str): the board's string representation
        """
        raise NotImplementedError
    
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

        For example, if this piece is red and not a king, get_moves would
        return [(-1, -1), (-1, 1)] regardless of the piece's location.

        Parameters: none

        Returns:
            (list[tuple[int, int]]): list of move vectors
        """
        raise NotImplementedError

    def get_captures(self):
        """
        Returns the types of capture moves this piece can perform as vectors
        (tuples) from an arbitrary location.

        For example, if this piece is red and not a king, get_captures would
        return [(-2, -2), (-2, 2)] regardless of the piece's location.

        Parameters: none
        
        Returns:
            (list[tuple[int, int]]): list of move vectors
        """
        raise NotImplementedError

    def crown_piece(self):
        """
        Makes this piece a king.

        Parameters: none
        
        Returns: None
        """
        raise NotImplementedError

    def get_color(self):
        """
        Returns the color of the piece.

        Parameters: none

        Returns: 
            (str): "red" or "black" 
        """
        raise NotImplementedError

    def get_is_king(self):
        """
        Returns whether this piece is a king.
        
        Parameters: none

        Returns: 
            (bool): whether this piece is a king
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a string representation of the piece. Kings are represented by
        capital letters. Red pieces are represented by "r" and "R". Black pieces
        are represented by "b" and "B".

        Parameters: none

        Returns: 
            (str): the string representation
        """    
        raise NotImplementedError

    def __repr__(self):
        """
        Returns a string representation of the piece. Kings are represented by
        capital letters. Red pieces are represented by "r" and "R". Black pieces
        are represented by "b" and "B".

        Parameters: none

        Returns: 
            (str): the string representation
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def copy(self):
        """
        Performs a deep copy, returning a new Move object with the same data.

        Parameters: none

        Returns:
            (Move): copied move object
        """
        raise NotImplementedError

    def get_step(self, index):
        """
        Returns the step at a specified index in the move.

        Parameters:
            index (int): the index of the step being accessed

        Returns:
            (tuple(int,int)): the step at the specified index
        """
        raise NotImplementedError

    def get_steps(self):
        """
        Returns the path of the move, including starting location.

        Parameters: none
        
        Returns:
            (list[tuple(int, int)]): list of move path
        """
        raise NotImplementedError
    
    def get_captured(self):
        """
        Returns the captured pieces of the move.

        Parameters: none
        
        Returns:
            (list[tuple(int, int)]): list of locations of moves captured
        """
        raise NotImplementedError
        
    def __str__(self):
        """
        Returns string representation of the move

        Parameters: none

        Returns:
            (str): the string representation
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Returns a string representation of the move.

        Parameters: none

        Returns: 
            (str): the string representation
        """
        raise NotImplementedError
