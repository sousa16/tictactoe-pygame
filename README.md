# tictactoe-pygame

Tic Tac Toe game created using PyGame. 
It can be played on 3 different difficulties and has a 2 Player Mode.

!!! TO PLAY THE GAME, RUN jogodogalopygame.py !!!
(you need the pygame library to do this)

autopickplay.py is the script that picks the computer's chosen play.
jogodogalopygame.py is the script where the GUI is created using PyGame.

autopickplay.py uses a different algorithm for each different difficulty.

Below you can see how the different algorithms were created (* means added from previous algorithm)

Easy Mode:
1 - If center is empty, play center
2 - If a corner is empty, play corner
3 - If a lateral is empty. play lateral

Normal Mode:
1* - If there is a winning play, play it
2* - If you can block the opponent's win, block it
3 - If center is empty, play center
4* - If an opposite corner from your piece is empty, play opposite corner
5 - If a corner is empty, play corner
6 - If a lateral is empty, play lateral

Hard Mode:

1 - If there is a winning play, play it
2 - If you can block the opponent's win, block it
3 - If CPU can create a bifurcation (2 rows/columns/diagonals with one CPU piece each that intersect each other, with an empty intersection), play the intersection
4 - If CPU can block a player's bifurcation, play the intersection of said bifurcation. 
	If there is more than 1 bifurcation, create a 2-in-a-row to force player to defend, only if it doesn't create a bifurcation for the player
5 - If center is empty, play center
6 - If an opposite corner from CPU's piece is empty, play opposite corner
7 - If a corner is empty, play corner
8 - If a lateral is empty, play lateral

More information can be found on the source code's comments

