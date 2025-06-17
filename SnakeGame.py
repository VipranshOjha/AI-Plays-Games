import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)


font = pygame.font.SysFont('arial', 25)

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

BLOCK_SIZE = 60
SPEED = 40


class SnakeGameAI:

    def __init__(self, w=1000, h=800):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        
        self.food_image = pygame.image.load('apple.png')
        self.food_image = pygame.transform.scale(self.food_image, (BLOCK_SIZE, BLOCK_SIZE))
        
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(
            (self.w // (2 * BLOCK_SIZE)) * BLOCK_SIZE,
            (self.h // (2 * BLOCK_SIZE)) * BLOCK_SIZE
        )
        
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        while True:
            x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food = Point(x, y)
            if self.food not in self.snake:  # Ensure food does not overlap with the snake
                break

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        # Fill the background with black
        self.display.fill(BLACK)  # Set background color to black

        # Draw the grid
        for x in range(0, self.w, BLOCK_SIZE):
            pygame.draw.line(self.display, (40, 40, 40), (x, 0), (x, self.h))  # Vertical lines
        for y in range(0, self.h, BLOCK_SIZE):
            pygame.draw.line(self.display, (40, 40, 40), (0, y), (self.w, y))  # Horizontal lines

        # Draw the snake using rectangles
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))  # Snake body
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))  # Snake inner part

        # Draw the food using the food image
        self.display.blit(self.food_image, (self.food.x, self.food.y))  # Draw food image

        # Render the score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

def get_state(game):
    head = game.snake[0]
    point_l = Point(head.x - BLOCK_SIZE, head.y)
    point_r = Point(head.x + BLOCK_SIZE, head.y)
    point_u = Point(head.x, head.y - BLOCK_SIZE)
    point_d = Point(head.x, head.y + BLOCK_SIZE)

    dir_l = game.direction == Direction.LEFT
    dir_r = game.direction == Direction.RIGHT
    dir_u = game.direction == Direction.UP
    dir_d = game.direction == Direction.DOWN

    # Check for danger
    danger_straight = (dir_r and game.is_collision(point_r)) or \
                      (dir_l and game.is_collision(point_l)) or \
                      (dir_u and game.is_collision(point_u)) or \
                      (dir_d and game.is_collision(point_d))

    danger_right = (dir_u and game.is_collision(point_r)) or \
                   (dir_d and game.is_collision(point_l)) or \
                   (dir_l and game.is_collision(point_u)) or \
                   (dir_r and game.is_collision(point_d))

    danger_left = (dir_d and game.is_collision(point_r)) or \
                  (dir_u and game.is_collision(point_l)) or \
                  (dir_r and game.is_collision(point_u)) or \
                  (dir_l and game.is_collision(point_d))

    # Check food location
    food_up = game.food.y < head.y
    food_down = game.food.y > head.y
    food_left = game.food.x < head.x
    food_right = game.food.x > head.x

    # Create the state list
    state = [
        danger_straight,  # 1 if there's a body or wall straight ahead
        danger_right,     # 1 if there's danger to the right
        danger_left,      # 1 if there's danger to the left
        food_up,          # 1 if food is above
        food_down,        # 1 if food is below
        food_left,        # 1 if food is to the left
        food_right        # 1 if food is to the right
    ]

    return list(map(int, state))