import pygame
import sys
from sorting_algorithms import MergeSort, BubbleSort

pygame.init()
# WINDOW DIMENSIONS
WIDTH = 1024
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
    pos_x = WIDTH // len(array)
    for i in range(len(array)):
        pygame.draw.line(WIN, GREEN,
                         (pos_x * i, HEIGHT),
                         (pos_x * i, HEIGHT - array[i]),
                         WIDTH // len(array))


def check_events(array, algorithm):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.key == pygame.K_r:
                array = algorithm.generate_array()
            elif event.key == pygame.K_RETURN:
                algorithm.algorithm()

    return array


def update(array):
    pygame.time.wait(25)
    draw_bars(array)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    algo = BubbleSort()
    array = algo.array
    while run:
        WIN.fill(WHITE)
        if array:
            draw_bars(array)
        clock.tick(FPS)
        array = check_events(array, algo)
        pygame.display.update()


if __name__ == '__main__':
    main()
