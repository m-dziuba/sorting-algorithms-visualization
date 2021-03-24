import pygame
import sys
import numpy as np

pygame.init()
# WINDOW DIMENSIONS
WIDTH = 800
HEIGHT = 800

# WINDOW
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("Sorting visualizer")

# COLOURS
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# BARS


def draw_bars(array):
    WIN.fill(WHITE)
    for i in range(len(array)):
        pygame.draw.line(WIN, GREEN,
                         (WIDTH // (len(array)) * i, 0),
                         (WIDTH // (len(array)) * i, array[i]),
                         WIDTH // len(array))


def generate_array(max_number, size):
    return [np.random.randint(max_number, size=size)[i] for i in range(size)]


def main():
    run = True
    clock = pygame.time.Clock()
    array = generate_array(800, 100)
    while run:
        WIN.fill(WHITE)
        if array:
            draw_bars(array)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                elif event.key == pygame.K_r:
                    array = generate_array(800, 100)
        pygame.display.update()


if __name__ == '__main__':
    main()
