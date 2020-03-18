import enum

class GameChoice(enum.Enum):
    NINE_BY_NINE_GOBAN = 1
    THIRTEEN_BY_THIRTEEN_GOBAN = 2
    NINETEEN_BY_NINETEEN_GOBAN = 3

class Team(enum.Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

class Dimensions:
    def __init__(self):
        self.window_width = 600
        self.window_height = 480
        self.window_gap = 40
        self.case_gap = 1
        self.stone_size = 20
        self.calc()

    def calc(self):
        self.heading_height = (self.window_height - self.window_gap * 2) // 8
        self.heading_width = (self.window_width - self.window_gap * 2)

        self.board_width = self.window_width - (self.window_gap * 2)
        self.board_heigt = self.window_height - (self.window_gap * 2) - self.heading_height

    def resize(self, game_choice=None):
        if not game_choice or game_choice == GameChoice.NINE_BY_NINE_GOBAN:
            self.window_width = 600
            self.window_height = 480
            self.stone_size = 20
            self.calc()
        elif game_choice == GameChoice.THIRTEEN_BY_THIRTEEN_GOBAN:
            self.window_width = 1000
            self.window_height = 600
            self.stone_size = 17
            self.calc()
        elif game_choice == GameChoice.NINETEEN_BY_NINETEEN_GOBAN:
            self.window_width = 1200
            self.window_height = 800
            self.stone_size = 16
            self.calc()

DIMENSIONS = Dimensions()

# Color shortcuts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Colors
CASE_COLOR = (229, 186, 95)
BACKGROUND_COLOR = (101, 67, 33)
LABEL_COLOR = (255, 255, 255)
