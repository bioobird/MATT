import constants
import window as w
import pygame
import random
import time
import math
import pygame.font
import enemy
import enemy_tools
import spaceship
import utils

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

game_state = "start"

# Initialize game window parameters, colors, global variables, etc.
window = pygame.display.set_mode((w.WIDTH, w.HEIGHT))

# Shield parameters
SHIELD_X = w.WIDTH - 150  # X-coordinate of the shield center
SHIELD_Y = 150  # Y-coordinate of the shield center
SHIELD_RADIUS = 100  # Radius of the shield
SHIELD_COLOR = (255, 255, 0)  # Yellow color (RGB)


def draw_shield():
    pygame.draw.circle(window, SHIELD_COLOR, (SHIELD_X, SHIELD_Y), SHIELD_RADIUS)

def next_stage():
    global current_stage
    current_stage += 1
    generate_enemies(current_stage)

def check_all_enemies_defeated():
    global running, current_stage
    if not enemies:
        if current_stage == 5:  # Adjusting for Stage 5 completion
            display_end_game_message("YOU WIN!")
            running = False
        else:
            next_stage()

def generate_enemies(stage):
    global enemies
    enemies.clear()
    enemies = enemy_tools.get_enemies_for_stage(stage)


def draw_boss_protection():
    if current_stage in [3, 4, 5]:
        pygame.draw.circle(window, YELLOW_CIRCLE_COLOR, (YELLOW_CIRCLE_X, YELLOW_CIRCLE_Y), YELLOW_CIRCLE_RADIUS)

pygame.display.set_caption("Space Invaders")
# Define colors, spaceship properties, enemy properties, etc.

# Functions to manage high scores
def read_high_score():
    # Read the high score from the file
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def update_high_score(new_score):
    global high_score
    # Check if the current score is greater than the stored high score
    if new_score > high_score:
        high_score = new_score
        # Overwrite the high_score.txt file with the new high score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))
        print("New high score saved:", high_score)

# Read the high score at the start
high_score = read_high_score()

# Load the sound
player_hit_sound = pygame.mixer.Sound("mixkit-arcade-retro-game-over-213.wav")
blaster_sound = pygame.mixer.Sound("blaster.wav")  # Loading the blaster sound
enemy_hit_sound = pygame.mixer.Sound("mixkit-falling-hit-757.wav")
background_music = pygame.mixer.Sound("tetris theme song.mp3")


# Load the background image
background_image = pygame.image.load("8734d3a2-2178-4459-aa4b-a3c1ad89aeb0.png")

# Load the background image for the game stages
game_background_image = pygame.image.load("714107fb-139b-49ca-bc8e-0dacf34d4fc2.png")
game_background_image = pygame.transform.scale(game_background_image, (w.WIDTH, w.HEIGHT))

pygame.display.set_caption("Space Invaders")

BLACK, WHITE, GREEN, RED, BLUE, ORANGE, YELLOW, PURPLE, PINK, CYAN, MAGENTA, LIME, OLIVE = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0), (255, 255, 0), (128, 0, 128), (255, 192, 203), (0, 255, 255), (255, 0, 255), (0, 255, 0), (128, 128, 0)

# Define yellow circle parameters for boss stages
YELLOW_CIRCLE_X = w.WIDTH - 150
YELLOW_CIRCLE_Y = 50
YELLOW_CIRCLE_RADIUS = 100
YELLOW_CIRCLE_COLOR = YELLOW  # Assuming YELLOW is already defined in your colors section
# Global Oscillation Variables
tail_angle = 0
oscillation_amplitude = 10  # Feel free to adjust
oscillation_speed = 0.05  # Feel free to adjust
particles = []

# Player properties
spaceship_x = (w.WIDTH - spaceship.WIDTH) // 2
spaceship_y = w.HEIGHT - spaceship.HEIGHT - 10
spaceship_speed = 5

# Bullet properties
player_bullets = []
player_bullet_speed = -5
player_bullet_fire_rate = 150  # milliseconds
last_player_shot_time = pygame.time.get_ticks()

enemy_bullets = []
enemy_bullet_speed = 3

# Enemies
enemies = []
enemy_fire_rate = 2000  # milliseconds
current_stage = 1

# Health definitions
enemy1_health = 1  # Health for each individual enemy in stages 1
enemy2_health = 1  # Health for each individual enemy in stages 2
boss3_health = 10  # Stage 3 boss health
boss4_health = 10  # Stage 4 boss health
boss5_health = 10  # Stage 5 boss health

# Explosions
explosions = []

# Score and font
score = 0
font = pygame.font.SysFont(None, 36)

# Particle class definition
class Particle:
    def __init__(self, x, y, color, size, velocity_x, velocity_y, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = lifetime

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

def generate_particles(x, y, type):
    # Default values for particles
    num_particles = 20  # Adjust as necessary
    particle_color = ORANGE  # Default color, can be adjusted based on particle type
    particle_size = 2  # Default size of particles
    particle_lifetime = 30  # Default lifetime of particles

    # Customization for different types of particles
    if type == "enemy_hit":
        # Customization for when an enemy is hit
        particle_color = RED
        particle_velocity_range = (-5, 5)  # Explosive effect for hits
    else:
        # Default or unknown type handling
        particle_velocity_range = (-2, 2)  # Less explosive effect for default or other cases

    # Loop to generate and append each new particle
    for _ in range(num_particles):
        particle_velocity_x = random.randint(*particle_velocity_range)
        particle_velocity_y = random.randint(*particle_velocity_range)
        particle_x = x + random.randint(-10, 10)  # Spawn around the event's position
        particle_y = y + random.randint(-10, 10)  # Spawn around the event's position

        # Create a new particle instance and add it to the particle list
        new_particle = Particle(particle_x, particle_y, particle_color, particle_size, particle_velocity_x, particle_velocity_y, particle_lifetime)
        particles.append(new_particle)
# Dorsal fin color definitions
DORSAL_FIN_COLOR_BOSS3 = BLUE
DORSAL_FIN_COLOR_BOSS4 = BLUE
DORSAL_FIN_COLOR_BOSS5 = BLUE

# Dorsal fin size definitions
DORSAL_FIN_WIDTH_BOSS3 = utils.get_enemy_size('boss3')
DORSAL_FIN_WIDTH_BOSS4 = utils.get_enemy_size('boss4')
DORSAL_FIN_WIDTH_BOSS5 = utils.get_enemy_size('boss5')

DORSAL_FIN_HEIGHT_BOSS3 = 40
DORSAL_FIN_HEIGHT_BOSS4 = 60
DORSAL_FIN_HEIGHT_BOSS5 = 90

def draw_scales(x, y, width, height, scale_width=8, scale_height=4):
    # Increase spacing between scales for visual appeal
    spacing_x = scale_width  # Adjust this value to increase horizontal spacing
    spacing_y = scale_height * 2  # Adjust this value to increase vertical spacing

    # Drawing rows of scales with increased spacing
    for row in range(y - height // 2, y + height // 2, spacing_y):
        offset_x = 0 if (row // spacing_y) % 2 == 0 else scale_width // 2  # Stagger the rows for a more natural scale pattern
        
        for col in range(x - width // 2 + offset_x, x + width // 2, spacing_x):
            # Calculate the top-left corner of the current scale
            scale_x = col
            scale_y = row
            
            # Determine if the scale's position is within the oval
            # This checks if the point is within an ellipse formula [(x-x0)^2/a^2 + (y-y0)^2/b^2 <= 1]
            # Also adjust the condition to better match the fish body by softening the edge detection
            if (((col - x)**2 / ((width // 2 + scale_width // 2)**2)) + 
                ((row - y)**2 / ((height // 2 + scale_height // 2)**2))) <= 1:
                # draw empty scale with a thinner outline to reduce visual density
                pygame.draw.ellipse(window, BLACK, (scale_x, scale_y, scale_width, scale_height), 1)

# Example fish body to demonstrate scales drawing
def draw_fish_with_scales(x, y):
    fish_width = 100  # Fish body width
    fish_height = 50  # Fish body height

    # Draw the fish body (filled)
    pygame.draw.ellipse(window, BLUE, (x - fish_width // 2, y - fish_height // 2, fish_width, fish_height))
    
    # Draw scales
    draw_scales(x, y, fish_width, fish_height)
    
def render_outlined_text(font, text, text_color, outline_color, outline_width=2):
    # Create a surface for the text
    text_surface = font.render(text, True, text_color).convert_alpha()

    # Create a slightly larger surface for the outline
    outline_surface = pygame.Surface(text_surface.get_size()).convert_alpha()
    outline_surface.fill((0, 0, 0, 0))  # Fill with transparent color

    # Render the outline
    render_outlined_text_on_surface(outline_surface, text_surface, outline_color, outline_width)

    return outline_surface, outline_surface.get_rect()

def render_outlined_text_on_surface(surface, text_surface, outline_color, outline_width):
    # Get the size of the text surface
    width, height = text_surface.get_size()

    # Draw the outline on the surface
    for x in range(-outline_width, width + outline_width):
        for y in range(-outline_width, height + outline_width):
            if abs(x) < outline_width or abs(y) < outline_width:
                surface.blit(text_surface, (x, y), None, pygame.BLEND_RGBA_MAX)
                pygame.draw.rect(surface, outline_color, (x, y, width, height), outline_width)

# Call this in your game loop or wherever you draw your fish
draw_fish_with_scales(400, 300)  # Example call

def draw_dorsal_fin(x, y, enemy_width, enemy_height, enemy_type):
    if enemy_type in ['enemy1', 'enemy2', 'boss3', 'boss4', 'boss5']:
        # Configuration for the fin size, adapt as necessary
        if enemy_type in ['enemy1', 'enemy2']:
            fin_height = 20
            fin_width = enemy_width // 4  # Making the fin narrower for smaller enemies
        else:  # Bosses have larger fins
            fin_height = 40 + (int(enemy_type[-1]) - 3) * 10  # Example scaling for bosses
            fin_width = enemy_width // 3

        # Position the base of the fin triangle on top of the enemy oval
        fin_base_x = x + enemy_width / 2 - fin_width // 2
        fin_base_y = y

        # Adjust the coordinates to make the hypotenuse point towards the left
        point1 = (fin_base_x + fin_width, fin_base_y)
        point2 = (fin_base_x, fin_base_y)  # Base of the triangle, on top of the enemy oval
        point3 = (fin_base_x + fin_width, fin_base_y - fin_height)  # Tip of the fin, pointing left and up

        # Choosing fin color
        fin_color = YELLOW  # Default color, can be changed based on enemy type or preference

        # Drawing the fin
        pygame.draw.polygon(window, fin_color, [point1, point2, point3])


def draw_angry_face(x, y, enemy):
    # Debugging - Remove after confirmation
    # print(f"Drawing face for {enemy.enemy_type} with mouth_state {enemy['mouth_state']} at (x:{x}, y:{y})")
    
    if enemy.enemy_type.startswith('enemy'):
        # Drawing code for regular enemies with enhanced eyes
        pygame.draw.circle(window, WHITE, (x + 5, y + 10), 7)  # Left eye
        pygame.draw.circle(window, WHITE, (x + 20, y + 10), 7)  # Right eye
        pygame.draw.circle(window, BLACK, (x + 5, y + 10), 5)   # Left pupil
        pygame.draw.circle(window, BLACK, (x + 20, y + 10), 5)  # Right pupil
        
        # Toggle mouth open/closed
        if enemy.mouthIsOpen():
            pygame.draw.circle(window, BLACK, (x + 12, y + 20), 3)  # Mouth open
        else:
            pygame.draw.line(window, BLACK, (x + 5, y + 20), (x + 20, y + 20), 2)  # Mouth closed
    else:  
        # Drawing for bosses
        pygame.draw.circle(window, WHITE, (x + 10, y + 20), 15)  # Left eye
        pygame.draw.circle(window, WHITE, (x + 65, y + 20), 15)  # Right eye
        pygame.draw.circle(window, BLACK, (x + 15, y + 30), 10)  # Left pupil
        pygame.draw.circle(window, BLACK, (x + 60, y + 30), 10)  # Right pupil

        # Ensuring 'mouth_state' impacts boss mouth visuals. Draw open or closed mouth accordingly.
        if enemy.mouthIsOpen():
            pygame.draw.circle(window, BLACK, (x + 37, y + 60), 20)  # Boss mouth open
        else:
            pygame.draw.line(window, BLACK, (x + 15, y + 60), (x + 60, y + 60), 5)  # Boss mouth closed # Boss mouth closed
    
    # Draw the tail for all enemies and bosses.
    draw_tail(x, y, enemy.width, enemy.height, enemy.enemy_type)

def draw_tail(x, y, enemy_width, enemy_height, enemy_type):
    global tail_angle

    # Define tail_height, tail_width, and half_moon_radius based on enemy_type
    if enemy_type == 'enemy1':
        tail_height = 20
        tail_width = 40
        half_moon_radius = 10
    elif enemy_type == 'enemy2':
        tail_height = 30
        tail_width = 60
        half_moon_radius = 10
    elif enemy_type == 'boss3':
        tail_height = 40
        tail_width = 90
        half_moon_radius = 20
    elif enemy_type == 'boss4':
        tail_height = 60
        tail_width = 120
        half_moon_radius = 30
    elif enemy_type == 'boss5':
        tail_height = 80
        tail_width = 150
        half_moon_radius = 40
    else:
        tail_height = 20  # Default tail_height if enemy_type is not recognized
        tail_width = 40  # Default tail_width if enemy_type is not recognized
        half_moon_radius = 10  # Default half_moon_radius if enemy_type is not recognized

    # Oscillation logic for natural movement
    oscillation = math.sin(tail_angle) * oscillation_amplitude

    # Starting position of the tail, adjusts with oscillation
    tail_start_x = x + enemy_width
    tail_start_y = y + (enemy_height // 2) - (tail_height // 2) + oscillation

    # Define tail color based on enemy type
    if enemy_type == 'enemy1':
        tail_color = PURPLE
    elif enemy_type == 'enemy2':
        tail_color = ORANGE
    elif enemy_type == 'boss3':
        tail_color = YELLOW
    elif enemy_type == 'boss4':
        tail_color = PINK
    elif enemy_type == 'boss5':
        tail_color = CYAN
    else:
        tail_color = GREEN  # Default tail color if enemy type is not recognized

    # Define points for the oscillating triangle tail
    point1 = (tail_start_x, tail_start_y)
    point2 = (tail_start_x + tail_width, tail_start_y + (tail_height // 2))  # Tip of the tail
    point3 = (tail_start_x, tail_start_y + tail_height)

    # Draw the oscillating tail triangle
    pygame.draw.polygon(window, tail_color, [point1, point2, point3])

    half_moon_thickness = 5  # Thickness, constant for simplicity

    # The rectangle that bounds the circle (ellipse) from which the arc is generated
    arc_rect = [point2[0] - half_moon_radius, point2[1] - half_moon_radius,
                half_moon_radius * 2, half_moon_radius * 2]

    # Drawing the half-moon ("C" shape) at the tip of the tail
    pygame.draw.arc(window, tail_color, arc_rect,
                    math.pi/2, 3*math.pi/2, half_moon_thickness)  # Draw arc from π/2 to 3π/2 radians

    # Your event handling
    pass

def next_stage():
    global current_stage
    current_stage += 1
    generate_enemies(current_stage)

def check_all_enemies_defeated():
    global running, current_stage
    if not enemies:
        if current_stage == 5:  # Adjusting for Stage 5 completion
            display_end_game_message("YOU WIN!")
            running = False
        else:
            next_stage()

# def generate_enemies(stage):
#     global enemies
#     enemies.clear()
    
#     enemy_size_mapping = {
#         'enemy1': ENEMY1_SIZE,
#         'enemy2': ENEMY2_SIZE,
#         'boss3': BOSS3_SIZE,
#         'boss4': BOSS4_SIZE,
#         'boss5': BOSS5_SIZE,
#     }
    
#     # Example logic for assigning health based on the stage and enemy type
#     if stage in [1, 2]:
#         enemy_count = 10
#         enemy_type = 'enemy1' if stage == 1 else 'enemy2'
#         enemy_health = enemy1_health if stage == 1 else enemy2_health
#     elif stage == 3:
#         enemy_count = 1
#         enemy_type = 'boss3'
#         enemy_health = boss3_health
#     elif stage == 4:
#         enemy_count = 1
#         enemy_type = 'boss4'
#         enemy_health = boss4_health
#     elif stage == 5:
#         enemy_count = 1
#         enemy_type = 'boss5'
#         enemy_health = boss5_health

#     enemy_size = enemy_size_mapping[enemy_type]
    
#     for _ in range(enemy_count):
#         enemies.append({
#             'x': random.randint(0, w.WIDTH - enemy_size),
#             'y': 50 if stage >= 3 else random.randint(50, 150),
#             'width': enemy_size,
#             'height': enemy_size,  # Assuming square shape; adjust dimensions as necessary
#             'speed': random.choice([-1, 1]) * 2,
#             'health': enemy_health,
#             'is_boss': stage >= 3,
#             'enemy_type': enemy_type,
#             'mouth_state': 'closed',
#             'last_shot': pygame.time.get_ticks()
#         })
def generate_particles(x, y, enemy_type):
    size_mapping = {
        'enemy1': 30,
        'enemy2': 45,
        'boss3': 200,
        'boss4': 450
    }

    particle_color = ORANGE
    particle_size = 2
    particle_lifetime = 30

    num_particles = size_mapping.get(enemy_type, 30) // 2  # Generate number of particles based on enemy type
    for _ in range(num_particles):
        particle_velocity_x = random.randint(-5, 5)
        particle_velocity_y = random.randint(-5, 5)
        particle_x = x + random.randint(-10, 10)
        particle_y = y + random.randint(-10, 10)
        
        new_particle = Particle(particle_x, particle_y, particle_color, particle_size, particle_velocity_x, particle_velocity_y, particle_lifetime)
        particles.append(new_particle)

    return particles

def fire_bullet(rect, speed, is_enemy, enemy_type=None, enemy=None):
    # Define bullet sizes for all enemy types including boss5
    bullet_sizes = {
        'enemy1': (20, 50),
        'enemy2': (30, 70),
        'boss3': (100, 130),
        'boss4': (150, 150),
        'boss5': (120, 120),  # Define a unique or suitable size for boss5 bullets
    }

    size = bullet_sizes.get(enemy_type, (20, 20))  # Use the get method to fetch sizes or default
    if is_enemy:
        # Set angle offsets for enemy bullets
        if enemy_type == 'boss3':
            angle1 = -0.523599  # -30 degrees in radians
            angle2 = 0.523599   # 30 degrees in radians
        elif enemy_type == 'boss4':
            angle1 = -0.785398  # -45 degrees in radians
            angle2 = 0.785398   # 45 degrees in radians
        elif enemy_type == 'boss5':
            angle1 = -1.0472    # -60 degrees in radians
            angle2 = 1.0472     # 60 degrees in radians
        else:
            angle1 = 0  # No angle offset for regular enemy bullets
            angle2 = 0
    else:
        angle1 = 0  # No angle offset for player bullets
        angle2 = 0

    bullet = {
        'rect': pygame.Rect(rect.x, rect.y, size[0], size[1]),
        'speed': speed,
        'is_enemy': is_enemy,
        'angle1': angle1,
        'angle2': angle2,
    }
    (enemy_bullets if is_enemy else player_bullets).append(bullet)

    # Toggle mouth state (Ensure all necessary enemies, including bosses, have a 'mouth_state' attribute)
    if enemy and enemy.mouthIsOpen():
        enemy.toggleMouthState()

def display_end_game_message(message):
    window.fill(BLACK)
    text = font.render(message, True, WHITE)
    window.blit(text, (w.WIDTH // 2 - text.get_width() // 2, w.HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(5000)  # Wait for 5 seconds

    background_image = pygame.image.load("8734d3a2-2178-4459-aa4b-a3c1ad89aeb0.png")
background_image = pygame.transform.scale(background_image, (w.WIDTH, w.HEIGHT))

def update_display(game_state):
    if game_state == "start":
        # Draw the scaled background image
        window.blit(background_image, (0, 0))

        # Define the font for the title
        title_font = pygame.font.SysFont(None, 72)

        # Text content
        text_content = "FISH INVADERS"

        # Calculate the center position to align the text
        text_surface = title_font.render(text_content, True, BLUE)
        text_rect = text_surface.get_rect(center=(w.WIDTH // 2, 100))

        # Render the outline by drawing the text with an offset, in yellow
        outline_color = YELLOW
        for offset in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:  # Offsets to create the outline effect
            outline_surface = title_font.render(text_content, True, outline_color)
            window.blit(outline_surface, (text_rect.x + offset[0], text_rect.y + offset[1]))

        # Render the "FISH INVADERS" title text over the outline
        window.blit(text_surface, text_rect)

        # The rest of the start screen UI elements (buttons, high score text, etc.) remain unchanged
        # Define the font for buttons and text
        button_font = pygame.font.SysFont(None, 36)

        # Render the "Start Game" button text
        start_text = button_font.render("Start Game", True, WHITE)
        start_rect = pygame.Rect(w.WIDTH // 2 - 100, w.HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(window, GREEN, start_rect)
        window.blit(start_text, (start_rect.centerx - start_text.get_width() // 2, start_rect.centery - start_text.get_height() // 2))

        # Render the "Quit Game" button text
        quit_text = button_font.render("Quit Game", True, WHITE)
        quit_rect = pygame.Rect(w.WIDTH // 2 - 100, w.HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(window, RED, quit_rect)
        window.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))

        # Render and draw the "High Scores" text
        high_score_text = button_font.render("High Scores:", True, WHITE)
        window.blit(high_score_text, (50, w.HEIGHT - 150))

        # Render and draw the high score value
        high_score_value_text = button_font.render(f"High Score: {high_score}", True, WHITE)
        window.blit(high_score_value_text, (50, w.HEIGHT - 100))

        # Update the display
        pygame.display.update()

    elif game_state == "game":
        # Draw the scaled background image for the game
        window.blit(game_background_image, (0, 0))

        # Draw the score counter
        score_text = font.render("Score: " + str(score), True, WHITE)
        window.blit(score_text, (10, 10))  # Position (10, 10) for top-left corner

        # Draw the spaceship
        pygame.draw.circle(window, WHITE, (spaceship_x + spaceship.WIDTH // 2, spaceship_y + spaceship.HEIGHT // 2), spaceship.WIDTH // 2)
        pygame.draw.circle(window, BLACK, (spaceship_x + spaceship.WIDTH // 4, spaceship_y + spaceship.HEIGHT // 4), spaceship.WIDTH // 8)
        pygame.draw.circle(window, BLACK, (spaceship_x + spaceship.WIDTH * 3 // 4, spaceship_y + spaceship.HEIGHT // 4), spaceship.WIDTH // 8)
        pygame.draw.line(window, BLACK, (spaceship_x + spaceship.WIDTH // 4, spaceship_y + spaceship.HEIGHT * 3 // 4), (spaceship_x + spaceship.WIDTH * 3 // 4, spaceship_y + spaceship.HEIGHT * 3 // 4), 2)

        # Draw the tabby stripes on the spaceship
        for i in range(3):
            start_x = spaceship_x + spaceship.WIDTH // 4
            start_y = spaceship_y + spaceship.HEIGHT // 4 + i * (spaceship.HEIGHT // 8)
            end_x = spaceship_x + spaceship.WIDTH * 3 // 4
            end_y = start_y
            pygame.draw.line(window, BLACK, (start_x, start_y), (end_x, end_y), 2)

        # Draw enemies and their health bars (if applicable)
        for enemy in enemies:
            # Define enemy body color based on enemy type
            if enemy.enemy_type == 'enemy1':
                enemy_color = BLUE
            elif enemy.enemy_type == 'enemy2':
                enemy_color = BLUE
            elif enemy.enemy_type == 'boss3':
                enemy_color = BLUE
            elif enemy.enemy_type == 'boss4':
                enemy_color = BLUE
            elif enemy.enemy_type == 'boss5':
                enemy_color = BLUE
            else:
                enemy_color = RED

            # Draw enemies as ovals
            pygame.draw.ellipse(window, enemy_color, pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height))
            draw_scales(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, enemy.width, enemy.height)
            
            # Draw the dorsal fin (if applicable)
            draw_dorsal_fin(enemy.x, enemy.y, enemy.width, enemy.height, enemy.enemy_type)

            # Draw the dorsal fin for each enemy using their specific type for appropriate adjustment.
            draw_dorsal_fin(enemy.x, enemy.y, enemy.width, enemy.height, enemy.enemy_type)
            
            draw_angry_face(enemy.x, enemy.y, enemy)
            draw_tail(enemy.x, enemy.y, enemy.width, enemy.height, enemy.enemy_type)

            # Draw health bars for bosses
            if enemy.is_boss:
                if enemy.enemy_type == 'boss3':
                    max_health = boss3_health
                    health_bar_color = CYAN
                elif enemy.enemy_type == 'boss4':
                    max_health = boss4_health
                    health_bar_color = ORANGE
                elif enemy.enemy_type == 'boss5':
                    max_health = boss5_health
                    health_bar_color = PURPLE
                health_percentage = enemy.health / max_health
                pygame.draw.rect(window, health_bar_color, (w.WIDTH - 210, 10, 200 * health_percentage, 20))

        # Draw all bullets
        for bullet in player_bullets + enemy_bullets:
            bullet_color = GREEN if not bullet['is_enemy'] else RED
            pygame.draw.rect(window, bullet_color, bullet['rect'])

        # Handle explosion effect particles
        for explosion in explosions[:]:
            pygame.draw.circle(window, ORANGE, (explosion['x'], explosion['y']), explosion['size'])
            explosion['timer'] -= 1
            if explosion['timer'] <= 0:
                explosions.remove(explosion)

        # Handle general particle effects
        for particle in particles[:]:
            if particle.lifetime > 0:
                particle.draw(window)
                particle.update()
            else:
                particles.remove(particle)

        # Update the display
        pygame.display.flip()

running = True
while running:
    # Update tail_angle to animate tails
    tail_angle += oscillation_speed

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "start":
                mouse_pos = pygame.mouse.get_pos()
                # Check if the "Start Game" button was clicked
                start_rect = pygame.Rect(w.WIDTH // 2 - 100, w.HEIGHT // 2 - 50, 200, 50)
                if start_rect.collidepoint(mouse_pos):
                    game_state = "game"
                    score = 0  # Reset score for a new game session
                    enemies.clear()  # Clear enemies for a new session
                    generate_enemies(current_stage)
                # Check if the "Quit Game" button was clicked
                quit_rect = pygame.Rect(w.WIDTH // 2 - 100, w.HEIGHT // 2 + 50, 200, 50)
                if quit_rect.collidepoint(mouse_pos):
                    running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "game":
                if event.key == pygame.K_SPACE and (pygame.time.get_ticks() - last_player_shot_time > player_bullet_fire_rate):
                    last_player_shot_time = pygame.time.get_ticks()
                    fire_bullet(pygame.Rect(spaceship_x + spaceship.WIDTH // 2 - 10, spaceship_y, 20, 20), player_bullet_speed, False)
                    blaster_sound.play()

    if game_state == "start":
        update_display("start")
    elif game_state == "game":
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship_x > 0:
            spaceship_x -= spaceship_speed
        if keys[pygame.K_RIGHT] and spaceship_x < w.WIDTH - spaceship.WIDTH:
            spaceship_x += spaceship_speed

        # Enemy logic and bullet update
        now = pygame.time.get_ticks()
        for enemy in enemies[:]:
            enemy.x += enemy.speed
            if enemy.x <= 0 or enemy.x + enemy.width >= w.WIDTH:
                enemy.toggle_direction()

            if now - enemy.last_shot > enemy_fire_rate and enemy.health > 0:
                fire_bullet(pygame.Rect(enemy.x + enemy.width // 2, enemy.y + enemy.height, 20, 20), enemy_bullet_speed, True, enemy.enemy_type, enemy)
                enemy.last_shot = now

        # Processing enemy and player bullets
        for bullet in player_bullets[:] + enemy_bullets[:]:
            bullet['rect'].y += bullet['speed']

            if bullet['rect'].y < 0 or bullet['rect'].y > w.HEIGHT:
                if bullet in player_bullets:
                    player_bullets.remove(bullet)
                elif bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
            else:
                # Collision detection for player bullets with enemies
                if not bullet['is_enemy']:
                    for enemy in enemies[:]:
                        if bullet['rect'].colliderect(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)):
                            enemy_hit_sound.play()
                            player_bullets.remove(bullet)
                            generate_particles(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, enemy.enemy_type)
                            enemy.health -= 1
                            if enemy.health <= 0:
                                enemies.remove(enemy)
                                score += 5000 if enemy.enemy_type == 'boss5' else 1000 if enemy.is_boss else 500
                                update_high_score(score)
                            break

        # Collision detection for enemy bullets with the player
        player_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship.WIDTH, spaceship.HEIGHT)
        for bullet in enemy_bullets[:]:
            if player_rect.colliderect(bullet['rect']):
                player_hit_sound.play()
                enemy_bullets.remove(bullet)
                update_high_score(score)
                game_state = "start"  # Switch to start screen after game over

        # Check if all enemies are defeated
        check_all_enemies_defeated()

        # Drawing game objects and particles
        update_display("game")

    pygame.time.delay(10)

pygame.quit()

