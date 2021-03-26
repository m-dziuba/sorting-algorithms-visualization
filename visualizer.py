import pygame
import sys
from sorting_algorithms import QuickSort  # SelectionSort, BubbleSort

pygame.init()
# VISUALIZER WINDOW DIMENSIONS
VISUALIZER_WIDTH = 1024
VISUALIZER_HEIGHT = 800


# COLOURS
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# BARS

# BUTTONS
BUTTON_WIDTH = 0
BUTTON_HEIGHT = 100
BUTTON_SPACING = 0
BORDER_WIDTH = 0
BORDER_HEIGHT = 0

# MENU
MENU_HEIGHT = BUTTON_HEIGHT * 2


# WINDOW
WINDOW_HEIGHT = VISUALIZER_HEIGHT + MENU_HEIGHT
WIN = pygame.display.set_mode((VISUALIZER_WIDTH, WINDOW_HEIGHT))
FPS = 60
pygame.display.set_caption("Sorting visualizer")


def draw_bars(array):
    WIN.fill(WHITE)
    pos_x = VISUALIZER_WIDTH // len(array)
    for i in range(len(array)):
        pygame.draw.line(WIN, GREEN,
                         (pos_x * i, WINDOW_HEIGHT),
                         (pos_x * i, WINDOW_HEIGHT - array[i] * VISUALIZER_HEIGHT // len(array)),
                         VISUALIZER_WIDTH // len(array))


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


def draw_text(text, font, colour, surface, x, y):
    text_obj = font.render(text, True, colour)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def create_button(text, font, colour, button_number):
    button = pygame.Rect((VISUALIZER_WIDTH - BUTTON_WIDTH) // 2, button_number * BUTTON_SPACING,
                         BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(WIN, colour, button, BORDER_WIDTH, BORDER_WIDTH)
    draw_text(text, font, colour, WIN, VISUALIZER_WIDTH // 2,
              button_number * BUTTON_SPACING + BUTTON_HEIGHT // 2)
    return button


def update(array):
    pygame.time.wait(1)
    draw_bars(array)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    algo = QuickSort()
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
