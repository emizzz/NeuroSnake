import neat
import math
from src.game.Snake import Snake
import numpy as np
from numpy import interp
from src.ai.fitness_functions import fitness_functions
from src.ai.ai_config import ai_config


class AugmentedSnake(Snake):
    def __init__(self, display, genome, config):
        self.fitness = 0.0
        self.starve = 0
        self.brain = neat.nn.FeedForwardNetwork.create(genome, config)
        self.id = genome.key
        self.self_collided = False
        self.food_collided = False
        self.fitness_function = fitness_functions[ai_config['fitness_func_id']]
        self.training_params = ai_config['training_params']

        super().__init__(display)

    def move(self, apple):
        new_apple = False

        if self.alive:
            self.body.append((self.pos[0], self.pos[1]))
            self.pos[0] += self.direction[0]
            self.pos[1] += self.direction[1]
            self.lifetime += 1
            self.starve += 1

            self.starving()

            if self.appleCollision(apple):
                self.eat()
                new_apple = True

            if len(self.body) > self.max_size:
                del(self.body[0])

            if self.wallCollision():
                self.alive = False

            if self.selfCollision():
                self.alive = False
                self.self_collided = True

            if self.appleCollision(apple):
                self.starve = 0
                self.food_collided = True

        if not self.isAlive():
            self.fitness = self.fitness_function(self)

        return new_apple

    def starving(self):
        if self.starve > self.training_params['starvingTS']:
            self.alive = False

    def controls(self, apple):

        if self.isAlive():
            nn_input = self.observe(apple)
            nn_output = self.brain.activate(nn_input)
            direction = np.argmax(nn_output)

            if direction == 0:
                self.direction = self.left_step(self.direction)
            elif direction == 1:
                self.direction = self.direction
            elif direction == 2:
                self.direction = self.right_step(self.direction)

    # Collide with Self
    def futureSelfCollision(self, x=None, y=None):
        if x is None and y is None:
            x = self.pos[0]
            y = self.pos[1]

        if len(self.body) >= 1:
            for i in range(len(self.body)):
                if i != 0:
                    if x == self.body[i][0] and y == self.body[i][1]:
                        return True
            return False

    def get_fitness(self):
        return self.fitness

    def observe(self, apple):
        result = np.empty(0)
        walls = np.empty(0)

        if self.training_params['foods']:
            foods = np.empty(0)

            is_food, where_food = self.where_the_food(apple.x_pos, apple.y_pos)
            foods = np.append(foods, is_food)
            foods = np.append(foods, where_food)

        if self.training_params['self']:
            selfs = np.empty(0)

        left = np.add(self.pos, self.left_step(self.direction))
        ahead = np.add(self.pos, self.direction)
        right = np.add(self.pos, self.right_step(self.direction))
        possible_steps = np.array([left, ahead, right])

        for i, direction in enumerate(possible_steps):

            #--------wall checker--------
            is_wall = 0
            if self.wallCollision(direction[0], direction[1]):
                is_wall = 1
            walls = np.append(walls, is_wall)

            # --------self checker--------
            if self.training_params['self']:
                is_self = 0
                if self.futureSelfCollision(direction[0], direction[1]):
                    is_self = 1
                selfs = np.append(selfs, is_self)

        result = np.append(result, walls)

        if self.training_params['foods']:
            result = np.concatenate((result, foods), axis=None)

        if self.training_params['self']:
            result = np.concatenate((result, selfs), axis=None)

        return result

    def normalize_vector(self, vector):
        return vector / np.linalg.norm(vector)

    def get_angle(self, a, b):
        a = self.normalize_vector(a)
        b = self.normalize_vector(b)
        return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]) / math.pi

    def where_the_food(self, f_x, f_y):
        snake_direction = self.direction
        food_direction = np.array([f_x, f_y]) - np.array(self.pos)

        angle = self.get_angle(snake_direction, food_direction)

        if -0.5 <= angle <= 0.5:                                        #FOV is 180°
            is_food_in_fov = 1
            where_is_the_food = interp(angle, [-0.5, 0.5], [0, 1])
        else:
            is_food_in_fov = 0
            where_is_the_food = -1

        return np.array([is_food_in_fov, where_is_the_food])
