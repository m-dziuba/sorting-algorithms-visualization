import pygame
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
BUTTON_WIDTH = VISUALIZER_WIDTH // BUTTONS_LIMIT_PER_ROW
BUTTONS_FONT_SIZE = 24
BUTTONS_BORDER_WIDTH = 2
FONT = pygame.font.Font("assets\\Ticketing.ttf", BUTTONS_FONT_SIZE)
BUTTONS_COLOUR = BLACK
SELECTION_COLOUR = GREY

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
WIN_COLOUR = WHITE
WINDOW_HEIGHT = VISUALIZER_HEIGHT + MAIN_MENU_HEIGHT
FPS = 200
WIN = pygame.display.set_mode((VISUALIZER_WIDTH, WINDOW_HEIGHT))
VISUALIZER_RECT = pygame.Rect(0, MAIN_MENU_HEIGHT, VISUALIZER_WIDTH, VISUALIZER_HEIGHT)
pygame.display.set_caption("Sorting Visualizer             Time elapsed: ---")

DELAY = 0

# ---------------- SORTING_ALGORITHMS ---------------- #
ARRAY_LENGTH = 1024
BAR_WIDTH = VISUALIZER_WIDTH // ARRAY_LENGTH
