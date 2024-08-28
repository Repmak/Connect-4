# Connect-4
The most recent version of the game is located in the folder Connect 4 pyglet v5. To run the code, download the contents of the folder and run pyglet_window.py. Ensure that the pyglet library is installed, and that icon.png and backend.py are in the same directory as the main file.

Prior versions are uploaded to this repository too but are not all fully functional and will have performance issues.

# Design process
- minimax v1: This algorithm only checks for the next best move. Only immediate wins are found.
- minimax v2: No scores are calculated for any of the generated turns. This algorithm only serves to output all possible turns that can be played (to ensure that tokens are not dropped in full columns, for example).
- minimax v3: The scores for all AI turns are calculated, permitting for the best AI turn to be returned. However, player turns are not minimsed yet.
- minimax v4: Scores for AI turns are maximised and scores for player turns are minimised. However, there is a major flaw in that the AI assumes for the best case scenario (which would be that the player plays the worst possible move every time), which is not realistic.
- minimax v5: This algorithm performs the best. Only the best player move(s) is/are branched out. This improves the efficiency of the algorithm by discarding moves with a poor score. This essentially means that the algorithm always assumes that the player will always play the best move possible.
- minimax v6: In an attempt to make the algorithm more efficient, finding a win will automatically terminate future turns from this branch to be generated. This performs worse than v5, for reasons stated later.
- minimax v7: This algorithm is capable of checking whether a board has already been evaluated (alpha-beta pruning). Unfortunately, this version of the algorithm also performs worse than v5, for reasons stated later.
- Connect 4 console UI (folder): This version has the AI randomly choose one of the available columns. This version mainly served to design an efficient function for checking when the game is over, which is implemented in later versions of the code.
- Connect 4 pygame.py: This version uses pygame for displaying the UI, though it was never fully completed. Just like in the previous version, the AI randomly chooses a column. I did attempt to use the class Token to model the token at the top of the screen, which would then be called from the class Connect4. This design did not end up being used in the final version of my code.
- Connect 4 pyglet v1.py: This version uses pyglet for displaying the UI, though it was never fully completed. 
- Connect 4 pyglet v2.py: The UI in this version is nearly fully completed, and does not change much throughout future versions. The AI randomly chooses a column for its turn.
- Connect 4 pyglet v3 (folder): This version makes use of two classes to separate the front end and backend code. In this version, the AI still does not make use of a minimax algorithm, though the structure of the current code will permit future versions of the code to remain readable and modular.
- Connect 4 pyglet v4 (folder): This version makes use of a minimax algorithm. There are still some minor improvements that are made in the latest version.
- Connect 4 pyglet v5 (folder): This is the most recent version of the game. The backend uses the algorithm from minimax v5. The AI is not perfect and is capable of winning against me roughly 50% of the time.

# Self-evaluation: why minimax v5 works best and how my algorithm can be improved
Firstly, let's address why minimax v6 causes the AI to perform worse. By terminating a branch from generating future turns once a win is found, the algorithm will not be able to check for forced wins through 2 or more threats. This is simply because the 2nd, 3rd, etc win will never be identified since the branch will have already been interrupted.

Secondly, here is why implementing alpha-beta pruning in minimax v7 causes the AI to perform worse. After a win is found, an arbitrarily large value is added to the score. This value is weighted accordingly depending on how far down the tree the move being predicted is. For example, finding a win on the very next move guarantees that the AI will win, so the value added to the score will be very large. If a win is found on the 7th turn into the future, the value added to the score will be smaller since this win is not guaranteed. This is becuse many different moves can be made throughout the next 6 moves, ultimately not guaranteeing this win. Now that the scoring system has been explained, we can go over why alpha-beta pruning causes the AI to perform worse. 

In minimax v7, boards that have already been evaluated will be not be re-evaluated to improve efficiency. However, due to the scoring system relying on how far down the tree a win is found, two matching boards will not necessarily return the same scores, since the time at which the win was found may be different. This is fairly obvious, since finding a win sooner than later is going to be the best case scenario.

The most obvious change that can be made to improve the AI is to increase the value of self.maxdepth. This variable dictates the number of moves the AI simulates into the future. Currently, it is set to 7 to permit the game to run smoothly (i.e. not too much delay in the AI's turn) while still being reasonably smart. Increasing this value will permit the AI to predict moves further into the future, permitting it to win more often. Also, writing the minimax algorithm in a compiled language rather than an interpreted language should result in the code running faster, permitting for moves to be predicted further into the future. This is especially important given the time complexity of the code, which would be 7^7 as there are 7 columns (7 possible moves) and a value of 7 set to self.maxdepth. Lastly, the score weighting can be tweaked, to make the AI play in a more offensive or defensive manner, for example.

In regards to the efficiency of my algorithm, I would argue that the algorithm is already fairly efficient. For example, discarding player moves with a bad score reduces the number of moves that are generated into the future, by assuming that the player will always play the best move. While testing, I found that this change has a large impact on reducing the thinking time of the AI while still keeping it just as smart. Also, the use of the string self.turns permits for checking for full columns, dropping tokens, and much more, while not having to use the 2D array self.board. For example, dropping a token using self.board involves using a loop to check each filled position until an available slot is found. Instead, counting the number of occurrences of a token in self.turns will return the number of slots filled in a given column, quickly permitting for the next slot to be filled. Small changes like this make the code slightly shorter and easier to read. Finally, identifying an immediate win (i.e. win found at depth 1) will automatically return this move to be played by the AI, terminating any redundant future turns from being generated.
