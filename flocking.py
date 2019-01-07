import sys
import pygame
import boid
from boid import Boid

pygame.init()

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
surface = pygame.display.set_mode(screen)
pygame.display.set_caption('Boids')
clock = pygame.time.Clock()

boid.init(DISPLAY_WIDTH, DISPLAY_HEIGHT, surface)

def createBoids(n, array):
    for i in range(0, n):
        array.append(Boid(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2))

def main():
    """Main animation loop"""
    n = 100
    pop = []
    createBoids(n, pop)
    stop = False

    while not stop:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                stop = True
        
        surface.fill(BLACK)

        for boid in pop:
            boid.run(pop)
        
        pygame.display.update()

        clock.tick(60)

main()
pygame.quit()
sys.exit()
