import pygame
import sys
from sorting_algorithms import *

pygame.init()
# ---------------- VISUALIZER ---------------- #
# VISUALIZER WINDOW DIMENSIONS
VISUALIZER_WIDTH = 1024
VISUALIZER_HEIGHT = 1000 - 80

# COLOURS
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# BARS
INSPECTED_COLOUR = BLUE
COMPARED_COLOUR = RED
BASE_COLOUR = GREEN

# BUTTONS
BUTTONS_TOTAL_NO = 6
BUTTONS_LIMIT_PER_ROW = 6
BUTTON_SPACING = 32
BUTTON_HEIGHT = 64
BUTTONS_FONTS = "assets\\Ticketing.ttf"
BUTTON_WIDTH = VISUALIZER_WIDTH // BUTTONS_LIMIT_PER_ROW
BUTTONS_FONT_SIZE = 24
BUTTONS_BORDER_WIDTH = 2

# COMMAND BUTTONS
COMMAND_BUTTONS = ("play", "left", "right", "reload")
COMMAND_BUTTONS_IMAGES = {"play": "assets\\play_button.png",
                          "pause": "assets\\pause_button.png",
                          "stop": "assets\\stop_button.png",
                          "left": "assets\\left_button.png",
                          "right": "assets\\right_button.png",
                          "reload": "assets\\reload_button.png",
                          }
COMMAND_BUTTONS_RECTS = {"play": (BUTTON_WIDTH + BUTTON_SPACING, 0, 64, 64),
                         "pause": (BUTTON_WIDTH + BUTTON_SPACING, 0, 64, 64),
                         "reload": (BUTTON_WIDTH + BUTTON_SPACING * 4, 0, 64, 64),
                         "stop": (BUTTON_WIDTH + BUTTON_SPACING * 4, 0, 64, 64),
                         "left": (BUTTON_WIDTH + BUTTON_SPACING * 7, 0, 64, 64),
                         "right": (BUTTON_WIDTH + BUTTON_SPACING * 13 + 4, 0, 64, 64),
                         }


# MAIN MENU
MAIN_MENU_HEIGHT = BUTTON_HEIGHT
MAIN_MENU = (0, 0, VISUALIZER_WIDTH, MAIN_MENU_HEIGHT + BUTTONS_BORDER_WIDTH)

# BUTTONS MENU
BUTTONS_MENU_HEIGHT = BUTTON_HEIGHT * (1 + BUTTONS_TOTAL_NO //
                                       (BUTTONS_LIMIT_PER_ROW + 1)) + BUTTONS_BORDER_WIDTH // 2
BUTTONS_MENU = (0, 0, VISUALIZER_WIDTH, BUTTONS_MENU_HEIGHT)

# WINDOW
WINDOW_HEIGHT = VISUALIZER_HEIGHT + MAIN_MENU_HEIGHT
FPS = 200
WIN = pygame.display.set_mode((VISUALIZER_WIDTH, WINDOW_HEIGHT))
VISUALIZER_RECT = pygame.Rect(0, MAIN_MENU_HEIGHT, VISUALIZER_WIDTH, VISUALIZER_HEIGHT)
pygame.display.set_caption("Sorting visualizer")


# ---------------- SORTING_ALGORITHMS ---------------- #
ARRAY_LENGTH = len(initial_array)
BAR_WIDTH = VISUALIZER_WIDTH // ARRAY_LENGTH


class SortButton:

    def __init__(self, name, button_number, colour=BLACK, secondary_colour=GREEN, text=None,
                 font=BUTTONS_FONTS, font_size=BUTTONS_FONT_SIZE):
        self.name = name
        self.colour = colour
        self.current_colour = colour
        self.secondary_colour = secondary_colour
        self.button_number = button_number
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.column = button_number % BUTTONS_LIMIT_PER_ROW
        self.row = button_number // BUTTONS_LIMIT_PER_ROW
        self.rect = pygame.Rect(self.column * BUTTON_WIDTH, self.row * BUTTON_HEIGHT,
                                BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw(self):
        self.mouseover()
        pygame.draw.rect(WIN, self.current_colour, self.rect, BUTTONS_BORDER_WIDTH)

        if self.text:
            text_obj = self.font.render(self.text, True, self.current_colour)
            text_rect = text_obj.get_rect()
            text_rect.center = (((self.column + 0.5) * BUTTON_WIDTH), ((self.row + 0.5) * BUTTON_HEIGHT))
            WIN.blit(text_obj, text_rect)

    def mouseover(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.current_colour = self.secondary_colour

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            return eval(self.name)

    def menu_mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            return True


class CommandButton:

    def __init__(self, name):
        self.name = name
        self.rect = pygame.Rect(COMMAND_BUTTONS_RECTS[self.name])

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)
        WIN.blit(pygame.image.load(COMMAND_BUTTONS_IMAGES[self.name]), COMMAND_BUTTONS_RECTS[self.name])
        pygame.display.update(self.rect)

    def mouse_click(self, click=False):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos) and click:
            return True


class InputBox:

    def __init__(self, name, sth="1024"):
        self.name = name
        self.rect = pygame.Rect(BUTTON_WIDTH + BUTTON_SPACING * 9, 0, BUTTON_SPACING * 4, 64)
        self.current_colour = BLACK
        self.secondary_colour = GREEN
        self.pos = pygame.mouse.get_pos()
        self.text_list = [number for number in sth]
        self.font = pygame.font.Font(BUTTONS_FONTS, BUTTONS_FONT_SIZE)
        self.text = "".join(number for number in self.text_list)

    def draw(self):
        pass
    #     self.mouseover()
    #     pygame.draw.rect(WIN, WHITE, self.rect)
    #     pygame.draw.rect(WIN, self.current_colour, self.rect, 2)
    #
    #     if self.text:
    #         text_obj = self.font.render(self.text, True, self.current_colour)
    #         text_rect = text_obj.get_rect()
    #         text_rect.center = (BUTTON_WIDTH + BUTTON_SPACING * 9 + BUTTON_SPACING * 4//2, 64//2)
    #         WIN.blit(text_obj, text_rect)
        pygame.display.update(self.rect)

    def mouseover(self):
        if self.rect.collidepoint(*self.pos):
            self.current_colour = self.secondary_colour

    def mouse_click(self, click=False):
        if self.rect.collidepoint(*self.pos) and click:
            return True

    def handle_event(self):
        active = True
        while active:
            for event in pygame.event.get():
                basic_check_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(*self.pos):
                        active = not active
                    else:
                        active = False
                    self.current_colour = GREY if active else BLACK
                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_list = self.text_list[:-1]
                        self.text = "".join(number for number in self.text_list)
                        self.draw()
                    else:
                        self.text_list += event.unicode
                        self.text = "".join(number for number in self.text_list)
                    self.draw()
        return self


class ArraySizeDisplay:

    def __init__(self):
        self.size = ARRAY_LENGTH
        self.rect = pygame.Rect(BUTTON_WIDTH + BUTTON_SPACING * 9, 0, BUTTON_SPACING * 4, 64)
        self.colour = BLACK
        self.text = str(self.size)
        self.font = pygame.font.Font(BUTTONS_FONTS, BUTTONS_FONT_SIZE)

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)
        pygame.draw.rect(WIN, self.colour, self.rect, 2)
        text_obj = self.font.render(self.text, True, self.colour)
        text_rect = text_obj.get_rect()
        text_rect.center = (BUTTON_WIDTH + BUTTON_SPACING * 9 + BUTTON_SPACING * 4 // 2, 64 // 2)
        WIN.blit(text_obj, text_rect)
        pygame.display.update(self.rect)

    def decrease(self, algorithm):
        global ARRAY_LENGTH, BAR_WIDTH
        if self.size > 2:
            self.size //= 2
            self.text = str(self.size)
            ARRAY_LENGTH = self.size
            BAR_WIDTH = VISUALIZER_WIDTH // ARRAY_LENGTH
            algorithm.array_length = self.size
            algorithm.generate_array()
        self.draw()
        pygame.display.update()

    def increase(self, algorithm):
        global ARRAY_LENGTH, BAR_WIDTH
        if self.size < 1024:
            self.size *= 2
            self.text = str(self.size)
            ARRAY_LENGTH = self.size
            BAR_WIDTH = VISUALIZER_WIDTH // ARRAY_LENGTH
            algorithm.array_length = self.size
            algorithm.generate_array()
        self.draw()
        pygame.display.update()


def draw_one_bar(bar, array, mode=None, single_bar=True):
    if mode == "inspected":
        colour = INSPECTED_COLOUR
    elif mode == "compared":
        colour = COMPARED_COLOUR
    else:
        colour = BASE_COLOUR

    pygame.draw.line(WIN, WHITE,
                     (BAR_WIDTH * (bar + 0.5), WINDOW_HEIGHT),
                     (BAR_WIDTH * (bar + 0.5), BUTTON_HEIGHT + 0.5 * BUTTONS_BORDER_WIDTH),
                     BAR_WIDTH + 1)
    pygame.draw.line(WIN, colour,
                     (BAR_WIDTH * (bar + 0.5), WINDOW_HEIGHT),
                     (BAR_WIDTH * (bar + 0.5), WINDOW_HEIGHT - array[bar] * VISUALIZER_HEIGHT // VISUALIZER_WIDTH),
                     BAR_WIDTH + 1)
    if single_bar:
        pygame.display.update((BAR_WIDTH * bar, MAIN_MENU_HEIGHT, BAR_WIDTH, VISUALIZER_HEIGHT))


def draw_bars(array, start=0, end=None):
    if end is None:
        end = len(array)
    global BAR_WIDTH, VISUALIZER_WIDTH
    BAR_WIDTH = VISUALIZER_WIDTH // end
    for i in range(start, end):
        draw_one_bar(i, array, single_bar=False)
    pygame.display.update((BAR_WIDTH * start, MAIN_MENU_HEIGHT,
                           BAR_WIDTH * (end - start), VISUALIZER_HEIGHT))


def draw_main_menu(algorithm, array_size):
    for action_button in COMMAND_BUTTONS:
        CommandButton(action_button).draw()
    SortButton(algorithm.name, 0, text=f"{algorithm.name[0:-4]} Sort").draw()
    array_size.draw()


def draw_sort_menu(all_algorithms):
    for index, algorithms in enumerate(all_algorithms):
        SortButton(algorithms[0], index, text=algorithms[1]).draw()


def get_all_algorithms(cls):
    all_algorithms = [(f"{subclass.__name__}()", f"{subclass.__name__[:-4]} Sort")
                      for subclass in cls.__subclasses__()]
    return all_algorithms


def basic_check_event(event):
    click = False
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            click = True
    return click


def check_events_while_running():
    pause = False
    for event in pygame.event.get():
        click = basic_check_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = True

        button = CommandButton("pause")
        button.draw()
        if button.mouse_click(click):
            pause = True
        button = CommandButton("stop")
        button.draw()
        if button.mouse_click(click):
            main()

    while pause:
        pause = check_events_while_paused()


def check_events_while_paused():
    for event in pygame.event.get():
        click = basic_check_event(event)
        button = CommandButton("play")
        button.draw()
        if button.mouse_click(click):
            return False
        button = CommandButton("stop")
        button.draw()
        if button.mouse_click(click):
            main()
    return True


def check_events_while_in_sort_menu(algorithm, all_algorithms, event):
    click = basic_check_event(event)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            algorithm.generate_array()
    for index, algorithms in enumerate(all_algorithms):
        button = SortButton(algorithms[0], index, text=algorithms[1])
        if click:
            if button.mouse_click():
                return button.mouse_click(), False
    if click and pygame.mouse.get_pos()[1] > BUTTONS_MENU_HEIGHT:
        return algorithm, False
    return algorithm, True


def check_events_while_in_main_menu(algorithm, event, all_algorithms, array_size):
    click = basic_check_event(event)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            algorithm.generate_array()
        elif event.key == pygame.K_RETURN:
            algorithm.algorithm()
    elif click and SortButton(algorithm.name, 0, text=f"{algorithm.name[0:-4]} Sort").menu_mouse_click():
        return sort_menu(algorithm, all_algorithms)
    else:
        for action_button in COMMAND_BUTTONS:
            button = CommandButton(action_button)
            if button.name == "play" and button.mouse_click(click):
                algorithm.algorithm()
            elif button.name == "reload" and button.mouse_click(click):
                algorithm.generate_array()
            elif button.name == "left" and button.mouse_click(click):
                array_size.decrease(algorithm)
            elif button.name == "right" and button.mouse_click(click):
                array_size.increase(algorithm)

    return algorithm


def sort_menu(algorithm, all_algorithms):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        pygame.draw.rect(WIN, GREY, BUTTONS_MENU)
        draw_sort_menu(all_algorithms)
        for event in pygame.event.get():
            algorithm, run = check_events_while_in_sort_menu(algorithm, all_algorithms, event)
        pygame.display.update(BUTTONS_MENU)
    return algorithm


def main():
    clock = pygame.time.Clock()
    all_algorithms = get_all_algorithms(Algorithm)
    algorithm = SelectionSort()
    algorithm.generate_array()
    WIN.fill(WHITE)
    draw_bars(algorithm.array)
    array_size = ArraySizeDisplay()
    while True:
        clock.tick(FPS)
        pygame.draw.rect(WIN, WHITE, MAIN_MENU)
        draw_main_menu(algorithm, array_size)
        for event in pygame.event.get():
            algorithm = check_events_while_in_main_menu(algorithm, event, all_algorithms, array_size)
        pygame.display.update()


if __name__ == '__main__':
    main()

# TODO review code cleanliness
# TODO Buttons can be optimized
