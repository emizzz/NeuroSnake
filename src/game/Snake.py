import pygame
import random
import numpy as np
from src.game.Config import Config


class Snake:
    def __init__(self, display):
        pygame.font.init()
        self.display = display
        self.size = Config['snake']['size']
        self.speed = Config['snake']['speed']
        self.max_size = 1  # must be 1 or >
        self.body = []
        self.alive = True
        self.lifetime = 0
        a = (Config['game']['size']-self.size)/self.size

        x = random.randint(1, (Config['game']['size']-self.size) / self.size) * self.size
        y = random.randint(1, (Config['game']['size']-self.size) / self.size) * self.size

        random_direction = random.choice(list(enumerate([[0, -self.speed], [self.speed, 0], [0, self.speed], [-self.speed, 0] ])))  #take a random direction
        self.direction = np.array(random_direction[1])
        self.pos = np.array([x, y])

        snake_body = self.pos
        build_dir = self.direction

        for i in range(self.max_size):                      #append the init blocks to the body (max_size)
            snake_body = np.add(snake_body, build_dir)
            self.body.append(snake_body)


    def eat(self):
        self.max_size += 1

    def draw(self, x=None, y=None):

        if x is None and y is None:
            x = self.pos[0]
            y = self.pos[1]

        return pygame.draw.rect(
            self.display,
            Config['colors']['snake'],
            [
                x,
                y,
                Config['snake']['size'],
                Config['snake']['size']
            ]
        )

    def draw_body(self):
        for item in self.body:
            pygame.draw.rect(
                self.display,
                Config['colors']['snake'],
                [
                    item[0],
                    item[1],
                    Config['snake']['size'],
                    Config['snake']['size']
                ]
            )

    def move(self, apple):
        new_apple = False

        if self.alive:
            self.body.append((self.pos[0], self.pos[1]))
            self.pos[0] += self.direction[0]
            self.pos[1] += self.direction[1]
            self.lifetime += 1

            if self.appleCollision(apple):
                self.eat()
                new_apple = True

            if len(self.body) > self.max_size:
                del(self.body[0])

            if self.wallCollision() or self.selfCollision():
                self.alive = False

        return new_apple

    # Detect collison with wall
    def wallCollision(self, x=None, y=None):

        if x is None and y is None:
            x = self.pos[0]
            y = self.pos[1]

        if (
            x < 0 or
            y < 0 or
            x + Config['snake']['size'] > Config['game']['size'] or
            y + Config['snake']['size'] > Config['game']['size']
        ):
            return True

        return False

    # Detect collision with apple
    def appleCollision(self, apple, x=None, y=None):

        if x is None and y is None:
            x = self.pos[0]
            y = self.pos[1]

        if (
            x < apple.x_pos+Config['apple']['size'] and
            x > apple.x_pos-Config['apple']['size'] and
            y < apple.y_pos+Config['apple']['size'] and
            y > apple.y_pos - Config['apple']['size']
        ):
            return True
        return False

    # Collide with Self
    def selfCollision(self, x=None, y=None):
        if x is None and y is None:
            x = self.pos[0]
            y = self.pos[1]

        if len(self.body) >= 1:
            for cell in self.body:
                if x == cell[0] and y == cell[1]:
                    return True
        return False

    def controls(self, event):

        if self.isAlive():
            if event.type == pygame.KEYDOWN and self.isAlive():
                if event.key == pygame.K_LEFT:
                    self.direction = self.left_step(self.direction)

                elif event.key == pygame.K_RIGHT:
                    self.direction = self.right_step(self.direction)

    def left_step(self, direction):
        new_direction = np.array(direction)
        new_direction[0] = direction[1]
        new_direction[1] = -direction[0]
        return new_direction

    def right_step(self, direction):
        new_direction = np.array(direction)
        new_direction[0] = -direction[1]
        new_direction[1] = direction[0]
        return new_direction

    def isAlive(self):
        return self.alive

