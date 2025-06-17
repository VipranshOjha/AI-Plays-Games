import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

font = pygame.font.SysFont('Aptos', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20  # dont change
SPEED = 15

class SnakeGame:

    def __init__(self, w=720, h=640):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h), pygame.RESIZABLE)

        liveTitle = "Cy-kneck - Get Ready"
        pygame.display.set_caption(liveTitle)
        self.clock = pygame.time.Clock()

        # Load and scale the food image
        self.food_image = pygame.image.load('apple.png')
        self.food_image = pygame.transform.scale(self.food_image, (BLOCK_SIZE, BLOCK_SIZE))

        # init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.moves = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.direction != Direction.RIGHT:  # Check if it's not opposite direction
                        self.direction = Direction.LEFT
                        self.moves += 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                        self.moves += 1
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                        self.moves += 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                        self.moves += 1

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.mainTheme = True
        self.display.fill(WHITE if self.mainTheme == False else BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        # Draw the food using the food image
        self.display.blit(self.food_image, (self.food.x, self.food.y))  # Draw food image

        if self.moves != 0:
            self.average = (self.score / self.moves) * 100
        else:
            self.average = 0

        if self.score == 0:
            pygame.display.set_caption("Cy-kneck Lets Get Started !!")
        elif self.score >= 1:
            pygame.display.set_caption(
                f"Cy-kneck    Score: {self.score}     Moves: {self.moves}      Accuracy: " + "{:.2f}".format(
                    self.average))

        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()
        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()