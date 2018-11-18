import random
import pygame

from src.game.Config import Config
import numpy as np

class Apple:
    def __init__(self, display):
        self.x_pos = 0
        self.y_pos = 0
        self.display = display
        self.size = Config['apple']['size']

    def randomize(self, snake_body):
        rand_val = self.rand_pos()
        while any((snake_body[:] == rand_val).all(1)):              #check if the apple new pos will be on the snake
            rand_val = self.rand_pos()

        self.x_pos = rand_val[0]
        self.y_pos = rand_val[1]

    def rand_pos(self):
        height = Config['game']['size']
        width = Config['game']['size']
        max_x = (height - Config['snake']['size'])
        max_y = (height - Config['snake']['size'])
        return np.array([random.randint(1, round(max_x / self.size)) * self.size, random.randint(1, round(max_y / self.size)) * self.size])

    def draw(self):
        return pygame.draw.rect(
            self.display, 
            Config['colors']['food'],
            [
                self.x_pos,
                self.y_pos,
                Config['apple']['size'],
                Config['apple']['size']
            ]
        )