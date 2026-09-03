# 43. Bundeswettbewerb Informatik
This repository contains my submissions for the **43. Bundeswettbewerb Informatik (BwInf)**. 

In the first round I solved **Problem 1**, **Problem 2** and **Problem 5**.
For the second round, I solved **Problem 1** and **Problem 2**. 
All documentation is written in German, detailing my algorithmic ideas and implementation choices.

* [Round 1 Original Problem Sheet (PDF)](https://bwinf.de/fileadmin/wettbewerbe/bundeswettbewerb/43/1_runde/Aufgaben431.pdf)
* [Round 1 Official Test Cases(.zip)](https://bwinf.de/fileadmin/wettbewerbe/bundeswettbewerb/43/1_runde/43_1.zip)
* [Round 2 Original Problem Sheet (PDF)](https://bwinf.de/fileadmin/wettbewerbe/bundeswettbewerb/43/2_runde/Aufgaben432.pdf)
* [Round 2 Official Test Cases(.zip)](https://bwinf.de/fileadmin/wettbewerbe/bundeswettbewerb/43/2_runde/43_2.zip)

---

## Round 1
The first round focuses on core algorithmic foundations, which I implemented using C# via .NET and Python.
### Round 1 - Problem 1: Hopsitexte
"Hopsitext" required a way to verify a specific text based on jumping patterns. Inspired by Vim, I implemented an interactive console IDE solution to assist the user in generating text that matches the problem constraints.
### Round 1 - Problem 2: Schwierigkeiten
"Schierigkeiten" was a unique problem. Given many difficulty-rankings of past exam-questions, the task is to output a recommended ranking-order, where the first tasks are more likely to be easy, while the last tasks are more likely to be hard. There are different solutions, especially by using a directed graph. Heavily inspired by the chess.com Elo rating system, I solved the problem by creating my own **Elo rating system** and by setting different modifications to reward specific circumstances. With that, I managed to create a program, which delivers very reliable results.
### Round 1 - Problem 5: Das ägyptische Grabmal
I solved this puzzle by modelling the mathematical formulas and time constraints as a state-space graph, navigating it using an algorithm based on Depth-First Search (DFS).

---

## Round 2
The second round handles advanced algorithmic complexity, making it more interesting and requiring deeper optimisation and architectural choices.
### Round 2 - Problem 1: Schmucknachrichten
#### Problem
This problem was one of the most interesting problems I have encountered. Given a string message and a set of available pearls, where each pearl type has a specific size, the goal is to encode the text into an optimal **lossless prefix code** where the total size of the code is minimized. Adding the sizes for the pearls turns the problem from a classic Huffman Coding problem into a **multidimensional knapsack-like variant**, making the problem **NP-hard**.
#### My Solution
A solution to the problem can be generated using a greedy approach. By counting and sorting each symbol based on its frequency, it is possible to recursively create groups made out of symbols and split them into multiple subgroups, where each subgroup corresponds to a code-symbol (pearl type). Highly frequent symbols are intentionally assigned to lighter smaller code-symbols to minimize the total length. By splitting each subgroup until all groups only have a single symbol or at least two subgroups, it is possible to efficiently assign each symbol to a unique prefix code.

---

### Round 2 - Problem 2: Simultane Labyrinthe
#### Problem
Given two unique labyrinths on a 2 dimensional plane where **both playable characters move simultaneously** using identical directional inputs, the goal is to find the shortest sequence of instructions to reach the goal in both labyrinths. In addition to that, there are holes which reset the position of the character for the corresponding labyrinth.
#### My Solution
While Breadth-First Search (BFS) easily finds the shortest path for a single labyrinth, combining two labyrinths creates a massive search space. To optimize this, I calculated the individual optimal paths first and combined them into a **heuristic progression scoring system** combined with BFS. Paths that align closely with individual optimal routes receive higher scores, allowing the search to prioritise optimal paths. To handle holes, falling into a hole penalizes the respective path's score.

---

## Author & License

**Copyright (C) 2026 Tao Zheng**
*Some Rights Reserved.*

All source code and documentation in this repository are licensed under the [GPL 3.0](https://choosealicense.com/licenses/gpl-3.0/). 

**DISCLAIMER: PROVIDED WITHOUT ANY WARRANTY.** <br/>
**There is no official guarantee for the absolute correctness of these solutions.** For official solution hints and scoring guidelines, please visit https://bwinf.de/bundeswettbewerb/aufgabenarchiv/. 