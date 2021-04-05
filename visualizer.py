import pygame
import sys
import config as cfg
import sorting_algorithms as sa

pygame.init()


class SortButton:

    def __init__(self, name, button_number, colour=cfg.BLACK, secondary_colour=cfg.GREEN, text=None,
                 font=cfg.BUTTONS_FONTS, font_size=cfg.BUTTONS_FONT_SIZE):
        self.name = name
        self.colour = colour
        self.current_colour = colour
        self.secondary_colour = secondary_colour
        self.button_number = button_number
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.column = button_number % cfg.BUTTONS_LIMIT_PER_ROW
        self.row = button_number // cfg.BUTTONS_LIMIT_PER_ROW
        self.rect = pygame.Rect(self.column * cfg.BUTTON_WIDTH, self.row * cfg.BUTTON_HEIGHT,
                                cfg.BUTTON_WIDTH, cfg.BUTTON_HEIGHT)

    def draw(self):
        self.mouseover()
        pygame.draw.rect(cfg.WIN, self.current_colour, self.rect, cfg.BUTTONS_BORDER_WIDTH)

        if self.text:
            text_obj = self.font.render(self.text, True, self.current_colour)
            text_rect = text_obj.get_rect()
            text_rect.center = (((self.column + 0.5) * cfg.BUTTON_WIDTH), ((self.row + 0.5) * cfg.BUTTON_HEIGHT))
            cfg.WIN.blit(text_obj, text_rect)

    def mouseover(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.current_colour = self.secondary_colour

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            return eval("sa." + self.name)

    def menu_mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            return True


class CommandButton:

    def __init__(self, name):
        self.name = name
        self.rect = pygame.Rect(cfg.COMMAND_BUTTONS_RECTS[self.name])

    def draw(self):
        pygame.draw.rect(cfg.WIN, cfg.WHITE, self.rect)
        cfg.WIN.blit(pygame.image.load(cfg.COMMAND_BUTTONS_IMAGES[self.name]), cfg.COMMAND_BUTTONS_RECTS[self.name])
        pygame.display.update(self.rect)

    def mouse_click(self, click=False):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos) and click:
            return True


class InputBox:

    def __init__(self):
        self.rect = pygame.Rect(cfg.BUTTON_WIDTH + cfg.BUTTON_SPACING * 20, 0, cfg.BUTTON_SPACING * 4, 64)
        self.primary_colour = cfg.BLACK
        self.secondary_colour = cfg.GREEN
        self.current_colour = self.primary_colour
        self.font = pygame.font.Font(cfg.BUTTONS_FONTS, cfg.BUTTONS_FONT_SIZE)
        self.text = str(cfg.DELAY)

    def draw(self):
        self.mouseover()
        pygame.draw.rect(cfg.WIN, cfg.WHITE, self.rect)
        pygame.draw.rect(cfg.WIN, self.current_colour, self.rect, 2)

        if self.text:
            text_obj = self.font.render(self.text, True, self.current_colour)
            text_rect = text_obj.get_rect()
            text_rect.center = (cfg.BUTTON_WIDTH + cfg.BUTTON_SPACING * 20 + cfg.BUTTON_SPACING * 4//2, 64//2)
            cfg.WIN.blit(text_obj, text_rect)
        pygame.display.update(self.rect)

    def mouseover(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.current_colour = self.secondary_colour
        else:
            self.current_colour = self.primary_colour

    def mouse_click(self, click=False):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos) and click:
            return True

    def handle_event(self):
        active = True
        previous_text = self.text
        self.text = ""
        while active:
            self.current_colour = cfg.GREEN
            for event in pygame.event.get():
                basic_check_event(event)
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(*pos):
                        active = not active
                    else:
                        active = False

                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
                                       pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                        self.text += event.unicode

            self.draw()
        if self.text == "":
            self.text = previous_text


class ArraySizeDisplay:

    def __init__(self):
        self.size = cfg.ARRAY_LENGTH
        self.rect = pygame.Rect(cfg.BUTTON_WIDTH + cfg.BUTTON_SPACING * 9, 0, cfg.BUTTON_SPACING * 4, 64)
        self.colour = cfg.BLACK
        self.text = str(self.size)
        self.font = pygame.font.Font(cfg.BUTTONS_FONTS, cfg.BUTTONS_FONT_SIZE)

    def draw(self):
        pygame.draw.rect(cfg.WIN, cfg.WHITE, self.rect)
        pygame.draw.rect(cfg.WIN, self.colour, self.rect, 2)
        text_obj = self.font.render(self.text, True, self.colour)
        text_rect = text_obj.get_rect()
        text_rect.center = (cfg.BUTTON_WIDTH + cfg.BUTTON_SPACING * 9 + cfg.BUTTON_SPACING * 4 // 2, 64 // 2)
        cfg.WIN.blit(text_obj, text_rect)
        pygame.display.update(self.rect)

    def decrease(self, algorithm):
        if self.size > 2:
            self.size //= 2
            self.text = str(self.size)
            cfg.ARRAY_LENGTH = self.size
            cfg.BAR_WIDTH = cfg.VISUALIZER_WIDTH // cfg.ARRAY_LENGTH
            algorithm.array_length = self.size
            algorithm.generate_array()
        self.draw()
        pygame.display.update()
        return algorithm

    def increase(self, algorithm):
        if self.size < 1024:
            self.size *= 2
            self.text = str(self.size)
            cfg.ARRAY_LENGTH = self.size
            cfg.BAR_WIDTH = cfg.VISUALIZER_WIDTH // cfg.ARRAY_LENGTH
            algorithm.array_length = self.size
            algorithm.generate_array()
        self.draw()
        pygame.display.update()
        return algorithm


def draw_one_bar(bar, array, mode=None, single_bar=True):
    if mode == "inspected":
        colour = cfg.INSPECTED_COLOUR
    elif mode == "compared":
        colour = cfg.COMPARED_COLOUR
    else:
        colour = cfg.BASE_COLOUR

    pygame.draw.line(cfg.WIN, cfg.WHITE,
                     (cfg.BAR_WIDTH * (bar + 0.5), cfg.WINDOW_HEIGHT),
                     (cfg.BAR_WIDTH * (bar + 0.5), cfg.BUTTON_HEIGHT + 0.5 * cfg.BUTTONS_BORDER_WIDTH),
                     cfg.BAR_WIDTH + 1)
    pygame.draw.line(cfg.WIN, colour,
                     (cfg.BAR_WIDTH * (bar + 0.5), cfg.WINDOW_HEIGHT),
                     (cfg.BAR_WIDTH * (bar + 0.5),
                      cfg.WINDOW_HEIGHT - array[bar] * cfg.VISUALIZER_HEIGHT // cfg.VISUALIZER_WIDTH),
                     cfg.BAR_WIDTH + 1)
    if single_bar:
        pygame.display.update((cfg.BAR_WIDTH * bar, cfg.MAIN_MENU_HEIGHT, cfg.BAR_WIDTH, cfg.VISUALIZER_HEIGHT))
        pygame.time.delay(cfg.DELAY)


def draw_bars(array, array_length, start=0, end=None):
    if end is None:
        end = len(array)
    cfg.BAR_WIDTH = cfg.VISUALIZER_WIDTH // array_length
    for i in range(start, end):
        draw_one_bar(i, array, single_bar=False)
    pygame.display.update((cfg.BAR_WIDTH * start, cfg.MAIN_MENU_HEIGHT,
                           cfg.BAR_WIDTH * (end - start), cfg.VISUALIZER_HEIGHT))
    pygame.time.delay(cfg.DELAY)


def draw_main_menu(algorithm, array_size, delay_input_box):
    for action_button in cfg.COMMAND_BUTTONS:
        CommandButton(action_button).draw()
    SortButton(algorithm.name, 0, text=f"{algorithm.name[0:-4]} Sort").draw()
    array_size.draw()
    delay_input_box.draw()


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
    if click and pygame.mouse.get_pos()[1] > cfg.BUTTONS_MENU_HEIGHT:
        return algorithm, False
    return algorithm, True


def check_events_while_in_main_menu(algorithm, event, all_algorithms, array_size, delay_input_box):
    click = basic_check_event(event)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            algorithm.generate_array()
        elif event.key == pygame.K_RETURN:
            algorithm.algorithm()
    elif click and SortButton(algorithm.name, 0, text=f"{algorithm.name[0:-4]} Sort").menu_mouse_click():
        return sort_menu(algorithm, all_algorithms)
    elif delay_input_box.mouse_click(click):
        delay_input_box.handle_event()
        cfg.DELAY = (int(delay_input_box.text))

    else:
        for action_button in cfg.COMMAND_BUTTONS:
            button = CommandButton(action_button)
            if button.name == "play" and button.mouse_click(click):
                algorithm.algorithm()
            elif button.name == "reload" and button.mouse_click(click):
                cfg.DELAY = 0
                algorithm.generate_array()
                cfg.DELAY = int(delay_input_box.text)
            elif button.name == "left" and button.mouse_click(click):
                algorithm = array_size.decrease(algorithm)
            elif button.name == "right" and button.mouse_click(click):
                algorithm = array_size.increase(algorithm)

    return algorithm


def sort_menu(algorithm, all_algorithms):
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(cfg.FPS)
        pygame.draw.rect(cfg.WIN, cfg.GREY, cfg.BUTTONS_MENU)
        draw_sort_menu(all_algorithms)
        for event in pygame.event.get():
            algorithm, run = check_events_while_in_sort_menu(algorithm, all_algorithms, event)
        pygame.display.update(cfg.BUTTONS_MENU)
    return algorithm


def main():
    clock = pygame.time.Clock()
    all_algorithms = get_all_algorithms(sa.Algorithm)
    algorithm = sa.SelectionSort()
    algorithm.generate_array()
    cfg.WIN.fill(cfg.WHITE)
    draw_bars(algorithm.array, algorithm.array_length)
    array_size = ArraySizeDisplay()
    delay_input_box = InputBox()
    while True:
        clock.tick(cfg.FPS)
        pygame.draw.rect(cfg.WIN, cfg.WHITE, cfg.MAIN_MENU)
        draw_main_menu(algorithm, array_size, delay_input_box)
        for event in pygame.event.get():
            algorithm = check_events_while_in_main_menu(algorithm, event, all_algorithms, array_size, delay_input_box)
        pygame.display.update()


if __name__ == '__main__':
    main()

# TODO review code cleanliness
# TODO Buttons can be optimized
