#Run the .py file to play game

## PART 1 INITIALIZE APP
import pygame #imports pygame library
import sys #imports sys module for some variables 
import random

#Constants
WIDTH, HEIGHT = 800, 600 #Dimensions of game window
BALL_RADIUS = 20 #Radius of ball
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 10 #Dimensions of platform
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)

## PART 2 CREATE PYGAME INSTANCE
#Initialize Pygame
pygame.init()

#Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")
font = pygame.font.Font(None, 36)

#Clock to control frame rate
clock = pygame.time.Clock()

#Initialize variables for game
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [random.uniform(2, 4), random.uniform(2, 4)] #faster starting speed
platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
platform_speed = 10
score = 0
lives = 3
current_level = 1
platform_color = ORANGE #initialize platform color

##PART 3 FUNCTIONS FOR GAME SCREENS
def start_screen(): #Elements for start screen
    screen.fill(BLACK)
    show_text_on_screen("Bouncing Ball Game", 50, HEIGHT // 4)
    show_text_on_screen("Press any key to start...", 20, HEIGHT * 2 // 3)
    show_text_on_screen("Move the platform with arrow keys...", 30, HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()

def game_over_screen(): #Elements for game over screen
    screen.fill(BLACK)
    show_text_on_screen("Game Over", 50, HEIGHT // 3)
    show_text_on_screen(f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 20, HEIGHT * 2 // 3)
    pygame.display.flip() #flips display to make changes visible
    wait_for_key()

def victory_screen(): #Elements for win screen
    screen.fill(BLACK)
    show_text_on_screen("Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(f"You've won with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any ket to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def wait_for_key(): #waits for key press before proceeding
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if event quits, exit game
                pygame.quit()
                sys.exit
            elif event.type == pygame.KEYDOWN: #stops waiting when key is pressed
                waiting = False

def show_text_on_screen(text, font_size, y_position): #renders text on screen
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    screen.blit(text_render, text_rect) #blit draws text on game screen

def change_platform_color(): #returns random RGB color for platform color
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

##PART 3 MAIN GAME LOOP
start_screen()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()

    # Move platform
    platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
    platform_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * platform_speed

    # Ensure platform stays within screen boundaries
    platform_pos[0] = max(0, min(platform_pos[0], WIDTH - PLATFORM_WIDTH))
    platform_pos[1] = max(0, min(platform_pos[1], HEIGHT - PLATFORM_HEIGHT))

    # Move ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce off walls
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    
    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]

    # Check if ball hits platform
    if (
        platform_pos[0] <= ball_pos[0] <= platform_pos[0] + PLATFORM_WIDTH
        and platform_pos[1] <= ball_pos[1] <= platform_pos[1] + PLATFORM_HEIGHT
    ):
        ball_speed[1] = -ball_speed[1]
        score += 1

    # Check if player advances to next level
    if score >= current_level * 10:
        current_level += 1
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_speed = [random.uniform(2, 4), random.uniform(2, 4)] #randomize ball speed
        platform_color = change_platform_color()

    # Check if ball falls off screen
    if ball_pos[1] >= HEIGHT:
        # Decrease lives
        lives -= 1
        if lives == 0:
            game_over_screen()
            start_screen() # restart game aft game over
            score = 0
            lives = 3
            current_level = 1
        else:
            # Reset ball position
            ball_pos = [WIDTH // 2, HEIGHT // 2]

            # Randomise ball speed
            ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]

    # Clear screen
    screen.fill(BLACK)

    # Draw ball
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Draw platform
    pygame.draw.rect(screen, platform_color, (int(platform_pos[0]), int(platform_pos[1]), PLATFORM_WIDTH, PLATFORM_HEIGHT))

    # Display information
    info_line_y = 10 #adjust vertical pos as needed
    info_spacing = 75 #adjust spacing as needed

    # Draw score in orange rect at top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw level indicator in light-blue rect at top left
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw lives in red rect at top left
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, RED, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
