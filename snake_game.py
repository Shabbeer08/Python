import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 15

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize the clock
clock = pygame.time.Clock()

# Initialize the snake
snake = [(5, 5)]
snake_direction = (1, 0)

# Initialize the food
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Initialize the score
score = 0

# Initialize font
font = pygame.font.Font(None, 36)

def draw_score():
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

def game_over():
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 18))
    score_text = font.render(f"Total Score: {score}", True, GREEN)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 18))
    options_text = font.render("Quit (Q)", True, GREEN)
    screen.blit(options_text, (SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2 + 64))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    return False  # Quit

running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            if event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            if event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            if event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)
            if event.key == pygame.K_p:
                paused = not paused

    if paused:
        continue  # Skip the game logic while paused

    # Update snake
    x, y = snake[0]
    x += snake_direction[0]
    y += snake_direction[1]

    # Allow the snake to go through the wall
    if x < 0:
        x = GRID_WIDTH - 1
    elif x >= GRID_WIDTH:
        x = 0
    if y < 0:
        y = GRID_HEIGHT - 1
    elif y >= GRID_HEIGHT:
        y = 0

    snake.insert(0, (x, y))

    # Check for collisions
    if snake[0] == food:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score += 1
    else:
        snake.pop()

    # Check for game over
    if snake[0] in snake[1:]:
        running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw food
    pygame.draw.rect(
        screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )

    # Draw snake
    for segment in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )

    # Draw the score
    draw_score()

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(SNAKE_SPEED)

# Game over screen
while True:
    if game_over():
        snake = [(5, 5)]
        snake_direction = (1, 0)
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score = 0
        running = True
        paused = False
    else:
        break

# Quit Pygame
pygame.quit()
