# This file contains a Graphical User Interface for checkers
#
# Sawiros
#
# CMSC 14200

import os
import sys
import copy
from typing import Union, Dict
from checkers import CheckerBoard
from checkers import Piece
from checkers import Move
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from bot import Bot



class GUIPlayer:
    """
    Simple class to store information about a GUI player

    A GUI player can either a human player using pygame to interact with the board,
    or a bot.
    """


    def __init__(self, n: int, player_type: str, board, color
                 ):
        """ 
        Constructor

        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The Connect-M board
            color: The player's color
        Returns: none
        """
        if player_type == "human":
            self.name = "human"
            self.bot = None
        elif player_type == "bot":
            self.name = "bot"
            self.bot = Bot(board, color)
        self.color = color
        self.board = board
        self.id = n

    def get_color (self):
        """
        Returns the color of the player 

        Parameters: none

        Returns:
            color(str): the color of the player
        """
        return self.color
    
    def get_id (self):
        """
        Returns the ID of the player which will be one, or two.

        Parameters: none

        Returns:
            color(str): the color of the player
        """
        return self.id
    
    def get_bot (self):
        """
        Returns the bot instance associated with the player

        Parameters: none

        Returns:
            bot(Bot): the bot instance associated with the player
        """
        return self.bot


def start_screen(n = 4):
    """

    Draws the home screen user interface with two buttons,
    and waits for user input.

    Parameters:
        n: (int) Scale of board 

    Returns:
        none
    """
    # Initializes pygame
    pygame.init()
    pygame.display.set_caption("Checkers: Home Screen")

    background_music = os.path.join('background.mp3')
    sound = pygame.mixer.Sound(background_music)
    sound.set_volume(0.4)
    click_sound = os.path.join('click.mp3')
    click = pygame.mixer.Sound(click_sound)
    click.set_volume(1)
    surface = pygame.display.set_mode((400, 500))

    # Code simply builds the start screen components through pygame, and initalizes sound affects
    surface.fill((191, 153, 105))
    pygame.draw.rect(surface, (139, 101,76), (80, 250, 240, 100))
    font = pygame.font.SysFont("Arial", 50, bold=True)
    text_surface = font.render("CHECKERS!", True, (255,255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (205, 100)
    surface.blit(text_surface, text_rect)

    # Constructs the buttons and their labels
    font2 = pygame.font.SysFont("Arial", 30)
    second_text_surface = font2.render("START", True, (255, 255, 255))
    text_rect2 = second_text_surface.get_rect()
    text_rect2.center = (140, 298)
    pygame.draw.rect(surface, (217, 178, 130), (90, 250, 100, 100))
    surface.blit(second_text_surface, text_rect2)
    pygame.draw.rect(surface, (217, 178, 130), (210, 250, 100, 100))
    third_text_surface = font2.render("MENU", True, (255, 255, 255))
    text_rect3 = second_text_surface.get_rect()
    text_rect3.center = (260, 298)
    surface.blit(third_text_surface, text_rect3)
    cond = True

    # Enters a while loop to wait until user chooses one of the above options, to enter the next state of the game
    while cond:
        sound.play()
        events = pygame.event.get()
        pygame.time.wait(10)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                sound.stop()
                if x > 90 and y > 250 and x < 190 and y <350:
                    cond = False
                    board = CheckerBoard(4)
                    player1 = GUIPlayer(1, "human", board, "red") 
                    player2 = GUIPlayer(2, "bot", board, "black") 
                    players = {"red": player1, "black": player2}
                    play_checkers(board, players)
                if x > 210 and y > 250 and x < 310 and y < 350:
                    menu(surface, n)

            pygame.display.flip()


def draw_board(surface: pygame.surface.Surface, board, dimensions, turn = None, analyze = False) -> None:
    """
    Draws the current state of the board on the given surface

    Parameters:
        surface: Pygame surface to draw the board on
        board: An instance of the Board class representing the current state of the board
        dimensions: An integer that represents the dimensions of the board
        turn: A string that represents whose turn it is on the board. Default -> None
        analyze: A boolean that determines whether the board is drawn in analysis mode or not. Default -> False

    Returns: none

    """
    # The color scheme is determined based off whether the board is in analysis mode or not
    if analyze:
        color_red = (44,49,66)
        color_beige = (84,91,114)
    else:
        color_red = (86,28,1)
        color_beige = (225,190,130)
    cond = False
    grid = board.get_grid()
    nrows = len(grid)
    sq_size = 400 / nrows
    surface.fill((84,91,114))
    moves_tuples = []

    # Draws the checkerboard pattern through the dimension attribute
    for x in range(dimensions):
        for y in range (dimensions):
            color = color_red if (x+y) % 2 == 0 else color_beige
            pygame.draw.rect(surface, color, (y*sq_size, x*sq_size, sq_size, sq_size))
    if turn is not None:
        moves = board.get_player_moves(turn)
        for x in moves:
            moves_tuples.append(x.get_step(0))

    # Draws the pieces as circles. A white outline distinguishes movable pieces while king pieces also have a gold outline
    color = (255,255,0)
    for x in range(dimensions):
        for y in range (dimensions):
            piece = board.get_piece((int(x), int(y)))
            if color is not None:
                for l in moves_tuples:
                    if l[0] == int(x) and l[1] == int(y):
                        cond = True
            if piece is not None and cond:
                if piece is not None and not piece.get_is_king():
                    color = (70, 4, 4) if piece.get_color() == "red" else (0, 0, 0)
                    pygame.draw.circle(surface, color, (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3)
                    pygame.draw.circle(surface, (255, 255, 255), (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3, width=2)
                elif  piece is not None and piece.get_is_king():
                    color = (70, 4, 4) if piece.get_color() == "red" else (0, 0, 0)
                    pygame.draw.circle(surface, color, (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3)
                    color = (255,215,0)
                    pygame.draw.circle(surface, color, (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3, width=8)
                    pygame.draw.circle(surface, (255, 255, 255), (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3, width=2)
            elif piece is not None and not piece.get_is_king():
                color = (70, 4, 4) if piece.get_color() == "red" else (0, 0, 0)
                pygame.draw.circle(surface, color, (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3)
            elif  piece is not None and piece.get_is_king():
                color = (70, 4, 4) if piece.get_color() == "red" else (0, 0, 0)
                pygame.draw.circle(surface, color, (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3)
                color = (255,215,0)
                pygame.draw.circle(surface, color, (y*sq_size + sq_size/2, x*sq_size + sq_size/2), sq_size/2 - 3, width=8)
            cond = False

    # Draws the components in the additional space below the checkerboards. Draws seperate instructions based off current state of board
    pygame.draw.rect(surface, (139, 101,76), (0, 400, 400, 100))
    font = pygame.font.SysFont("Arial", 20, bold=True)
    text_surface = font.render("ANALYSIS!" if analyze else "CHECKERS!" , True, (255,255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (100, 420)
    surface.blit(text_surface, text_rect)
    font1 = pygame.font.SysFont("Arial", 14, bold=True)
    if analyze:
        instructions_surface = font1.render("Within this analysis tool, you may press " , True, (255,255, 255))
        instructions_surface2 = font1.render("left and right keys on your keyboard to" , True, (255,255, 255))
        instructions_surface3 = font1.render("go back and forth through your moves." , True, (255,255, 255))
        instructions_surface4 = font1.render("After going back, press spacebar" , True, (255,255, 255))
        instructions_surface5 = font1.render("to see the best possible move at the time" , True, (255,255, 255))

        instructions_rect_rect = instructions_surface.get_rect()
        instructions_rect_rect2 = instructions_surface2.get_rect()
        instructions_rect_rect3 = instructions_surface3.get_rect()
        instructions_rect_rect4 = instructions_surface4.get_rect()
        instructions_rect_rect5 = instructions_surface5.get_rect()

        instructions_rect_rect.center = (290, 410)
        instructions_rect_rect2.center = (288, 430)
        instructions_rect_rect3.center = (290, 450)
        instructions_rect_rect4.center = (290, 470)
        instructions_rect_rect5.center = (290, 488)

        surface.blit(instructions_surface, instructions_rect_rect)
        surface.blit(instructions_surface2, instructions_rect_rect2)
        surface.blit(instructions_surface3, instructions_rect_rect3)
        surface.blit(instructions_surface4, instructions_rect_rect4)
        surface.blit(instructions_surface5, instructions_rect_rect5)
        pygame.draw.rect(surface, (139, 0, 0), (50, 440, 100, 50))
        resign = font1.render("Exit", True, (255, 255, 255))
        resign_rect = resign.get_rect()
        resign_rect.center = (100, 462)
        surface.blit(resign, resign_rect)
    else:
        instructions_surface = font1.render("Hello! Click on a piece to move!" , True, (255,255, 255))
        instructions_surface2 = font1.render("For multi-step captures, make" , True, (255,255, 255))
        instructions_surface3 = font1.render("sure to click on every step of the move, " , True, (255,255, 255))
        instructions_surface4 = font1.render("otherwise, you wont capture the pieces" , True, (255,255, 255))
        instructions_surface5 = font1.render("Press left and right keys to navigate history" , True, (255,255, 255))

        instructions_rect_rect = instructions_surface.get_rect()
        instructions_rect_rect2 = instructions_surface2.get_rect()
        instructions_rect_rect3 = instructions_surface3.get_rect()
        instructions_rect_rect4 = instructions_surface4.get_rect()
        instructions_rect_rect5 = instructions_surface5.get_rect()

        instructions_rect_rect.center = (290, 410)
        instructions_rect_rect2.center = (288, 430)
        instructions_rect_rect3.center = (290, 450)
        instructions_rect_rect4.center = (290, 470)
        instructions_rect_rect5.center = (285, 488)

        surface.blit(instructions_surface, instructions_rect_rect)
        surface.blit(instructions_surface2, instructions_rect_rect2)
        surface.blit(instructions_surface3, instructions_rect_rect3)
        surface.blit(instructions_surface4, instructions_rect_rect4)
        surface.blit(instructions_surface5, instructions_rect_rect5)

        pygame.draw.rect(surface, (139, 0, 0), (50, 440, 100, 50))
        resign = font1.render("Resign", True, (255, 255, 255))
        resign_rect = resign.get_rect()
        resign_rect.center = (100, 462)
        surface.blit(resign, resign_rect)

    pygame.display.flip()


def menu_helper(surface, color = (217, 178, 130), n = 1):
    """
    Draws a checkers menu on a given surface

    Parameters: 
        surface (pygame.Surface): the surface to draw the menu on
        color (tuple): the color of the rectangle labled "BOARD SIZE". Defaults to (217, 178, 130)
        n (int): optional parameter to set the size of the board. Defaults to 0
    Returns:
        none
    """

    # Draws the menu, with the "BOARD SIZE" rectangle color depending on the color parameter

    surface.fill((191, 153, 105))
    pygame.draw.rect(surface, (139, 101,76), (80, 110, 240, 250))
    font = pygame.font.SysFont("Arial", 50, bold=True)
    text_surface = font.render("CHECKERS MENU!", True, (255,255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (205, 50)
    surface.blit(text_surface, text_rect)

    font2 = pygame.font.SysFont("Arial", 15)
    second_text_surface = font2.render("TWO PLAYER", True, (255, 255, 255))
    text_rect2 = second_text_surface.get_rect()
    text_rect2.center = (143, 160)
    pygame.draw.rect(surface, (217, 178, 130), (90, 120, 100, 100))
    surface.blit(second_text_surface, text_rect2)

    pygame.draw.rect(surface, (217, 178, 130), (210, 120, 100, 100))
    font3 = pygame.font.SysFont("Arial", 25)
    third_text_surface = font3.render("BOT", True, (255, 255, 255))
    text_rect3 = second_text_surface.get_rect()
    text_rect3.center = (280, 155)
    surface.blit(third_text_surface, text_rect3)

    font2 = pygame.font.SysFont("Arial", 15)
    second_text_surface = font2.render("BOARD SIZE", True, (255, 255, 255))
    text_rect2 = second_text_surface.get_rect()
    text_rect2.center = (143, 260)
    font2 = pygame.font.SysFont("Arial", 15)
    input_box = pygame.draw.rect(surface, color, (90, 240, 100, 100))
    surface.blit(second_text_surface, text_rect2)

    pygame.draw.rect(surface, (217, 178, 130), (210, 240, 100, 100))
    font3 = pygame.font.SysFont("Arial", 15)
    third_text_surface = font3.render("BOT vs BOT", True, (255, 255, 255))
    text_rect3 = second_text_surface.get_rect()
    text_rect3.center = (265, 286)
    surface.blit(third_text_surface, text_rect3)

    font1 = pygame.font.SysFont("Arial", 14, bold=True)
    instructions_surface = font1.render("Hi! To increase board size, select" , True, (255,255, 255))
    instructions_surface2 = font1.render("the board size square, and type" , True, (255,255, 255))
    instructions_surface3 = font1.render("the number that you would like to" , True, (255,255, 255))
    instructions_surface4 = font1.render("add. (Ex. n = 1, press 1 gets  1+1= 2)" , True, (255,255, 255))
    instructions_surface5 = font1.render("then, click on a mode to play!" , True, (255,255, 255))

    instructions_rect_rect = instructions_surface.get_rect()
    instructions_rect_rect2 = instructions_surface2.get_rect()
    instructions_rect_rect3 = instructions_surface3.get_rect()
    instructions_rect_rect4 = instructions_surface4.get_rect()
    instructions_rect_rect5 = instructions_surface5.get_rect()

    instructions_rect_rect.center = (290, 410)
    instructions_rect_rect2.center = (288, 430)
    instructions_rect_rect3.center = (290, 450)
    instructions_rect_rect4.center = (290, 470)
    instructions_rect_rect5.center = (290, 488)

    surface.blit(instructions_surface, instructions_rect_rect)
    surface.blit(instructions_surface2, instructions_rect_rect2)
    surface.blit(instructions_surface3, instructions_rect_rect3)
    surface.blit(instructions_surface4, instructions_rect_rect4)
    surface.blit(instructions_surface5, instructions_rect_rect5)

    pygame.draw.rect(surface, (139, 0, 0), (50, 440, 100, 50))
    resign = font1.render("Back", True, (255, 255, 255))
    resign_rect = resign.get_rect()
    resign_rect.center = (100, 462)
    surface.blit(resign, resign_rect)

    # This displays the current size that the user has selected
    larger = pygame.font.SysFont("Arial", 25, bold = True)
    second_text_surface = font2.render(str(n), True, (255, 255, 255))
    text_rect2 = second_text_surface.get_rect()
    text_rect2.center = (143, 290)
    surface.blit(second_text_surface, text_rect2)


def menu(surface, n = 1):
    """
    Displays the Checkers menu given a pygame. Provides options for the user.

    Parameters:
    surface (Pygame surface object): The surface to display the menu on
    n (int): Size of board. Defaults to 1

    Returns:
    None
    """
    menu_helper(surface, n)
    font3 = pygame.font.SysFont("Arial", 15)
    cond = True
    active = False

    # Allows the user to press a button in order to change the size of the board, then select what mode they want to play checkers in.
    while cond:
        events = pygame.event.get()
        pygame.time.wait(1)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if x > 90 and x < 190 and y > 240 and y < 340:
                    active = not active
                elif x > 90 and y > 120 and x < 190 and y < 220:
                    cond = False
                    pygame.quit()
                    board = CheckerBoard(n)
                    player1 = GUIPlayer(1, "human", board, "red") 
                    player2 = GUIPlayer(2, "human", board, "black") 
                    players = {"red": player1, "black": player2}
                    play_checkers(board, players)
                elif x > 210 and x < 310 and y > 120 and y < 220:
                    cond = False
                    pygame.quit()
                    board = CheckerBoard(n)
                    player1 = GUIPlayer(1, "human", board, "red") 
                    player2 = GUIPlayer(2, "bot", board, "black") 
                    players = {"red": player1, "black": player2}
                    play_checkers(board, players)
                elif x > 210 and y > 250 and x < 310 and y < 350:
                    board = CheckerBoard(n)
                    player1 = GUIPlayer(1, "bot", board, "red") 
                    player2 = GUIPlayer(2, "bot", board, "black") 
                    players = {"red": player1, "black": player2}
                    play_checkers(board, players)
                elif x > 50 and y > 440 and x < 150 and y < 490:
                    start_screen(1)
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        n = " "
                        third_text_surface = font3.render("BOT", True, (255, 255, 255))
                    elif event.key == pygame.K_BACKSPACE:
                        n = n[:-1]
                        third_text_surface = font3.render("BOT", True, (255, 255, 255))
                    elif event.unicode.isdigit():
                        text = event.unicode
                        n += int(text)
            menu_helper(surface, (124,252,0) if active else (217, 178, 130), n)
            pygame.display.flip()


def highlight_moves (board, surface, moves, highlight_color = (255, 255, 0), tint = 225):

    """
    Highlights the squares of a board where a set of moves can be made.

    Parameters:
        board (object): An object representing the current state of the board.
        surface (object): An object representing the surface where the board will be drawn.
        moves (list[tuple(int, int)]): A list of moves that can be made on the board.
        highlight_color (tuple): RGB values of the highlight color. Defaults to (255, 255, 0) (yellow)
        tint (int, optional): Transparency level. Defaults to 225
    Returns:
        None

    """

    size = board.get_size()
    sq_size = 400 / size
    for move in moves:
        x = move[0]
        y = move[1]
        rect_surface = pygame.Surface((sq_size, sq_size), pygame.SRCALPHA)
        rect_surface.fill((highlight_color[0], highlight_color[1], highlight_color[2], tint))
        surface.blit(rect_surface, (y * sq_size, x * sq_size))


def end_screen(surface: pygame.surface, previous, current, two_player):
    """
    Constructs the end of game screen with options to play again or analyze the game

    Parameters:
        surface (pygame.surface): The surface to draw the end screen on
        previous(list): The list of previous game states
        current (GUIPlayer): The player turn at the end of the game
        two_player (bool): A bool indicating whether the game was a two player game or not

    Returns:
    None
    """

    # Here we initialize the background music and construct the end of game screen

    background_music = os.path.join('background.mp3')
    sound = pygame.mixer.Sound(background_music)
    sound.set_volume(0.4)

    surface = pygame.display.set_mode((400, 500))
    surface.fill((191, 153, 105))
    pygame.draw.rect(surface, (139, 101,76), (80, 250, 240, 100))
    font = pygame.font.SysFont("Arial", 30, bold=True)
    text_surface = font.render("THANKS FOR PLAYING!", True, (255,255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (205, 100)
    surface.blit(text_surface, text_rect)

    font2 = pygame.font.SysFont("Arial", 15)
    second_text_surface = font2.render("PLAY AGAIN", True, (255, 255, 255))
    text_rect2 = second_text_surface.get_rect()
    text_rect2.center = (140, 298)
    pygame.draw.rect(surface, (217, 178, 130), (90, 250, 100, 100))
    surface.blit(second_text_surface, text_rect2)
    pygame.draw.rect(surface, (217, 178, 130), (210, 250, 100, 100))
    font3 = pygame.font.SysFont("Arial", 15)
    third_text_surface = font2.render("ANALYSIS", True, (255, 255, 255))
    text_rect3 = second_text_surface.get_rect()
    text_rect3.center = (260, 298)
    surface.blit(third_text_surface, text_rect3)
    cond = True
    pygame.display.update()

    while cond:
        sound.play()
        events = pygame.event.get()
        pygame.time.wait(1)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                sound.stop()
                if x > 90 and y > 250 and x < 190 and y <350:
                    cond = False
                    board = CheckerBoard(4)
                    player1 = GUIPlayer(1, "human", board, "red") 
                    player2 = GUIPlayer(2, "bot", board, "black") 
                    players = {"red": player1, "black": player2}
                    menu(surface, 1)
                if x > 210 and y > 250 and x < 310 and y < 350:
                    analyze(surface, previous, current.get_color(), two_player)


            else: pygame.display.flip()
    

def play_checkers(board, players: Dict,
                   bot_delay = 450) -> None:
    """
    Plays a game of checkers with the given board and players.

    Args:
        board (Board): The checkers board on which the game is played.
        players (Dict): A dictionary of players, where the keys are their colors ("red" or "black"), and the values are Player objects. 
        bot_delay (int): The delay (in milliseconds) between bot moves. Defaults to 450.

    Returns:
        None
    """
    # Initalizes pygame, background music and variables needed later on
    pygame.init()
    pygame.display.set_caption("Checkers")
    surface = pygame.display.set_mode((400, 500))
    clock = pygame.time.Clock()
    red = players["red"]
    black = players["black"]
    current = players["red"]
    two_player = False
    if red.bot is None and black.bot is None:
        two_player = True
    sq_size = 400/ board.get_size()
    draw_board(surface, board, board.get_size(), "red")
    original = None
    sound_file = os.path.join('click.mp3')
    sound = pygame.mixer.Sound(sound_file)
    final_set = set()
    previous = [board]
    back_index = 0
    # Enters while loop to check if user is interacting with the surface
    while not board.game_over():
        events = pygame.event.get()
        pygame.time.wait(1)
        column = None
        # Retrieves any action that the user has taken
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                # Rewinds through previous board states that are saved within the previous list as long as it is within the index
                back_index += 1
                if len(previous) > back_index and back_index > 0:
                    draw_board(surface, previous[len(previous)- 1 - back_index], board.get_size())
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                # Forwards through board states that are saved within the previous list as long as it is within the index
                back_index -= 1
                if len(previous) > back_index and back_index > 0:
                    draw_board(surface, previous[len(previous)- 1- back_index], board.get_size())
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if current.bot is None:
                    back_index = 0
                    highlighted_moves = set()
                    col = int(pos[0]/sq_size)
                    row = int(pos[1]/sq_size)
                    first = (col, row)
                    player_set = set()
                    player_moves = board.get_player_moves(current.get_color())
                    for b in player_moves:
                        player_set = player_set.union(set(b.get_steps()))
                    if pos[0] > 50 and pos[1] > 440 and pos[0] < 150 and pos[1] < 490:
                        board.concede(current.get_color())
                    elif pos [1] < 400 and board.get_piece((row,col)) is not None and len(board.get_piece_moves((row, col)))> 0 and current.name == "human" and (row, col) in player_set:
                        if board.get_piece((row,col)).get_color() == current.get_color():
                            final_set = set()
                            draw_board(surface, board, board.get_size(), current.get_color())
                            selected_piece = (row, col)
                            moves = board.get_piece_moves((row, col))
                            iterable_moves = set()
                            if len(moves) > 0:
                                original = (row,col)
                                highlighted_moves = moves
                                for a in highlighted_moves:
                                    final_set = final_set.union(set(a.get_steps()))
                                highlight_moves(board, surface, final_set) 
                                pygame.display.update()
                    elif (row, col) in final_set:
                        # The user has already selected a piece, and has now clicked again initating a piece move
                        previous.append(copy.deepcopy(board))
                        sound.play()
                        temp = Move (original)
                        temp.add_step((int(row),int(col)))
                        board.perform_move(temp)
                        
                        captured = False
                        if len(temp.get_captured()) > 0:
                            captured = True
                        possible_moves = board.get_piece_moves((row,col))
                        possible_captures = False
                        temp_move = Move((int(row),int(col)))
                        for z in possible_moves:
                            possible_captures = board.can_capture((temp_move), z.get_steps()[-1])

                        if not (possible_captures and captured): 
                            if current.get_id() == red.get_id():
                                current = black
                            elif current.get_id() == black.get_id():
                                current = red 

                        # Makes sure only to outline the humans pieces as moveable
                        if current.bot is not None:
                            draw_board(surface, board, board.get_size(), "black" if current.get_color() == "red" else "red")
                        else:
                            draw_board(surface, board, board.get_size(), current.get_color())
                        final_set = set()
                if pos[0] > 50 and pos[1] > 440 and pos[0] < 150 and pos[1] < 490:
                    board.concede(current.get_color())

        if current.bot is not None:
            # Bot makes its move, and a sound plays
            previous.append(copy.deepcopy(board))
            move = current.bot.suggest_move()
            pygame.time.wait(bot_delay)
            if red.bot is not None and black.bot is not None:
                pygame.time.wait(100)
            board.perform_move(move)

            sound.play()
            if current.get_color() == "black":
                current = red
            else:
                current = black
            draw_board(surface, board, board.get_size(), current.get_color())

    end_screen(surface, previous, current, two_player)

    winner = board.game_over()
    if winner is not None:
        print(f"The winner is {winner}!")
    else:
        print("It's a tie!")


def analyze(surface: pygame.surface.Surface, previous_moves, color, two_player):
    """
    Analyzes a game of checkers, based off a list of board states, allowing the user to go back and forth,
    and giving the best move, as decided by a level 4 bot

    Parameters: 
        Surface (pygame.surface.Surface): The surface to draw the analysis on
        previous_moves (list[Board]): A list of game states
        color (str): The color of the current player
        two_player (bool): Whether the game is two, or one player
    Returns:
        none
    """

    position = 0
    current_board =  previous_moves[len(previous_moves)-1]
    draw_board(surface, current_board, previous_moves[len(previous_moves) - 1 - position].get_size(), None, True)
    turn = copy.deepcopy(color)
    while True:
        pygame.time.wait(5)
        events = pygame.event.get()      

        for event in events:
            pygame.time.wait(1)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos =pygame.mouse.get_pos()
                if pos[0] > 50 and pos[1] > 440 and pos[0] < 150 and pos[1] < 490:
                    end_screen(surface, previous_moves, turn, two_player)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                position += 1
                if position < len(previous_moves) - 2 and position > 0:
                    current_board = previous_moves[len(previous_moves) - 1 - position]
                    draw_board(surface, current_board, previous_moves[len(previous_moves) - 1 - position].get_size(), None, True)
                if two_player:
                    if turn == "red":
                        turn = "black"
                    elif turn == "black":
                        turn = "red"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                position -= 1
                if position > 0 and position < len(previous_moves) - 2:
                    current_board = previous_moves[len(previous_moves) - 1 - position]
                    draw_board(surface, current_board, previous_moves[len(previous_moves) - 1 - position].get_size(), None, True)
                if two_player:
                    if turn == "red":
                        turn = "black"
                    elif turn == "black":
                        turn = "red"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Highlights the best possible move according to a level 4 bot whenever the user presses spacebar 
                if position > 0 and position < len(previous_moves) - 2:
                    current_board = previous_moves[len(previous_moves) - 1 - position]
                    analyze_bot = Bot(current_board, turn)
                    one = analyze_bot.suggest_move()
                    suggested_move = one
                    final_set = []
                    for x in range(len(one.get_steps())):
                        final_set.append(one.get_steps()[x])
                    highlight_moves(previous_moves[len(previous_moves) - position -1], surface, final_set, (124, 252, 0), 100)
                    pygame.display.update()



start_screen(1)