
---

# Flappy Bird NEAT AI

This project implements a NEAT (NeuroEvolution of Augmenting Topologies) AI to play the classic game Flappy Bird. NEAT is a method of evolving artificial neural networks through a genetic algorithm to solve various problems, in this case, playing Flappy Bird.

## Requirements

- Python 3.x
- pygame library
- neat library
- matplotlib library

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure all dependencies are installed.
2. Run the `flappy_bird_ai.py` file:

    ```bash
    python flappy_bird_ai.py
    ```

3. The program will start training the AI using NEAT. You can observe the progress in the console output and in the plotted graphs.
4. Once training is complete, the best performing AI will be saved, and its score will be displayed.

## Configuration

The behavior of the NEAT algorithm and the Flappy Bird game can be configured through the `config-feedforward.txt` file. This file contains parameters such as population size, mutation rates, and neural network structure.

## Customization

You can customize various aspects of the game and AI behavior by modifying the source code. For example, you can adjust the game speed, graphics, neural network structure, and fitness function.

## High Score

The high score achieved by the best performing AI is saved in the `high_score.txt` file. You can monitor and compare high scores across different runs of the program.

