import pygame
import math
import numpy as np
from src.game.Config import Config
from src.game.Snake import Snake
from src.game.Apple import Apple
from src.ai.AugmentedSnake import AugmentedSnake


class Game:
    def __init__(self, display, genomes=None, config=None, mod='HUMAN'):
        self.display = display
        self.mod = mod

        if self.mod == 'HUMAN':
            self.numSnakes = 1
            self.snakes = np.empty(self.numSnakes, dtype=np.object)
            self.apples = np.empty(self.numSnakes, dtype=np.object)
            self.snakes[0] = Snake(self.display)
            self.apples[0] = Apple(self.display)
            self.apples[0].randomize(self.snakes[0].body)
        else:
            self.numSnakes = len(genomes)
            self.snakes = np.empty(self.numSnakes, dtype=np.object)
            self.apples = np.empty(self.numSnakes, dtype=np.object)
            for i in range(self.numSnakes):
                self.snakes[i] = AugmentedSnake(self.display, genomes[i], config)
                self.apples[i] = Apple(self.display)
                self.apples[i].randomize(self.snakes[i].body)

    def play(self):
        clock = pygame.time.Clock()

        while True:
            self.eventListener()
            self.drawEnvironment()

            for i in range(self.numSnakes):

                if self.mod == "TRAIN" or self.mod == "TRAIN_NO_DRAW" or self.mod == "BEST" or self.mod == "BEST_MEAN_LIFETIME":           # NN controls
                    self.snakes[i].controls(self.apples[i])

                new_apple = self.snakes[i].move(self.apples[i])

                if self.snakes[i].isAlive() and self.mod is not "TRAIN_NO_DRAW":                                                           #drawing methods
                    self.snakes[i].draw()
                    self.snakes[i].draw_body()
                    self.apples[i].draw()

                if new_apple: self.apples[i].randomize(self.snakes[i].body)                                                                 #create a new apple

            if (self.mod == "TRAIN" or self.mod == "TRAIN_NO_DRAW") and all(self.snakes[i].isAlive() == 0 for i in range(self.numSnakes)):  #if all the snakes are dead
                scores = [snake.get_fitness() for snake in self.snakes]                                                                     #return the snakes fitness

                return scores

            if self.mod == "BEST_MEAN_LIFETIME" and all(self.snakes[i].isAlive() == 0 for i in range(self.numSnakes)):
                scores = [snake.lifetime for snake in self.snakes]
                return scores

            pygame.display.update()

            if self.mod is not "TRAIN_NO_DRAW":
                clock.tick(Config['game']['fps'])

    def eventListener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if self.mod == "HUMAN":
                self.snakes[0].controls(event)

    def drawEnvironment(self):
        self.display.fill(Config['colors']['snake'])

        pygame.draw.rect(
            self.display,
            Config['colors']['background'],
            [
                0,
                0,
                Config['game']['size'],
                Config['game']['size'],
            ]
        )