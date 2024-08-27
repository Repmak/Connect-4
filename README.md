# Connect-4

Connect 4 game written in Python. Pyglet used for the UI.

# Notes
The most recent version (v5) is the best (and should have no bugs or errors). Prior versions are uploaded to this repository too but are not all fully functional and may have poor performance.

# To play the game
To run the final version of the code, download the contents of the folder Connect 4 pyglet v5 and run pyglet_window.py. Ensure that the pyglet library is installed, and that icon.png and backend.py are in the same directory as the main file.

# Self-evaluation
- minimax v1: This algorithm only checks for the next best move. Only immediate wins are found.
- minimax v2: No scores are calculated for any of the generated turns. This algorithm only serves to output all possible turns that can be played (to ensure that tokens are not dropped in a full column, for example).
- minimax v3: The scores for all AI turns are calculated, permitting for the best AI turn to be returned. Player turns are not minimsed though.
- minimax v4: Scores for AI turns are maximised and scores for player turns are minimised. However, the major flaw from this algorithm is that the AI assumes for the best case scenario (which would be that the player plays the worst move every time) which is not realistic.
- minimax v5: Th
- minimax v6: In an attempt to make the algorithm more efficient, finding a win will automatically terminate future turns from this branch to be generated. This performs worse than v5, for the reasons stated later. 
- minimax v7: This algorithm is capable of checking whether a board has already been evaluated (alpha-beta pruning). Unfortunately, this version of the algorithm also performs worse than v5, for the reasons stated later.


- Connect 4 console UI (folder):
- Connect 4 pygame.py:
- Connect 4 pyglet v1.py:
- Connect 4 pyglet v2.py:
- Connect 4 pyglet v3 (folder):
- Connect 4 pyglet v4 (folder):
- Connect 4 pyglet v5 (folder): This is the most recent version of the game. The backend uses the algorithm from minimax v6. The AI is not flawless, due to the efficiency of the backend. That being said, it is not bad either and is capable of beating me roughly 50% of the time. 
self.maxdepths dictates the number of moves the AI simulates into the future. Currently set to 7 to permit the game to run smoothly, but this value can be increased so the AI plays better.

# Why minimax v5 works best, and how the minimax AI can be improved

is not used in the final version of the game because it performs worse than v5 for the following reason: 
