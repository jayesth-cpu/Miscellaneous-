import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple FPS Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_pos = [width // 2, height // 2]
player_angle = 0
player_speed = 3

# Walls
walls = [
    pygame.Rect(100, 100, 20, 400),
    pygame.Rect(300, 200, 400, 20),
    pygame.Rect(600, 300, 20, 200),
]

# Targets
targets = [
    {"pos": [200, 200], "alive": True},
    {"pos": [600, 100], "alive": True},
    {"pos": [700, 500], "alive": True},
]

# Bullet
bullet = None
BULLET_SPEED = 10
BULLET_LIFETIME = 60


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def ray_cast(start_pos, angle):
    for _ in range(1000):  # Maximum distance
        x = start_pos[0] + math.cos(angle) * _
        y = start_pos[1] + math.sin(angle) * _

        # Check collision with walls
        for wall in walls:
            if wall.collidepoint(x, y):
                return (x, y)

        # Check collision with targets
        for target in targets:
            if target["alive"] and distance((x, y), target["pos"]) < 20:
                return (x, y)

    return (x, y)


# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if bullet is None:
                bullet = {
                    "pos": player_pos.copy(),
                    "angle": player_angle,
                    "lifetime": BULLET_LIFETIME,
                }

    # Handle player movement
    keys = pygame.key.get_pressed()
    move_x = move_y = 0
    if keys[pygame.K_w]:
        move_x += math.cos(player_angle) * player_speed
        move_y += math.sin(player_angle) * player_speed
    if keys[pygame.K_s]:
        move_x -= math.cos(player_angle) * player_speed
        move_y -= math.sin(player_angle) * player_speed
    if keys[pygame.K_a]:
        player_angle -= 0.05
    if keys[pygame.K_d]:
        player_angle += 0.05

    # Check wall collisions before moving
    new_rect = pygame.Rect(
        player_pos[0] + move_x - 10, player_pos[1] + move_y - 10, 20, 20
    )
    if not any(wall.colliderect(new_rect) for wall in walls):
        player_pos[0] += move_x
        player_pos[1] += move_y

    # Update bullet
    if bullet:
        bullet["pos"][0] += math.cos(bullet["angle"]) * BULLET_SPEED
        bullet["pos"][1] += math.sin(bullet["angle"]) * BULLET_SPEED
        bullet["lifetime"] -= 1

        # Check bullet collision with walls
        if any(wall.collidepoint(bullet["pos"]) for wall in walls):
            bullet = None

        # Check bullet collision with targets
        for target in targets:
            if target["alive"] and distance(bullet["pos"], target["pos"]) < 20:
                target["alive"] = False
                bullet = None
                break

        if bullet and bullet["lifetime"] <= 0:
            bullet = None

    # Clear the screen
    display.fill(BLACK)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(display, WHITE, wall)

    # Draw targets
    for target in targets:
        if target["alive"]:
            pygame.draw.circle(display, RED, target["pos"], 20)

    # Draw player
    pygame.draw.circle(display, GREEN, (int(player_pos[0]), int(player_pos[1])), 10)

    # Ray casting
    for i in range(-30, 31, 2):
        angle = player_angle + math.radians(i)
        end_pos = ray_cast(player_pos, angle)
        pygame.draw.line(display, (100, 100, 100), player_pos, end_pos)

    # Draw bullet
    if bullet:
        pygame.draw.circle(
            display, WHITE, (int(bullet["pos"][0]), int(bullet["pos"][1])), 5
        )

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
