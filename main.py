import asyncio
import pygame
import random

pygame.init()
random.seed()

WIDTH = 1300
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Best Path")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

points = []

def setup_grid(columns, rows, grid_size):
    global points
    points = []
    offset_x = (WIDTH - grid_size*(columns-1))/2
    offset_y = (HEIGHT - grid_size*(rows-1))/2
    for i in range(columns):
        for i2 in range(rows):
            points.append([i*grid_size+offset_x, i2*grid_size+offset_y, []])
    for i, p in enumerate(points):
        for i2, p2 in enumerate(points):
            if p2 != p:
                dist = ((p[0]-p2[0])**2+(p[1]-p2[1])**2)
                if dist <= grid_size**2 and (i not in p2[2]) and (i2 not in p[2]):
                    p[2].append(i2)
                    p2[2].append(i)
def draw_points():
    for p in points:
        for l in p[2]:
            pygame.draw.line(screen, (155, 155, 155), (p[0], p[1]), (points[l][0], points[l][1]), 5)
    for p in points:
        pygame.draw.circle(screen, (255,255,255), (p[0], p[1]), 10)

def draw():
    draw_points()

setup_grid(10, 10, 80)
async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        draw()
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())