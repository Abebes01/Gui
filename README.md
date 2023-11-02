

- Alex Arnell (Game logic)
- Ben Armstrong (Bot)
- Nikhil Patel (TUI)
- Sawiros Abebe (GUI)

# How to run the bot tests:

To run bot simulations, install `click` and then navigate to the src directory and run the following (which as a default will put a skilled bot of depth 1 against a random bot on an 8x8 board):

    python3 bot.py
    
Advanced options:

    --num-games | int (x >= 1) | default = 100
    > how many games the bots should play
    
    --board-size | int (x >= 1) | default = 2
    > how large the board should be (1 means 4x4, 2 means 6x6, 3 means 8x8, etc)
    
    --turn-limit | int (x >= 1) | default = 500
    > how many turns the bots will play before the bot with more pieces is declared the winner
    
    --display-board | bool | default = False
    > whether to display every move on an ASCII board (not recommended for bots that decide quickly)
    
    --material-info | bool | default = True
    > whether to display info about how much material each bot had after each game
    
    --bot1 | str ("random" or "smart") | default = "smart"
    > how bot 1 will choose moves
    
    --bot2 | str ("random" or "smart") | default = "random"
    > how bot 2 will choose moves
    
    --b1-skill | int (0 <= x <= 1) | default = -1
    > how well bot 1 will pick the best move (0.5 means it picks randomly from the top 50% of moves)
    
    --b1-depth | int (x >= 1) | default = 1
    > how many moves ahead bot 1 will look (important: skill must be changed from -1 for this to work)
       
    --b2-skill | int (0 <= x <= 1) | default = -1
    > how well bot 2 will pick the best move (0.5 means it picks randomly from the top 50% of moves)
    
    --b2-depth | int (x >= 1) | default = 1
    > how many moves ahead bot 2 will look (important: skill must be changed from -1 for this to work)

# How to run the TUI:

To run the TUI, install `time`, `click`, and `termcolor`, and then navigate to the src directiory and run one of the following in python3 (the first specified player will go first in the game):

    python3 tui.py

...or, for a more customized game, run the following:

    python3 --player1 <human/smart-bot/random-bot> --player2 <human/smart-bot/random-bot> --bot-delay <bot delay>

# How to run the GUI:

To run the GUI, make sure to install pygame and click. Navigate to the src directiory, and enter the following:
    python3 gui.py

Once the file is running, click Play to begin playing or click on Menu make adjustments to board size, and choose player mode. Change board size by clicking on "BOARD SIZE" button in menu, and typing numeric values to add to the size. After you have the perfect size, press on the player mode you wish to engage.

Keep in mind, analysis only works on games that contain more than 2 moves. To get into analysis mode, the game must be over, so to enter analysis mode, simply resign. Once you resign, you can press "Anlysis". Once in analysis mode, press left and right keyboard keys to navigate through previous moves. Press spacebar and the best move (according to a level 4 bot) will be displayed.

Note: The reason for creating a new bot every move in analysis, is simply because I did not want to burden my teamate in charge of bot, to change the suggest_move feature to take in a board parameter when the deadline was so near. If this was a real world environment I would have done so.

# Changes made:

Design:
- Generalized Board class and put Checkers-specific logic in new CheckerBoard class
    - Moved the following methods to CheckerBoard:
        - can_capture
        - game_over
        - get_movable_pieces
        - get_piece_moves
        - get_player_moves
        - perform_move
        - reset
    - Added the following methods to CheckerBoard:
        - get_size (still returns one int)
        - get_piece (calls Board's get_piece)
        - remove_piece
        - concede
    - Made the following Board methods public:
        - clear_board
        - get_grid
        - get_piece
        - get_size (changed to return a tuple of two ints)
        - add_piece
    - Changed initializer in Board to work with any board size

Game logic (Alex):
- Implemented Board -> CheckerBoard transition (described in Design changes)

Bot (Ben):
- Added documentation for all major methods
- Improved simulations by switching to a terminal command and adding advanced settings
- Generate moves using a tree for cleaner code and a slightly more effective bot
    - Bot now attempts each of opponent's moves rather than assuming based on static heuristic alone
    - Leaves the potential for preset openers being stored in a file
    - Computation time can be lowered in the future using advanced tree algorithms / pruning strategies

TUI (Nikhil):
- Added code comments to TUI code and dependencies in utils.py
- Added "help me" functionality
- Switched board coloring mechanism from built-in (and buggy) ANSI codes to termcolor module
- Made small stylistic changes in accordance with Pylint

GUI (Sawiros):
- Implimented multiple methods to differenciate diffrent states in the game.
    - Menu()
        - Gave a lot more options as to player options (bot v bot, bot v player, player v player)
        - Allowed customization of board size
        - Added back button
    - Start_screen()
        - Creates a nice home screen that allows the user to start a default game of checkers or go to menu for more customization
    - Analyze()
-Updated code:
    - draw_board()
        - Differentiates king pieces
        - Outlines pieces that you can move in white
    - play_checkers()
        - Added resignation feature
        - Move history feature
        - Allows for more flexibility in terms of players
- Added move-history by storing a board in a list after every move.
- Added Analysis feature that shows best reccomended moves after a game
- Included resignation option

Changes based on Feedback:
- Board -> CheckerBoard transition
- TUI: Switched from ANSI code to termcolor
- GUI: Added docstrings, and documentation within text in accordance with the style guide. Seperated diffrent states of board through functions. Shortened down unnessary code.