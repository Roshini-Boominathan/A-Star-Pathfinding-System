import pygame
from queue import PriorityQueue
import math

pygame.init()

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding System")

ROWS = 20
GAP = WIDTH // ROWS

# COLORS
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)  # weighted nodes

# GRID
grid = [[WHITE for _ in range(ROWS)] for _ in range(ROWS)]
weights = [[1 for _ in range(ROWS)] for _ in range(ROWS)]

start = None
end = None


def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def get_neighbors(node):
    neighbors = []
    r, c = node

    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),   # straight
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonal
    ]

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < ROWS:
            neighbors.append((nr, nc))

    return neighbors


def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if grid[current[0]][current[1]] not in (GREEN, RED):
            grid[current[0]][current[1]] = YELLOW


def a_star():
    open_set = PriorityQueue()
    open_set.put((0, 0, start))

    came_from = {}

    g_score = {(i, j): float("inf") for i in range(ROWS) for j in range(ROWS)}
    g_score[start] = 0

    f_score = {(i, j): float("inf") for i in range(ROWS) for j in range(ROWS)}
    f_score[start] = heuristic(start, end)

    open_set_hash = {start}
    count = 0

    while not open_set.empty():
        pygame.time.delay(20)  # animation speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)
            return True

        for neighbor in get_neighbors(current):
            r, c = neighbor

            if grid[r][c] == BLACK:
                continue

            temp_g = g_score[current] + weights[r][c]

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor, end)

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

                    if grid[r][c] not in (GREEN, RED, ORANGE):
                        grid[r][c] = BLUE

        draw(WIN)

    return False


def draw(win):
    win.fill(WHITE)

    for i in range(ROWS):
        for j in range(ROWS):
            pygame.draw.rect(win, grid[i][j], (j * GAP, i * GAP, GAP, GAP))

    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * GAP), (WIDTH, i * GAP))
        pygame.draw.line(win, GREY, (i * GAP, 0), (i * GAP, WIDTH))

    pygame.display.update()


def get_clicked_pos(pos):
    x, y = pos
    return y // GAP, x // GAP


def reset():
    global grid, weights, start, end
    grid = [[WHITE for _ in range(ROWS)] for _ in range(ROWS)]
    weights = [[1 for _ in range(ROWS)] for _ in range(ROWS)]
    start = None
    end = None


run = True
while run:
    draw(WIN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_clicked_pos(pygame.mouse.get_pos())

            # LEFT CLICK
            if event.button == 1:
                if not start:
                    start = (row, col)
                    grid[row][col] = GREEN

                elif not end:
                    end = (row, col)
                    grid[row][col] = RED

                else:
                    grid[row][col] = BLACK

            # RIGHT CLICK (erase)
            elif event.button == 3:
                grid[row][col] = WHITE
                weights[row][col] = 1

                if (row, col) == start:
                    start = None
                elif (row, col) == end:
                    end = None

            # MIDDLE CLICK (weighted node)
            elif event.button == 2:
                grid[row][col] = ORANGE
                weights[row][col] = 5  # heavier cost

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:
                a_star()

            if event.key == pygame.K_c:
                reset()

pygame.quit()