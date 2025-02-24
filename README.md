# Othello Assignment
This repository contains the code for the implenting an automated player(s) for the game of _Othello_. There are three different heuristics used to power the automate players. 

| Heuristic | Description |
|-----------|-------------|
| H0(n) | Number of your pieces - number of opponents pieces |
| H1(n) | Number of your legal move - number of opponents legal moves |
| H2(n) | Number of your pieces - number of opponents pieces, +10 for every corner you can legally play or have a piece placed |

# To Run
In order to run the program, you can either do a quick unit test, making sure the program itself works, run the program raw, allowing for humans or automated players to play, or run depth/heurisitcs tests.

Unit Test: `python3 unit_tests.py`
Make sure `main()` is commented out in the `GameDriver.py` file.

Raw Program: `python3 -m GameDriver player1 player2 rows cols p1_eval_type p1_prune p2_eval_type p2_prune p1_depth p2_depth`
Make sure `main()` is NOT commented out in the `GameDriver.py` file.

| Parameter | Description |
|-----------|-------------|
| `player1/2` | Type of player: "human" or "alphabeta" |
| `rows` | Number of rows in the grid for the game |
| `cols` | Number of columns in the grid for the game |
| `p1/2_eval_type` | Player heuristic: 0 = H0(n), 1 = H1(n), 2 = H2(n) |
| `p1/2_prune` | Allow pruning for player: True/False |
| `p1/2_depth` | Max depth the player may search |

Depth/Heuristic Tests: `python3 -m GameDriver`
Comment out `main()` and uncomment out the function and function call you wish to run (either `searchVSdepth()` or `quality()`) in the `GameDriver.py` file.
