from src.ai.ai_config import ai_config
import os
import pickle
import numpy as np
import errno
from src.ai import visualize

class Validation:
    def __init__(self):
        pass

    @staticmethod
    def load_data(file_path):
        with (open(ai_config['output_dir'] + file_path + "/bestgenome", "rb")) as openfile:
            while True:
                try:
                    return pickle.load(openfile)
                except EOFError:
                    break

    @staticmethod
    def save_data(stats, config):
        fitness_func = str(ai_config['fitness_func_id'])
        max_fitness = str(stats.best_genome().fitness)
        best_genome = stats.best_genome()

        directory_name = max_fitness +  "__ffid_" + fitness_func
        directory_path = ai_config['output_dir'] + directory_name

        try:
            os.makedirs(directory_path)

            with open(directory_path + '/bestgenome', 'wb') as handle:
                pickle.dump(best_genome, handle, protocol=pickle.HIGHEST_PROTOCOL)
            visualize.plot_stats(stats, ylog=False, view=True, filename=directory_path + "/stats")                      #visualize is a component find in the NEAT examples (https://github.com/CodeReclaimers/neat-python/tree/master/examples)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    @staticmethod
    def mean(_list):
        return np.mean(_list)
