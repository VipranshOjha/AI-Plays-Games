import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
gravity = 0.25
bird_movement = 0

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
background_surface = pygame.image.load(r"C:\Users\ojhav\Desktop\AI & ML\Project1\imgs\bg.png").convert()
background_surface = pygame.transform.scale(background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_surface = pygame.image.load(r"C:\Users\ojhav\Desktop\AI & ML\Project1\imgs\bird1.png").convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (50, 40))
bird_rect = bird_surface.get_rect(center=(100, SCREEN_HEIGHT/2))

pipe_surface = pygame.image.load(r"C:\Users\ojhav\Desktop\AI & ML\Project1\imgs\pipe.png").convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (70, 400))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 300, 400]

clock = pygame.time.Clock()

def draw_floor():
    screen.blit(background_surface, (0, 0))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 200))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

# Define score variable
score = 0

# Load font for score counter
font = pygame.font.SysFont(None, 36)  # Choose a font and font size
score_text = font.render(f"Score: {score}", True, WHITE)
score_rect = score_text.get_rect(topleft=(10, 10))  # Adjust the position as needed

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bird_rect.top >= 0:
                bird_movement = 0
                bird_movement -= 8

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            score += 1  # Increment score

    screen.fill(BLACK)
    draw_floor()
    bird_movement += gravity
    bird_rect.centery += bird_movement
    rotated_bird = rotate_bird(bird_surface)
    screen.blit(rotated_bird, bird_rect)

    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    running = check_collision(pipe_list)

    # Render and draw score text
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, score_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
