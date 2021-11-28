from __future__ import print_function
import os
import time

import neat
import keyboard
import numpy
import visualize

# 2-input XOR inputs and expected outputs.
from src.game.slither_game import SlitherGame


def eval_genomes(genomes, config):
    game = SlitherGame()
    game.start_game("Test", 900, 900)
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        while not game.is_game_running():
            time.sleep(0.01)
        inactive_count = 0
        last_score = 0
        while game.is_game_running():
            if keyboard.is_pressed('ESC'):
                exit(0)
            output = net.activate(numpy.array(game.get_screenshot().resize((100, 76))).flatten())
            print(output)
            game.move_angle(output[0] * 360)
            game.set_boost(output[1] > 0)
            score = game.get_score()
            if score == last_score:
                inactive_count += 1
            else:
                inactive_count = 0
            if inactive_count > 100:
                game.close()
                game.start_game("Test", 900, 900)
                while not game.is_game_running():
                    time.sleep(0.01)
                genome.fitness *= 0.5
                break
            last_score = score
            if score != 0:
                genome.fitness = score
                print("Genome:", genome_id, "Score:", genome.fitness, end="\r")
        game.restart_game()

    game.close()


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
