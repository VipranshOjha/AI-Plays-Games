import neat
import pygame
import os
import pickle
from SnakeGame import SnakeGameAI, Point, Direction
from TrainingGraph import plot

CONFIG_PATH = "neat-config.txt"

# Evaluate a single genome

def eval_genomes(genomes, config):
    global global_plot_scores, global_plot_mean_scores
    global_plot_scores = []
    global_plot_mean_scores = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = SnakeGameAI()
        
        fitness = 0
        # Calculate initial distance to food
        old_distance = abs(game.head.x - game.food.x) + abs(game.head.y - game.food.y)

        while True:
            state = get_state(game)
            output = net.activate(state)
            final_move = get_action_from_output(output)

            reward, done, score = game.play_step(final_move)
            fitness += reward

            # Bonus for staying alive (but not too much)
            fitness += 0.1

            # Extra bonus for getting food
            if reward == 10:
                fitness += 50

            # Calculate new distance to food
            new_distance = abs(game.head.x - game.food.x) + abs(game.head.y - game.food.y)
            if new_distance < old_distance:
                fitness += 1  # Reward getting closer to food

            # Update old_distance for the next iteration
            old_distance = new_distance

            if done:
                break

        genome.fitness = fitness
        print(f"Genome {genome_id} -> Score: {score}, Fitness: {fitness}")

    # Compute best and mean scores after processing all genomes
    scores = [g.fitness for _, g in genomes]
    best = max(scores)
    mean = sum(scores) / len(scores)

    global_plot_scores.append(best)
    global_plot_mean_scores.append(mean)

    # Plot the scores
    plot(global_plot_scores, global_plot_mean_scores)

# Convert game state into NEAT input (11-dim)
def get_state(game):
    head = game.snake[0]
    point_l = Point(head.x - 20, head.y)
    point_r = Point(head.x + 20, head.y)
    point_u = Point(head.x, head.y - 20)
    point_d = Point(head.x, head.y + 20)

    dir_l = game.direction == Direction.LEFT
    dir_r = game.direction == Direction.RIGHT
    dir_u = game.direction == Direction.UP
    dir_d = game.direction == Direction.DOWN

    state = [
        # Danger straight
        (dir_r and game.is_collision(point_r)) or
        (dir_l and game.is_collision(point_l)) or
        (dir_u and game.is_collision(point_u)) or
        (dir_d and game.is_collision(point_d)),

        # Danger right
        (dir_u and game.is_collision(point_r)) or
        (dir_d and game.is_collision(point_l)) or
        (dir_l and game.is_collision(point_u)) or
        (dir_r and game.is_collision(point_d)),

        # Danger left
        (dir_d and game.is_collision(point_r)) or
        (dir_u and game.is_collision(point_l)) or
        (dir_r and game.is_collision(point_u)) or
        (dir_l and game.is_collision(point_d)),

        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,

        # Food location
        game.food.x < head.x,  # food left
        game.food.x > head.x,  # food right
        game.food.y < head.y,  # food up
        game.food.y > head.y   # food down
    ]

    return list(map(int, state))

# Get [1, 0, 0] / [0, 1, 0] / [0, 0, 1] from NEAT output
def get_action_from_output(output):
    move = output.index(max(output))
    final_move = [0, 0, 0]
    final_move[move] = 1
    return final_move


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)  # number of generations

    # Save the winning model
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)


if __name__ == '__main__':
    run(CONFIG_PATH)
