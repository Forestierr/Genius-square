# Genius Square Solver

![Genius Square](doc/img/SG_Genius-Square_Website_CHB-cover.jpg)

Link to the game : [Genius Square by SMART GAMES](https://www.smartgames.eu/fr/jeux-pour-1-joueur/genius-square)

## Description

The Genius Square Solver is a Python-based implementation of the popular Genius Square puzzle game. 
The game consists of a 6x6 grid and a set of polyomino pieces. 
The objective is to fit all the pieces into the grid while avoiding obstacles, 
which are randomly placed or user-defined.

## Rules of the Game

#### Step 1

Roll the dice and place the 7 blockers into the squares matching the coordinates that appear on the dice.

#### Step 2

Race your opponent to fill the empty spaces on the game board using the 9 puzzle pieces.

#### Step 3

The first player to fill their game board wins the game.

## Features

- **Interactive Gameplay**: Add obstacles by clicking on the grid.
- **Automatic Solver**: Uses a backtracking algorithm to find solutions.
- **Visual Feedback**: Watch the solver place pieces step by step.

## How to Play

1. Run the program using Python.
2. Click on the grid to place obstacles (up to 7).
3. Watch the solver find a solution or reset the game by pressing `R`.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/genius-square-solver.git
   ```
2. Navigate to the project directory:
   ```bash
   cd genius-square-solver
   ```
3. Install the required dependencies:
   ```bash
   pip install pygame
   ```
4. Run the game:
   ```bash
   python src/main.py
   ```

## Screenshots

### Initial Grid
![grid.png](doc/img/grid.png)

### Adding Obstacles
![obstacle.png](doc/img/obstacle.png)

### Solved Puzzle
![genius_square_solver.gif](doc/img/genius_square_solver.gif)

## Technologies Used

- **Python**: Core programming language.
- **Pygame**: For rendering the grid and handling user interactions.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
