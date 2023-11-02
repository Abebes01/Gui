# Implements a TUI for this Checkers game.

import time
import click
from termcolor import colored

from checkers import CheckerBoard
from bot import Bot
from utils import MoveTree, loc_to_idx, idx_to_loc, col_to_letter, tuple_avg

def help_me():
    """
    Prints a message explaining the different symbols on the board
    """
    print(
    """
    Pieces are represented as letters, b/r for regular black/red pieces
    and B/R for kings. The letters and numbers on the sides of the board
    indicate the coordinate system. When choosing moves, other characters
    will be displayed:
        - yellow = either the pieces that can be moved or the piece that is currently being moved
        - * = the squares to which the currently selected piece can move in the next step
        - x = the opponent's pieces that have been captured during this move
    """)

class TUIPlayer:
    """
    Simple class to store information about a TUI player
    A TUI player can either a human player using the keyboard,
    or a bot.
    """
    def __init__(self, number, player_type, board, color, bot_delay):
        """
        Constructor
        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The Checkerboard
            color: The player's color
            bot_delay: When playing as a bot, an artificial delay
                (in seconds) to wait before making a move.
        """
        # Parses what type of player this is
        if player_type == "human":
            self.name = f"Player {number}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {number}"
            self.bot = Bot(board, color, 0)
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {number}"
            self.bot = Bot(board, color, 1)

        self.board = board
        self.color = color
        self.bot_delay = bot_delay

    def get_move(self, board):
        """
        Gets a move from the player
        If the player is a human player, prompt the player for a column.
        If the player is a bot, ask the bot to suggest a move.

        Parameters:
            board (CheckerBoard): the board on which the game is taking place

        Returns: (Move): the move the player would like to make
        """
        if self.bot is not None:
            # If this player is a bot
            time.sleep(self.bot_delay) # Pause for animation purposes

            # Get the bot's move
            move = self.bot.suggest_move()

            # Prints information about the bot's move
            steps = [idx_to_loc(step, board.get_size()) for step in move.get_steps()]
            captured = [idx_to_loc(pc, board.get_size()) for pc in move.get_captured()]
            if len(captured) == 0:
                captured_str = ""
            else:
                captured_str = " and captured the pieces at " + ", ".join(captured)
            print(f"{self.name} moved from " + " to ".join(steps) + captured_str)

            return move

        else:
            # If this player is a human
            # Ask for a piece to move until a valid piece is given
            while True:
                print_board(board,
                    highlight=board.get_movable_pieces(self.color))

                print("\nType \"help\" for information about the board.")
                loc = input("Which piece would you like to move? (movable pieces in yellow; enter a location, for example A5 or E2): ")
                if loc == "help":
                    help_me()
                    loc = input("Which piece would you like to move? (movable pieces in yellow; enter a location, for example A5 or E2): ")
                try:
                    idx = loc_to_idx(loc, board.get_size())
                except (ValueError, TypeError, AssertionError):
                    # If the location format is incorrect
                    # or the location is out of the board
                    print("Invalid location!")
                    continue

                piece = board.get_piece(idx)

                # Various error messages to help the player make a valid choice
                if piece is None:
                    print("There's no piece there!")
                    continue
                elif piece.get_color() != self.color:
                    print("That's not your piece!")
                    continue
                elif len(board.get_piece_moves(idx)) == 0:
                    print("That piece can't move!")
                    continue
                else:
                    # Make sure they want to move this piece (cannot undo this)
                    print_board(board, highlight={idx})
                    confirm = input(f"Are you sure you want to move your piece at {loc}? (y to confirm) ")
                    if confirm == "y":
                        break
                    else:
                        continue

            # Gets the possible moves for this piece and populates a MoveTree
            moves = board.get_piece_moves(idx)
            tree = MoveTree(moves)

            current = tree.get_current_loc()
            captured = set()

            # Asks questions to determine which Move
            # the player would like to make
            while True:
                # Display the board with the current move in progress
                print_board(board,
                            highlight={idx},
                            captured=captured,
                            moves=set(tree.get_next_moves()),
                            piece=(idx, current))

                # Get the possible next steps
                next_moves = tree.get_next_moves()

                if len(next_moves) == 1:
                    # If there's only one possible next step, perform it
                    if next_moves[0][0] - current[0] in {-2, 2}:
                        captured.add(tuple_avg(current, next_moves[0]))
                    move = tree.traverse(next_moves[0])
                    print(f"Moved to {idx_to_loc(next_moves[0], board.get_size())}")
                    if move is not None:
                        return move
                else:
                    # Otherwise, ask the player which move they would like to choose
                    print("\nType \"help\" for information about the board.")
                    move_loc = input("Where would you like to move? (enter a location, for example A5 or E2): ")
                    if move_loc == "help":
                        help_me()
                        move_loc = input("Where would you like to move? (enter a location, for example A5 or E2): ")
                    try:
                        move_idx = loc_to_idx(move_loc, board.get_size())
                    except (ValueError, TypeError, AssertionError):
                        print("Invalid location!")
                        continue

                    if move_idx in next_moves:
                        # If the requested move is possible
                        # Perform the move and update captured as needed
                        if move_idx[0] - current[0] in {-2, 2}:
                            captured.add(tuple_avg(current, move_idx))
                        move = tree.traverse(move_idx)
                        new_loc = idx_to_loc(next_moves[0], board.get_size())
                        print(f"Moved to {new_loc}")
                        if move is not None:
                            return move
                    else:
                        print("Invalid move!")
                        continue
                current = tree.get_current_loc()
                time.sleep(0.5)

def print_board(board, highlight=None, captured=None, moves=None, piece=None):
    """
    Prints the board to the screen. Lets the player type "help" for info
    on what the board symbols mean.
    
    Parameters:
        board (CheckerBoard): the board to print
        highlight (Set[Tuple[int, int]]): the set of pieces that can be moved
        captured (Set[Tuple[int, int]]): the set of pieces that have been captured ("X")
        moves (Set[Tuple[int, int]]): the set of moves a piece can make ("x")
        piece (Tuple[Tuple[int, int], Tuple[int, int]]): the start and end squares of the move

    Returns: None
    """
    board_grid = board.get_grid()
    nrows = len(board_grid)
    ncols = len(board_grid[0])
    grid = [["" for _ in range(ncols)] for _ in range(nrows)]

    # Convert grid items to strings
    for i in range(nrows):
        for j in range(ncols):
            if board_grid[i][j] is None:
                if (i + j) % 2 == 0:
                    grid[i][j] = "□"
                else:
                    grid[i][j] = "■"
            else:
                piece_str = str(board_grid[i][j])
                color_pieces = {
                    "b": colored("b", "blue"),
                    "B": colored("B", "blue"),
                    "r": colored("r", "red"),
                    "R": colored("R", "red")
                }
                if highlight is None or (highlight is not None and (i, j) not in highlight):
                    # If the piece is not supposed to be yellow
                    grid[i][j] = color_pieces[piece_str]
                else:
                    grid[i][j] = piece_str

    # Display highlighted characters
    if highlight is not None:
        for loc in highlight:
            i, j = loc
            grid[i][j] = colored(grid[i][j], "yellow")

    # Display captured pieces
    if captured is not None:
        for loc in captured:
            i, j = loc
            grid[i][j] = "x"

    # Display moves
    if moves is not None:
        for loc in moves:
            i, j = loc
            grid[i][j] = "*"

    # Display current piece in its current location
    if piece is not None:
        i1, j1 = piece[0]
        i2, j2 = piece[1]
        grid[i2][j2] = grid[i1][j1]
        if piece[0] != piece[1]:
            if (i1 + j1) % 2 == 0:
                grid[i1][j1] = "□"
            else:
                grid[i1][j1] = "■"

    result = ""
    padding = len(str(nrows)) # Left-side whitespace
    for i, row in enumerate(grid):
        # Display each row with row numbers on the left hand side
        row_str = " ".join(row)
        row_num = nrows - i
        result += str(row_num).rjust(padding) + "|" + row_str + "\n"
    # Display bottom line and column letters
    result += " " * padding + "└" + "─" * (ncols * 2) + "\n"
    letter_row = [col_to_letter(i).ljust(2) for i in range(ncols)]
    result += " " * (padding + 1) + "".join(letter_row)

    print(result)

def play_checkers(board, players):
    """
    Plays a game of Checkers on the terminal

    Parameters:
        board (CheckerBoard): The board to play on
        players (Dict[str, TUIPlayer]): A dictionary mapping piece colors to
            TUIPlayer objects
    
    Returns: None
    """
    # The starting player is black
    current = players["black"]

    # Keep playing until there is a winner:
    while board.game_over() is None:
        # Get and perform the next move
        move = current.get_move(board)
        board.perform_move(move)

        if players["black"].bot is not None and players["red"].bot is not None:
            print_board(board)

        # Update the player
        if current.color == "black":
            current = players["red"]
        elif current.color == "red":
            current = players["black"]

    print()
    print_board(board)

    winner = board.game_over()
    if winner != "draw":
        print(f"The winner is {players[winner].name}!")
    else:
        print("It's a tie!")


# Command-line interface

@click.command(name="checkers-tui")
@click.option('--player1',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="human")
@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="smart-bot")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def cmd(player1, player2, bot_delay):
    """
    Runs the game from the command line
    """
    board = CheckerBoard(3)

    player1 = TUIPlayer(1, player1, board, "black", bot_delay)
    player2 = TUIPlayer(2, player2, board, "red", bot_delay)

    players = {"black": player1, "red": player2}

    play_checkers(board, players)


if __name__ == "__main__":
    cmd()
