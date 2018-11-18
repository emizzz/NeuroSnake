from src.game.Config import Config


ai_config = {
    "num_generations": 500,
    "mod": "BEST",
    "best_file": "352669510__ffid_1",
    "output_dir": "./src/output/",
    "fitness_func_id": 1,
    "save_data": True,
    "training_params": {
        'starvingTS': (Config['game']['size']/Config['snake']['size'])*8,
        'walls': True,
        'foods': True,
        'self': True
    }
}


'''
    ---------README---------

    num_generations: number of generations for the NEAT algorithm
    
    mod: the valid values are: 
        "TRAIN" : training mode (for training the NEAT alg.)
        "TRAIN_NO_DRAW" : training mode, but without drawing (faster)
        "HUMAN" : human controlled snake (the classic version)
        "BEST" : takes the "best_file" (the best genome) saved after the training process and runs it.
        "BEST_MEAN_LIFETIME" : it runs the best genome 100 times and calculates the lifetime average (if the fitness function changes, the results are no longer comparable, so it is better to use the lifetime value)
        
    best_file: the name of the best file (used for the BEST and BEST_MEAN_LIFETIME mode)
    
    output_dir: the folder for saving the best files 
    
    fitness_func_id: if you want to try different fitness functions you can add them to the fitness_functions array and then select the function id in this section.
    
    save_data: if true the best genome is saved, otherwise nothing is saved.
    
    training_params: the training parameters relative to the AugmentedSnake class:
        starvingTS: above this threshold, the snake dies (this value is incremented every step, but is setted to 0 if the snake eats)
                    (!! this parameter is always TRUE !!)
        walls: the NN considers the walls in the training session (if you change this param, you must change also the NN's architecture in the neatconfig)
        foods: the NN considers the foods in the training session (if you change this param, you must change also the NN's architecture in the neatconfig)
        self: the NN considers the self collisions in the training session (if you change this param, you must change also the NN's architecture in the neatconfig)
        
'''