#Hello
import pygame
import random
import math

# Simulation settings
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 40
ANT_COUNT = 50
ANT_RADIUS = 6
ANT_SPEED = 1.2
SPAWN_INTERVAL = 700
WANDER_CHANCE = 0.02

# Underground colony entrances
HOLES = [
    (150, 150),
    (650, 150),
    (400, 450)
]

# Colors
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BROWN = (130, 70, 30)
DARK_BROWN = (65, 35, 20)
DIRT = (165, 110, 65)


class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * ANT_SPEED
        self.vy = math.sin(angle) * ANT_SPEED

    def move(self):
        # Occasionally change direction
        if random.random() < WANDER_CHANCE:
            angle = math.atan2(self.vy, self.vx)
            angle += random.uniform(-0.5, 0.5)

            self.vx = math.cos(angle) * ANT_SPEED
            self.vy = math.sin(angle) * ANT_SPEED

        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x <= ANT_RADIUS or self.x >= WIDTH - ANT_RADIUS:
            self.vx *= -1
            self.x = max(ANT_RADIUS, min(self.x, WIDTH - ANT_RADIUS))

        if self.y <= ANT_RADIUS or self.y >= HEIGHT - ANT_RADIUS:
            self.vy *= -1
            self.y = max(ANT_RADIUS, min(self.y, HEIGHT - ANT_RADIUS))

    def draw(self, screen):
        body = (int(self.x), int(self.y))

        angle = math.atan2(self.vy, self.vx)
        head = (
            int(self.x + math.cos(angle) * 8),
            int(self.y + math.sin(angle) * 8)
        )

        pygame.draw.circle(screen, BROWN, body, ANT_RADIUS)
        pygame.draw.circle(screen, DARK_BROWN, head, 3)


def check_collision(ant1, ant2):
    dx = ant2.x - ant1.x
    dy = ant2.y - ant1.y
    distance = math.sqrt(dx**2 + dy**2)

    if 0 < distance < ANT_RADIUS * 2:
        nx = dx / distance
        ny = dy / distance

        # Separate overlapping ants
        overlap = ANT_RADIUS * 2 - distance
        ant1.x -= nx * overlap / 2
        ant1.y -= ny * overlap / 2
        ant2.x += nx * overlap / 2
        ant2.y += ny * overlap / 2

        # Bounce when moving toward each other
        relative_speed = (
            (ant1.vx - ant2.vx) * nx
            + (ant1.vy - ant2.vy) * ny
        )

        if relative_speed > 0:
            ant1.vx -= relative_speed * nx
            ant1.vy -= relative_speed * ny
            ant2.vx += relative_speed * nx
            ant2.vy += relative_speed * ny


def draw_holes(screen):
    for x, y in HOLES:
        pygame.draw.circle(screen, DIRT, (x, y), 24)
        pygame.draw.circle(screen, DARK_BROWN, (x, y), 17)


def spawn_ant(ants):
    # Find entrances that do not have an ant blocking them
    available_holes = []

    for x, y in HOLES:
        blocked = False

        for ant in ants:
            distance = math.hypot(ant.x - x, ant.y - y)

            if distance < ANT_RADIUS * 2 + 2:
                blocked = True
                break

        if not blocked:
            available_holes.append((x, y))

    if available_holes:
        x, y = random.choice(available_holes)
        ants.append(Ant(x, y))


# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ant Colony Simulation")
clock = pygame.time.Clock()

# Begin with no ants
ants = []

last_spawn_time = pygame.time.get_ticks()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn ants at regular intervals
    current_time = pygame.time.get_ticks()

    if current_time - last_spawn_time >= SPAWN_INTERVAL:
        if len(ants) < ANT_COUNT:
            spawn_ant(ants)

        last_spawn_time = current_time

    # Move ants
    for ant in ants:
        ant.move()

    # Check collisions
    for i in range(len(ants)):
        for j in range(i + 1, len(ants)):
            check_collision(ants[i], ants[j])

    # Draw background
    screen.fill(WHITE)

    # Draw grid
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Draw underground entrances
    draw_holes(screen)

    # Draw ants
    for ant in ants:
        ant.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
# Run the Code: py -V:3.14 Antfarm.py