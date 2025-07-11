import pygame
import random
import os
import math

# Initialize
pygame.init()
pygame.display.set_caption("Dino Runner - AI Player")

# Screen
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Ground baseline
GROUND_Y = HEIGHT - 20

# Load Assets
ASSETS = "assets"

# Dino sprite sheet
sprite_sheet = pygame.image.load(os.path.join(ASSETS, "dino_sprite_sheet.png")).convert_alpha()

# Dino frame sizes
FRAME_WIDTH = 147
FRAME_HEIGHT = 212
SCALE_FACTOR = 0.5
NEW_WIDTH = int(FRAME_WIDTH * SCALE_FACTOR)
NEW_HEIGHT = int(FRAME_HEIGHT * SCALE_FACTOR)

def get_frame(index):
    frame = sprite_sheet.subsurface((index * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    return pygame.transform.scale(frame, (NEW_WIDTH, NEW_HEIGHT))

# Dino animation frames
RUN_FRAMES = [get_frame(0), get_frame(1)]
JUMP_FRAME = get_frame(2)
DUCK_FRAMES = [get_frame(5), get_frame(6)]

# Load hurdle sprite sheet
hurdle_sheet = pygame.image.load(os.path.join(ASSETS, "hurdle_sheet.png")).convert_alpha()
HURDLE_WIDTH = 48
HURDLE_HEIGHT = 149
TOTAL_FRAMES = 14

def load_hurdle_frames():
    frames = []
    for i in range(TOTAL_FRAMES):
        frame = hurdle_sheet.subsurface((i * HURDLE_WIDTH, 0, HURDLE_WIDTH, HURDLE_HEIGHT))
        frames.append(frame)
    return frames

HURDLE_FRAMES = load_hurdle_frames()

# Background and Game Over
BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "background.png")), (WIDTH, HEIGHT)
)
GAME_OVER_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS, "game_over.png")).convert_alpha(),
    (300, 100)
)

FONT = pygame.font.SysFont('comicsans', 30)

class GameState:
    """Represents the current state of the game for AI decision making"""
    def __init__(self):
        self.dino_x = 0
        self.dino_y = 0
        self.dino_is_jumping = False
        self.dino_is_ducking = False
        self.obstacles = []
        self.score = 0
        self.game_speed = 7
        self.time_elapsed = 0
        self.initial_speed = 7
        self.max_speed = 15
        self.speed_increase_rate = 0.1  # Speed increase per second
    
    def update(self, dino, obstacles, score, time_elapsed):
        """Update game state with current game information"""
        self.dino_x = dino.x
        self.dino_y = dino.y
        self.dino_is_jumping = dino.is_jumping
        self.dino_is_ducking = dino.is_ducking
        self.obstacles = [(obs.x, obs.y, obs.image.get_width(), obs.image.get_height()) for obs in obstacles]
        self.score = score
        self.time_elapsed = time_elapsed
        
        # Calculate game speed based on time elapsed
        self.game_speed = min(
            self.initial_speed + (time_elapsed * self.speed_increase_rate),
            self.max_speed
        )

class DinosaurAI:
    """AI controller for the dinosaur game"""
    
    def __init__(self):
        self.base_decision_distance = 200  # Base distance for decisions
        self.base_jump_threshold = 120     # Base distance threshold for jumping
        self.base_duck_threshold = 100     # Base distance threshold for ducking
        self.safety_margin = 10            # Extra safety margin
        self.last_action = "RUN"           # Track last action taken
        self.reaction_time = 0             # Simulate reaction time
        
    def get_adaptive_thresholds(self, game_speed):
        """Adjust AI thresholds based on current game speed"""
        speed_multiplier = game_speed / 7  # Ratio compared to initial speed
        
        # Increase thresholds as speed increases to give AI more time to react
        decision_distance = self.base_decision_distance * speed_multiplier
        jump_threshold = self.base_jump_threshold * speed_multiplier
        duck_threshold = self.base_duck_threshold * speed_multiplier
        
        return decision_distance, jump_threshold, duck_threshold
        
    def get_nearest_obstacle(self, game_state):
        """Find the nearest obstacle in front of the dinosaur"""
        nearest_obstacle = None
        min_distance = float('inf')
        
        for obs_x, obs_y, obs_width, obs_height in game_state.obstacles:
            # Only consider obstacles in front of the dinosaur
            if obs_x > game_state.dino_x:
                distance = obs_x - game_state.dino_x
                if distance < min_distance:
                    min_distance = distance
                    nearest_obstacle = (obs_x, obs_y, obs_width, obs_height, distance)
        
        return nearest_obstacle
    
    def calculate_collision_risk(self, game_state, obstacle):
        """Calculate if the dinosaur will collide with an obstacle"""
        if not obstacle:
            return False, 0
        
        obs_x, obs_y, obs_width, obs_height, distance = obstacle
        
        # Predict where the dinosaur will be when the obstacle reaches it
        frames_to_collision = distance / game_state.game_speed
        
        # Account for jumping physics
        if game_state.dino_is_jumping:
            # Predict dinosaur's y position during jump
            predicted_y = self.predict_jump_position(game_state, frames_to_collision)
        else:
            predicted_y = game_state.dino_y
        
        # Check for collision
        dino_rect = pygame.Rect(game_state.dino_x, predicted_y, NEW_WIDTH, NEW_HEIGHT)
        obs_rect = pygame.Rect(obs_x, obs_y, obs_width, obs_height)
        
        collision_risk = dino_rect.colliderect(obs_rect)
        
        return collision_risk, frames_to_collision
    
    def predict_jump_position(self, game_state, frames_ahead):
        """Predict dinosaur's y position during jump"""
        # Simplified jump physics prediction
        # This is based on the jump mechanics in the original game
        jump_vel = 8.5
        gravity = 0.5
        
        # Estimate current jump phase
        if game_state.dino_is_jumping:
            # Rough estimation of jump position
            time_in_jump = frames_ahead
            y_offset = jump_vel * time_in_jump - 0.5 * gravity * time_in_jump * time_in_jump
            return max(game_state.dino_y - y_offset * 4, GROUND_Y - NEW_HEIGHT - 50)
        
        return game_state.dino_y
    
    def should_jump(self, game_state, obstacle):
        """Determine if the dinosaur should jump"""
        if not obstacle:
            return False
        
        obs_x, obs_y, obs_width, obs_height, distance = obstacle
        _, jump_threshold, _ = self.get_adaptive_thresholds(game_state.game_speed)
        
        # Don't jump if already jumping or ducking
        if game_state.dino_is_jumping or game_state.dino_is_ducking:
            return False
        
        # Jump if obstacle is at ground level and within jump threshold
        obstacle_at_ground = obs_y >= GROUND_Y - obs_height - 10
        
        if obstacle_at_ground and distance <= jump_threshold + self.safety_margin:
            return True
        
        return False
    
    def should_duck(self, game_state, obstacle):
        """Determine if the dinosaur should duck"""
        if not obstacle:
            return False
        
        obs_x, obs_y, obs_width, obs_height, distance = obstacle
        _, _, duck_threshold = self.get_adaptive_thresholds(game_state.game_speed)
        
        # Don't duck if already jumping
        if game_state.dino_is_jumping:
            return False
        
        # Duck if obstacle is high (like flying obstacles) and within duck threshold
        obstacle_is_high = obs_y < GROUND_Y - obs_height - 30
        
        if obstacle_is_high and distance <= duck_threshold + self.safety_margin:
            return True
        
        return False
    
    def make_decision(self, game_state):
        """Make AI decision based on current game state"""
        # Add small reaction delay for realism
        if self.reaction_time > 0:
            self.reaction_time -= 1
            return self.last_action
        
        nearest_obstacle = self.get_nearest_obstacle(game_state)
        
        if not nearest_obstacle:
            self.last_action = "RUN"
            return "RUN"
        
        # Get adaptive thresholds based on current game speed
        decision_distance, _, _ = self.get_adaptive_thresholds(game_state.game_speed)
        
        # Check if we need to take action
        distance = nearest_obstacle[4]
        
        if distance > decision_distance:
            self.last_action = "RUN"
            return "RUN"
        
        # Decide action based on obstacle type and position
        if self.should_jump(game_state, nearest_obstacle):
            self.last_action = "JUMP"
            self.reaction_time = 2  # Small delay before next decision
            return "JUMP"
        elif self.should_duck(game_state, nearest_obstacle):
            self.last_action = "DUCK"
            self.reaction_time = 2  # Small delay before next decision
            return "DUCK"
        else:
            self.last_action = "RUN"
            return "RUN"
    
    def draw_debug_info(self, win, game_state):
        """Draw debug information on screen"""
        font = pygame.font.SysFont(None, 24)
        
        # Draw AI decision
        decision_text = font.render(f"AI Decision: {self.last_action}", True, (0, 0, 0))
        win.blit(decision_text, (10, 50))
        
        # Draw game speed
        speed_text = font.render(f"Game Speed: {game_state.game_speed:.1f}", True, (0, 0, 0))
        win.blit(speed_text, (10, 75))
        
        # Draw time elapsed
        time_text = font.render(f"Time: {game_state.time_elapsed:.1f}s", True, (0, 0, 0))
        win.blit(time_text, (10, 100))
        
        # Draw obstacle detection
        nearest_obstacle = self.get_nearest_obstacle(game_state)
        if nearest_obstacle:
            obs_x, obs_y, obs_width, obs_height, distance = nearest_obstacle
            distance_text = font.render(f"Next Obstacle: {int(distance)}px", True, (0, 0, 0))
            win.blit(distance_text, (10, 125))
            
            # Get adaptive thresholds
            decision_distance, jump_threshold, duck_threshold = self.get_adaptive_thresholds(game_state.game_speed)
            
            # Draw detection line
            pygame.draw.line(win, RED, (game_state.dino_x + NEW_WIDTH, game_state.dino_y + NEW_HEIGHT//2),
                           (obs_x, obs_y + obs_height//2), 2)
            
            # Draw adaptive decision boundaries
            pygame.draw.line(win, GREEN, (game_state.dino_x + jump_threshold, 0),
                           (game_state.dino_x + jump_threshold, HEIGHT), 1)
            pygame.draw.line(win, BLUE, (game_state.dino_x + duck_threshold, 0),
                           (game_state.dino_x + duck_threshold, HEIGHT), 1)
        
        # Draw obstacle spacing info
        if len(game_state.obstacles) >= 2:
            # Calculate distance between first two obstacles
            obs1_x = game_state.obstacles[0][0]
            obs2_x = game_state.obstacles[1][0]
            spacing = abs(obs2_x - obs1_x)
            spacing_text = font.render(f"Obstacle Spacing: {int(spacing)}px", True, (0, 0, 0))
            win.blit(spacing_text, (10, 150))

# Enhanced Dinosaur Class
class Dinosaur:
    def __init__(self):
        self.x = 80
        self.y = GROUND_Y - NEW_HEIGHT
        self.jump_vel = 8.5
        self.is_jumping = False
        self.is_ducking = False
        self.run_index = 0
        self.image = RUN_FRAMES[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.y_original = self.y

    def jump(self):
        if self.is_jumping:
            self.y -= self.jump_vel * 4
            self.jump_vel -= 0.5
            if self.jump_vel < -8.5:
                self.is_jumping = False
                self.jump_vel = 8.5
        self.image = JUMP_FRAME

    def run(self):
        self.y = self.y_original
        self.image = RUN_FRAMES[self.run_index // 5]
        self.run_index = (self.run_index + 1) % 10

    def duck(self):
        self.y = self.y_original + 20
        self.image = DUCK_FRAMES[self.run_index // 5]
        self.run_index = (self.run_index + 1) % 10

    def update(self):
        if self.is_jumping:
            self.jump()
        elif self.is_ducking:
            self.duck()
        else:
            self.run()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

# Obstacle Class
class Obstacle:
    def __init__(self, speed=7, next_spawn_distance=300):
        self.image = HURDLE_FRAMES[0]
        self.x = WIDTH
        self.y = GROUND_Y - self.image.get_height()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = speed
        self.next_spawn_distance = next_spawn_distance  # Distance to next obstacle

    def move(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

# Difficulty Manager Class
class DifficultyManager:
    """Manages game difficulty progression"""
    def __init__(self):
        self.initial_speed = 7
        self.max_speed = 15
        self.speed_increase_rate = 0.1  # Speed increase per second
        
        # Distance configuration
        self.min_distance = 180        # Minimum distance between obstacles
        self.max_distance = 450        # Maximum distance between obstacles
        self.preferred_distance = 300  # Preferred average distance
        
        # Pattern weights for different distance types
        self.distance_patterns = {
            'close': (180, 250),      # Close obstacles (challenging)
            'normal': (250, 350),     # Normal spacing
            'far': (350, 450),        # Far obstacles (easier)
            'mixed': (180, 450)       # Full range
        }
        
        # Pattern probabilities (change over time)
        self.pattern_weights = {
            'close': 0.2,
            'normal': 0.5,
            'far': 0.2,
            'mixed': 0.1
        }
        
        self.last_distance = self.preferred_distance
        self.consecutive_close = 0  # Track consecutive close obstacles
        self.consecutive_far = 0    # Track consecutive far obstacles
        
    def get_current_speed(self, time_elapsed):
        """Calculate current game speed based on time elapsed"""
        return min(
            self.initial_speed + (time_elapsed * self.speed_increase_rate),
            self.max_speed
        )
    
    def get_adaptive_pattern_weights(self, time_elapsed):
        """Adjust pattern weights based on game progression"""
        # As time progresses, increase difficulty by having more close obstacles
        time_factor = min(time_elapsed / 120, 1)  # Normalize over 2 minutes
        
        base_weights = {
            'close': 0.2 + (time_factor * 0.3),    # Increase from 20% to 50%
            'normal': 0.5 - (time_factor * 0.1),   # Decrease from 50% to 40%
            'far': 0.2 - (time_factor * 0.15),     # Decrease from 20% to 5%
            'mixed': 0.1 - (time_factor * 0.05)    # Decrease from 10% to 5%
        }
        
        # Ensure no negative weights
        return {k: max(0.05, v) for k, v in base_weights.items()}
    
    def choose_distance_pattern(self, time_elapsed):
        """Choose a distance pattern based on current game state and time"""
        weights = self.get_adaptive_pattern_weights(time_elapsed)
        
        # Avoid too many consecutive close or far obstacles
        if self.consecutive_close >= 3:
            # Force a break with normal or far obstacles
            weights['close'] = 0.05
            weights['normal'] += 0.3
            weights['far'] += 0.2
        elif self.consecutive_far >= 2:
            # Add some challenge with closer obstacles
            weights['far'] = 0.1
            weights['close'] += 0.2
            weights['normal'] += 0.1
        
        # Weighted random selection
        patterns = list(weights.keys())
        probabilities = list(weights.values())
        
        # Normalize probabilities
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        
        return random.choices(patterns, weights=probabilities)[0]
    
    def get_next_obstacle_distance(self, time_elapsed):
        """Calculate the distance for the next obstacle"""
        pattern = self.choose_distance_pattern(time_elapsed)
        min_dist, max_dist = self.distance_patterns[pattern]
        
        # Add some randomness within the pattern range
        base_distance = random.randint(min_dist, max_dist)
        
        # Apply small variations for more natural feel
        variation = random.randint(-20, 20)
        final_distance = max(self.min_distance, base_distance + variation)
        
        # Update consecutive counters
        if pattern == 'close':
            self.consecutive_close += 1
            self.consecutive_far = 0
        elif pattern == 'far':
            self.consecutive_far += 1
            self.consecutive_close = 0
        else:
            self.consecutive_close = 0
            self.consecutive_far = 0
        
        self.last_distance = final_distance
        return final_distance
    
    def should_spawn_obstacle(self, obstacles, time_elapsed):
        """Determine if a new obstacle should be spawned with variable distance"""
        if len(obstacles) == 0:
            return True, self.get_next_obstacle_distance(time_elapsed)
        
        last_obstacle = obstacles[-1]
        required_distance = getattr(last_obstacle, 'next_spawn_distance', self.preferred_distance)
        
        should_spawn = last_obstacle.x < WIDTH - required_distance
        
        if should_spawn:
            next_distance = self.get_next_obstacle_distance(time_elapsed)
            return True, next_distance
        
        return False, 0

# Main Game Function with AI
def main():
    run = True
    clock = pygame.time.Clock()
    
    # Initialize game objects
    dino = Dinosaur()
    ai = DinosaurAI()
    game_state = GameState()
    difficulty_manager = DifficultyManager()
    obstacles = []
    score = 0
    font = pygame.font.SysFont(None, 36)
    game_over = False
    show_debug = True  # Toggle for debug information
    
    # Time tracking
    start_time = pygame.time.get_ticks()
    
    def redraw():
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
        dino.draw(WIN)
        for obs in obstacles:
            obs.draw(WIN)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        WIN.blit(score_text, (600, 30))
        
        # Draw AI indicator
        ai_text = font.render("AI PLAYING", True, (255, 0, 0))
        WIN.blit(ai_text, (10, 10))
        
        # Draw current speed
        speed_text = font.render(f"Speed: {game_state.game_speed:.1f}", True, (0, 0, 0))
        WIN.blit(speed_text, (600, 60))
        
        # Draw debug info if enabled
        if show_debug:
            ai.draw_debug_info(WIN, game_state)
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)
        
        # Calculate time elapsed
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - start_time) / 1000.0  # Convert to seconds

        if not game_over:
            # Update game state with current time
            game_state.update(dino, obstacles, score, time_elapsed)
            
            # Get AI decision
            ai_decision = ai.make_decision(game_state)
            
            # Apply AI decision
            if ai_decision == "JUMP" and not dino.is_jumping:
                dino.is_jumping = True
                dino.is_ducking = False
            elif ai_decision == "DUCK" and not dino.is_jumping:
                dino.is_ducking = True
            else:
                dino.is_ducking = False
            
            dino.update()

            # Spawn obstacles based on difficulty
            should_spawn, next_distance = difficulty_manager.should_spawn_obstacle(obstacles, time_elapsed)
            if should_spawn:
                if random.randint(0, 2) > 0:  # 66% chance to spawn obstacle
                    current_speed = difficulty_manager.get_current_speed(time_elapsed)
                    new_obstacle = Obstacle(current_speed, next_distance)
                    obstacles.append(new_obstacle)

            # Update obstacles
            for obs in list(obstacles):
                obs.move()
                if obs.x < -obs.image.get_width():
                    obstacles.remove(obs)
                    score += 1
                if dino.rect.colliderect(obs.rect):
                    game_over = True

        else:
            # Game over screen
            WIN.blit(BACKGROUND_IMAGE, (0, 0))
            WIN.blit(GAME_OVER_IMAGE, (WIDTH // 2 - GAME_OVER_IMAGE.get_width() // 2,
                                       HEIGHT // 2 - GAME_OVER_IMAGE.get_height() // 2))
            
            # Show final score and time
            final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
            WIN.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2,
                                       HEIGHT // 2 + 100))
            
            final_time_text = font.render(f"Time Survived: {time_elapsed:.1f}s", True, (0, 0, 0))
            WIN.blit(final_time_text, (WIDTH // 2 - final_time_text.get_width() // 2,
                                      HEIGHT // 2 + 130))
            
            max_speed_text = font.render(f"Max Speed: {game_state.game_speed:.1f}", True, (0, 0, 0))
            WIN.blit(max_speed_text, (WIDTH // 2 - max_speed_text.get_width() // 2,
                                     HEIGHT // 2 + 160))
            
            pygame.display.update()
            pygame.time.delay(4000)
            return main()  # Restart game

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:  # Toggle debug info
                    show_debug = not show_debug

        redraw()

    pygame.quit()

if __name__ == "__main__":
    main()
