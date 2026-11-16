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

async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())