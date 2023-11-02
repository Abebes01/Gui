"""
Bot for checkers
"""
import random
import math
import copy

import click
import warnings

from checkers import CheckerBoard

class Bot:
    """
    Adjustable bot that picks moves based on a skill and lookahead depth
    """

    def __init__(self, board, color, skill = 1, depth = 1):
        """
        Constructor
        
        Args:
            (Board) board: board for bot to play on (automatically updates with moves)
            (str) color: bot's color
            (float) skill: bot's skill level from 0 to 1
            (int) depth: how many turns ahead the bot will look (default is 1)
        """
        # (Board): the board for the bot to play on
        self._board = board

        # (str): the bot's color, either "black" or "red"
        self._color = color
        
        # (str): the opponent's color, either "black" or "red"
        self._opp_color = "black" if color == "red" else "red"

        # (int): bot skill between 0 and 1 where 0 means making random
        # moves and 1 means always making the best calculated move
        self._skill = skill

        # (int): the bot's lookahead depth in picking moves, independent of skill
        self._depth = depth

    # Wrapper method to only return the best move and not its associated heuristic
    def suggest_move(self):
        """
        Constructs a tree of possible moves (storing the tree between calls had too
        many bugs and could not be safely implemented in time) and then picks the
        "best" move, subject to faulty decision making if at a skill < 1

        Parameters: None

        Returns:
            (Move): the bot's chosen move!
        """
        possible = self._board.get_player_moves(self._color)
        if len(possible) == 0:
            return None
        if len(possible) == 1:
            return list(possible)[0]
        if self._skill == 0:
            return random.choice(list(possible))

        tree = self._get_tree_from(self._board, self._depth, self._color)

        return tree.best_move(self._skill).get_move()
    

    def _get_tree_from(self, board, depth, player, move = None):
        """
        Recursively creates a tree of TNode objects each representing possible
        future moves and returns the root.

        Parameters:
            (Board) board: the board to test different moves on
            (int) depth: how many more bot-opponent move pairs
                should it look at before stopping
            (str) player: whose moves is it looking at for the next
                layer of the tree ("black" or "red")
        """
        possible_moves = board.get_player_moves(player)
        tree = TNode(move, self._get_heuristic(board), player == self._opp_color)

        if len(possible_moves) == 0:
            tree.value = -math.inf
            return tree

        if depth > 0:
            #Update the depth
            if player == self._opp_color:
                depth -= 1

            #Update the player
            player = "black" if player == "red" else "red"
            
            #For each move, make it and recurse
            for move in possible_moves:
                #Update the board
                future = copy.deepcopy(board)
                future.perform_move(move)
                
                child = self._get_tree_from(future, depth, player, move)

                tree.add_child(child)

        return tree
    
    def _get_heuristic(self, board):
        """
        Returns a static evaluation of the board based on some heuristic.
        In this case, it simply counts the number of each player's pieces,
        weighing kings more highly than other piees. Can be tuned further
        to value certain board positions higher if desired.

        Parameters:
            (CheckerBoard) board: the board to evaluate

        Returns:
            (int): an evaluation of the board's state, positive meaning
                the bot is favored over its opponent
        """
        grid = board.get_grid()
        size = len(grid) #board.get_size()
        bot_pieces = 0
        opp_pieces = 0

        for i in range(size):
            for j in range(size):
                piece = grid[i][j]
                if piece is not None:
                    if piece.get_color() == self._color:
                        bot_pieces += 2 if piece.get_is_king() else 1
                    else:
                        opp_pieces += 2 if piece.get_is_king() else 1

        return bot_pieces - opp_pieces
    
    def get_color(self):
        return self._color

"""
Helper class for trees of possible bot moves
"""

class TNode:
    """
    Helpful "node" class for storing moves along with values, in order to construct a tree
    """
    def __init__(self, move, value, is_bot):
        """
        Constructor

        Parameters:
            (Move) move: the move associated with this node of the tree
            (int) value: the initial heuristic assigned to the move
            (bool) is_bot: whether the move was made by the bot or its
                opponent, determines how the minimax algorithm will run
        """
        self._move = move
        self._value = value
        self._is_bot = is_bot
        self._children = []

    def pull_values(self):
        """
        Recursively updates the heuristic value associated with itself and each of
        its children using minimax algorithm (assuming opponent plays optimally)

        Parameters: None

        Returns:
            (int): the move's recalculated value (only used recursively)
        """
        if len(self._children) > 0:
            #If node is the bot's move, pick minimum of values (opponent's best move)
            if self._is_bot:
                self._value = min(self._children, key = lambda node: node.pull_values()).get_value()
            else:
                self._value = max(self._children, key = lambda node: node.pull_values()).get_value()

        return self._value
    
    def best_move(self, skill):
        """
        Picks from the set of possible moves (the node's children) based on a
        given "skill". For instance, a bot of skill 0.5 will randomly choose
        among the best 50% of moves, a bot of skill 1.0 will always choose the
        best move, and a bot of skill 0 will choose entirely randomly.

        Parameters:
            (float) skill: determines how randomly the bot will choose

        Returns:
            (Move): the chosen "best" move (based on skill)
        """
        self.pull_values()
        children_by_weight = sorted(self._children, key = lambda node: node.get_value())

        cutoff = min(math.floor(skill * (len(children_by_weight))),\
            len(children_by_weight) - 1)

        return random.choice(children_by_weight[cutoff:])
    
    def add_child(self, node):
        self._children.append(node)

    def get_move(self):
        return self._move
    
    def get_value(self):
        return self._value
    
    def __str__(self):
        if self.get_move() is None:
            return str("ROOT")
        return str(f"Move: {self.get_move().get_steps()}, Value: {self.get_value()}")
    
    def __repr__(self):
        return str(self)

"""
Simulation Code
"""

def get_material(board, player):
        """
        Returns the number of piees a player has minus
        the number of pieces their opponent has

        Parameters:
            (Board) board: the board to evaluate
            (str) player: the player whose pieces count as positive material

        Returns:
            (int): input player's pieces minus their opponent's pieces
        """
        grid = board.get_grid()
        size = len(grid)
        bot_pieces = 0
        opp_pieces = 0

        for i in range(size):
            for j in range(size):
                piece = grid[i][j]
                if piece is not None:
                    if piece.get_color() == player:
                        bot_pieces += 1
                    else:
                        opp_pieces += 1

        return bot_pieces - opp_pieces

def simulate(board, n, b1 = (1, 1), b2 = (0, 0), turn_limit = -1, display_board = False):
    """
    Simulates multiple games between two bots

    Parameters:
        (Board) board: the board to play on
        (int) n: the number of matches to play
        (tuple[int, int]) b1: skill, depth of bot 1
        (tuple[int, int]) b2: skill, depth of bot 2
        (int) turn_limit: ends game early and judges winner based on number of pieces
        remaining if turn_limit is reached. Default of -1 means no turn limit

    Returns:
        (float): the proportion of games won by bot1
    """
    b1wins = 0
    b2wins = 0
    material_sum = 0
    reset = copy.deepcopy(board)
    for i in range(n):
        # Reset the board
        board = copy.deepcopy(reset)
        turns = 0

        # Initialize bots and assign colors (alternates between games)
        if i % 2 == 0:
            bot1 = Bot(board, "black", b1[0], b1[1])
            bot2 = Bot(board, "red", b2[0], b2[1])
            current = bot1
        else:
            bot1 = Bot(board, "red", b1[0], b1[1])
            bot2 = Bot(board, "black", b2[0], b2[1])
            current = bot2

        if display_board:
            print(board._board)

        # While the game isn't over, make a move
        while board.game_over() is None:
            # If turn limit has been reached, end game early
            if turn_limit != -1 and turns >= turn_limit:
                break

            move = current.suggest_move()
            board.perform_move(move)

            # Update whose turn it is
            if current == bot1:
                current = bot2
            else:
                current = bot1

            if display_board:
                print(board._board)

            turns += 1

        material = get_material(board, bot1._color)

        # If there is a winner, print it and add one to that bot's tally
        winner = board.game_over()
        if winner == bot1.get_color():
            b1wins += 1
            print(f"Game {i} complete, Bot 1 won!")
        elif winner == bot2.get_color():
            b2wins += 1
            print(f"Game {i} complete, Bot 2 won!")
        else:
            if material > 0:
                b1wins += 1
                print(f"Game {i} complete, Bot 1 won on material!")
            elif material < 0:
                b2wins += 1
                print(f"Game {i} complete, Bot 2 won on material!")
            else:
                n -= 1
                print(f"Game {i} complete, bots tied on material!")
        
        material_sum += material

    return b1wins / n, material_sum / n

"""
Command-line Interface Code
"""

@click.command(name="checkers-bot")
@click.option('--num-games',  type=click.INT, default=100)
@click.option('--bot1',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="smart")
@click.option('--bot2',
              type=click.Choice(['random', 'smart'], case_sensitive=False),
              default="random")
@click.option('--b1-skill', type=click.FLOAT, default=-1)
@click.option('--b1-depth', type=click.INT, default=1)
@click.option('--b2-skill', type=click.FLOAT, default=-1)
@click.option('--b2-depth', type=click.INT, default=1)
@click.option('--board-size', type=click.INT, default=2)
@click.option('--turn-limit', type=click.INT, default=500)
@click.option('--display-board', type=click.BOOL, default=False)
@click.option('--material-info', type=click.BOOL, default=True)

def cmd(num_games, bot1, bot2, b1_skill, b1_depth, b2_skill, b2_depth,\
            board_size, turn_limit, display_board, material_info):
    board = CheckerBoard(board_size)
    if b1_skill != -1:
        if b1_skill < 0 or b1_skill > 1:
            raise ValueError('b1-skill must be between 0 and 1')
        if b1_depth < 1:
            raise ValueError('b1-depth must be 1 or higher')
        if b1_depth >= 3:
            warnings.warn('depth of 3 or higher may result in slower simulation runtime')
        b1 = (b1_skill, b1_depth)
    else:
        if bot1 == "random":
            b1 = (0, 0)
        elif bot1 == "smart":
            b1 = (1, 1)
    if b2_skill != -1:
        if b2_skill < 0 or b2_skill > 1:
            raise ValueError('b2-skill must be between 0 and 1')
        if b2_depth < 1:
            raise ValueError('b2-depth must be 1 or higher')
        if b2_depth >= 3:
            warnings.warn('depth of 3 or higher may result in slower simulation runtime')
        b2 = (b2_skill, b2_depth)
    else:
        if bot2 == "random":
            b2 = (0, 0)
        elif bot2 == "smart":
            b2 = (1, 1)

    if board_size >= 4:
        warnings.warn('board size of 4 or higher may result in slower simulation runtime')

    bot1_winrate, material_avg = simulate(board, num_games, b1, b2, turn_limit, display_board)
        
    print(f"Bot1 had {100 * round(bot1_winrate, ndigits=5)}% success against bot 2")

    if material_info:
        print(f"Bot1 ended with {round(material_avg, ndigits=3)} more pieces on average than bot2")

if __name__ == "__main__":
    cmd()
