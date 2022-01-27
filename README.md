# N-puzzle-greedy-solver

Implementation of N-puzzle solver using greedy algorithm.

## Requirements
- [Python3](https://www.python.org/downloads/)

## Input specification
Currently, only file input is supported.

Input is structured as follows:

**h m n** <br/>
\<empty line\> <br/>
**initial state** <br/>
\<empty line\> <br/>
**goal state**

, where:
- h - Heuristic number
    - 1 - Number of misplaced tiles
    - 2 - Manhattan distance 
- m - Width of the game board
- n - Height of the game board

Input structure of states is as follows:


**d<sub>0,0</sub> d<sub>1,0</sub> . . . d<sub>m-1,0</sub> <br/>**
**d<sub>0,1</sub> d<sub>1,1</sub> . . . d<sub>m-1,1</sub> <br/>**
**.   .   .   .   .   .   . <br/>**
**.   .   .   .   .   .   . <br/>**
**d<sub>0,n-1</sub> d<sub>1,n-1</sub> . . . d<sub>m-1,n-1</sub>**

, where *d<sub>i,j</sub>* represents number on tile on position [i, j]. Number *d<sub>i,j</sub>* must be from interval <1, m*n-1> and empty tile must be represented by character 'm'.

You can find example input in example_input.txt file.

## User guide
1. Clone the repository
2. Open terminal in project root directory
3. Run <code>python3 n_puzzle_greedy_algo.py</code>
4. Program is up and running. UI of program should be intuitive enough to navigate you through further usage.
