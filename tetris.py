import pygame
import sys
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

time = 0
WIN_W = 800
WIN_H = 700
GRID_W = 300  # 300 // 30 = 10 columns
GRID_H = 600  # 600 // 30 = 20 rows
HGRID_W = 600  # 600 // 30 = 20 columns
HGRID_H = 300  # 300 // 30 = 10 rows
ROW = 20
COLUMN = 10
HROW = 10
HCOLUMN = 20
BLOCK_W = BLOCK_H = 30
GRID_X_1 = (WIN_W - GRID_W) // 2  # one player
GRID_Y_1 = WIN_H - GRID_H  # one player
GRID_X_H = (WIN_W - (2 * GRID_W)) // 2
GRID_Y_H = WIN_H - GRID_H
GRID_X_2_left = (WIN_W - 2 * GRID_W) // 2
GRID_X_2_right = GRID_X_2_left + GRID_W
GRID_Y_2_left = GRID_Y_2_right = WIN_H - GRID_H
HGRID_X = (WIN_W - HGRID_W) // 2
HGRID_Y = GRID_Y_1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (169, 169, 169)

# Figures
FIGURE_I = [
    ["P   ",
     "P   ",
     "P   ",
     "P   "],
    ["PPPP",
     "    ",
     "    ",
     "    "]
]

FIGURE_O = [
    ["PP  ",
     "PP  ",
     "    ",
     "    "]
]

FIGURE_T = [
    [" P  ",
     "PPP ",
     "    ",
     "    "],
    ["P   ",
     "PP  ",
     "P   ",
     "    "],
    ["PPP ",
     " P  ",
     "    ",
     "    "],
    [" P  ",
     "PP  ",
     " P  ",
     "    "]
]

FIGURE_S = [
    [" PP ",
     "PP  ",
     "    ",
     "    "],
    ["P   ",
     "PP  ",
     " P  ",
     "    "]
]

FIGURE_Z = [
    ["PP  ",
     " PP ",
     "    ",
     "    "],
    [" P  ",
     "PP  ",
     "P   ",
     "    "]
]

FIGURE_J = [
    ["P   ",
     "PPP ",
     "    ",
     "    "],
    ["PP  ",
     "P   ",
     "P   ",
     "    "],
    ["PPP ",
     "  P ",
     "    ",
     "    "],
    [" P  ",
     " P  ",
     "PP  ",
     "    "]
]

FIGURE_L = [
    ["  P ",
     "PPP ",
     "    ",
     "    "],
    ["P   ",
     "P   ",
     "PP  ",
     "    "],
    ["PPP ",
     "P   ",
     "    ",
     "    "],
    ["PP  ",
     " P  ",
     " P  ",
     "    "]
]

FIGURES = [FIGURE_S, FIGURE_Z, FIGURE_I, FIGURE_O, FIGURE_J, FIGURE_L, FIGURE_T]
COLORS = [GREEN, RED, LIGHT_BLUE, YELLOW, ORANGE, BLUE, PURPLE]
previous_figure = 9
previous2_figure = 9


# S = 0, Z = 1, I = 2, O = 3, J = 4, L = 5, T = 6


class Game:
    def __init__(self, mode=None):
        self.volume = 2
        self.main_menu = True
        self.choosing = True
        self.choosing_mute_assist = True
        self.intro = True
        self.play = True
        self.outro = True
        self.mode = mode
        self.assist_mode = False
        self.screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.cur_time = pygame.time.get_ticks()
        self.beg_time = pygame.time.get_ticks()
        self.fps = 60

        # intro animation figures
        self.figure_1 = Figure(random.randrange(0, WIN_W - 100), 0)
        self.figure_2 = Figure(random.randrange(0, WIN_W - 100), 0)
        self.figure_3 = Figure(random.randrange(0, WIN_W - 100), 0)

        # Backgrounds
        self.background_1 = pygame.image.load("images/tetris_bg.jpg").convert()
        self.background_1 = pygame.transform.scale(self.background_1, (WIN_W, WIN_H))
        self.background_1_rect = self.background_1.get_rect()
        self.background_2 = pygame.image.load("images/bg_2.png").convert()
        self.background_2 = pygame.transform.scale(self.background_2, (WIN_W, WIN_H))
        self.background_2_rect = self.background_2.get_rect()
        self.background_3 = pygame.image.load("images/bg_6.png").convert()
        self.background_3 = pygame.transform.scale(self.background_3, (WIN_W, WIN_H))
        self.background_3_rect = self.background_3.get_rect()
        self.background_4 = pygame.image.load("images/bg_4.jpg").convert()
        self.background_4 = pygame.transform.scale(self.background_4, (WIN_W, WIN_H))
        self.background_4_rect = self.background_4.get_rect()
        self.background_5 = pygame.image.load("images/bg_5.jpg").convert()
        self.background_5 = pygame.transform.scale(self.background_5, (WIN_W, WIN_H))
        self.background_5_rect = self.background_5.get_rect()

        # Text objects
        self.text_group = []
        self.pause = Text("Game paused; press P to resume", WHITE, 30)
        self.pause.rect.centerx = self.screen_rect.centerx
        self.pause.rect.centery = self.screen_rect.centery
        self.key = Text("How to play", WHITE, 45)
        self.key.rect.centerx = self.screen_rect.centerx
        self.key.rect.y = WIN_H // 15
        self.mute = Text("sound setting", WHITE, 45)
        self.mute.rect.centerx = self.screen_rect.centerx
        self.mute.rect.y = self.key.rect.y + 2 * self.key.rect.height
        self.mute_choice = Text("mute", WHITE, 30)
        self.mute_choice.rect.centerx = self.screen_rect.centerx // 2
        self.mute_choice.rect.y = WIN_H // 10
        self.not_mute_choice = Text("w/ sound", WHITE, 30)
        self.not_mute_choice.rect.x = self.screen_rect.centerx * 1.5
        self.not_mute_choice.rect.y = self.mute_choice.rect.y
        self.assist = Text("assist mode", WHITE, 45)
        self.assist.rect.centerx = self.screen_rect.centerx
        self.assist.rect.y = self.mute.rect.y + 2 * self.assist.rect.height
        self.assist_choice = Text("assist mode", WHITE, 45)
        self.assist_choice.rect.centerx = self.screen_rect.centerx // 2
        self.assist_choice.rect.y = self.assist.rect.y
        self.no_assist_choice = Text("regular mode", WHITE, 45)
        self.no_assist_choice.rect.centerx = self.screen_rect.centerx * 1.5
        self.no_assist_choice.rect.y = self.assist.rect.y
        self.title_2 = Text("Click here for high_level tetris", WHITE, 30)
        self.title_2.rect.centerx = self.screen_rect.centerx
        self.title_2.rect.y = self.key.rect.y - self.title_2.rect.height
        self.chose_one = Text("one-player", WHITE, 45)
        self.chose_one.rect.centerx = self.screen_rect.centerx / 2
        self.chose_one.rect.centery = self.screen_rect.centery * 1.5
        self.chose_two = Text("two-player", WHITE, 45)
        self.chose_two.rect.centerx = self.screen_rect.centerx * 1.5
        self.chose_two.rect.centery = self.screen_rect.centery * 1.5
        self.enter = Text("Press enter to begin", WHITE, 45)
        self.enter.rect.centerx = self.screen_rect.centerx
        self.enter.rect.y = WIN_H - (self.enter.rect.height * 2)
        self.back = Text("back", WHITE, 20)
        self.back.rect.x = WIN_W // 15
        self.back.rect.y = WIN_H - 2 * self.back.rect.height

        self.next_figure = Text("Next shape:", WHITE, 25)
        self.next_figure.rect.centerx = self.screen_rect.centerx * 1.5 + 50
        self.next_figure.rect.centery = self.screen_rect.centery * 0.5 + 50

        self.hold = Text("On hold:", WHITE, 20)
        self.hold.rect.x = GRID_X_1 - (BLOCK_W * 2) - self.hold.rect.width
        self.hold.rect.y = WIN_H//15

        self.reenter = Text("Press enter to play again", BLACK, 45)
        self.reenter.rect.centerx = self.screen_rect.centerx
        self.reenter.rect.y = WIN_H - (self.reenter.rect.height * 2)

        self.gameover = self.hold_left = self.hold_right = self.not_computer = self.computer = self.text = None

        # Music
        self.theme = pygame.mixer.Sound("sounds/Tetris_theme.ogg")
        self.theme.set_volume(0.1)
        self.select = pygame.mixer.Sound("sounds/select.ogg")
        self.select.set_volume(0.1)
        self.intro_music = pygame.mixer.Sound("sounds/intro.ogg")
        self.intro_music.set_volume(0.1)
        self.levelup = pygame.mixer.Sound("sounds/levelup.ogg")
        self.levelup.set_volume(0.1)

    def blink(self, text):
        self.cur_time = pygame.time.get_ticks()
        if ((self.cur_time - self.beg_time) % 1000) < 600:
            self.screen.blit(text.image, text.rect)

    def update_self(self):
        if self.mode == "one":
            self.gameover = Text("BLOCKED OUT", BLACK, 95)
            self.gameover.rect.centerx = self.screen_rect.centerx
            self.gameover.rect.centery = self.screen_rect.centery / 2

        elif self.mode == "two":
            self.hold_left = Text("On hold:", WHITE, 15)
            self.hold_left.rect.x = 0
            self.hold_left.rect.y = self.screen_rect.centery - 10
            self.hold_right = Text("On hold:", WHITE, 15)
            self.hold_right.rect.x = WIN_W - self.hold_right.rect.width
            self.hold_right.rect.centery = self.screen_rect.centery - 10
            self.computer = Text("Vs. Computer", WHITE, 25)
            self.computer.rect.centerx = self.screen_rect.centerx / 2
            self.computer.rect.y = WIN_H * 0.75
            self.not_computer = Text("Vs. Human", WHITE, 25)
            self.not_computer.rect.centerx = WIN_W * 0.75
            self.not_computer.rect.y = WIN_H * 0.75

        elif self.mode == "high_level":
            self.gameover = Text("BLOCKED OUT", BLACK, 95)
            self.gameover.rect.centerx = self.screen_rect.centerx
            self.gameover.rect.centery = self.screen_rect.centery / 2

    def begin_game(self):
        self.screen.fill(BLACK)
        pygame.display.flip()
        pygame.time.wait(500)
        self.text = Text("3", WHITE, 100)
        self.text.rect.centerx = self.screen_rect.centerx
        self.text.rect.centery = self.screen_rect.centery
        self.screen.blit(self.text.image, self.text.rect)
        pygame.display.flip()
        pygame.time.wait(500)

        self.screen.fill(BLUE)
        pygame.display.flip()
        pygame.time.wait(500)
        self.text = Text("2", WHITE, 100)
        self.text.rect.centerx = self.screen_rect.centerx
        self.text.rect.centery = self.screen_rect.centery
        self.screen.blit(self.text.image, self.text.rect)
        pygame.display.flip()
        pygame.time.wait(500)

        self.screen.fill(LIGHT_BLUE)
        pygame.display.flip()
        pygame.time.wait(500)
        self.text = Text("1", BLACK, 100)
        self.text.rect.centerx = self.screen_rect.centerx
        self.text.rect.centery = self.screen_rect.centery
        self.screen.blit(self.text.image, self.text.rect)
        pygame.display.flip()
        pygame.time.wait(500)

        self.screen.fill(WHITE)
        pygame.display.flip()
        pygame.time.wait(500)
        self.text = Text("GO!!", BLACK, 100)
        self.text.rect.centerx = self.screen_rect.centerx
        self.text.rect.centery = self.screen_rect.centery
        self.screen.blit(self.text.image, self.text.rect)
        pygame.display.flip()
        pygame.time.wait(500)


def check_click(list, pos):
    for text in list:
        if in_rect(text, pos):
            return text


def in_rect(text, pos):
    x = text.rect.x
    y = text.rect.y
    w = text.rect.width
    h = text.rect.height
    (pos_x, pos_y) = pos
    if pos_x == x or pos_x == (x + w) or ((x + w) > pos_x > x):
        if pos_y == y or pos_y == (y + h) or ((y + h) > pos_y > y):
            return True


class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Courier New", size)
        self.color = color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()


class Figure:

    def __init__(self, x, y):
        global previous_figure, previous2_figure
        self.x = x
        self.y = y
        self.rotation = 0
        seq = [0, 0, 1, 1, 2, 3, 4, 4, 5, 5, 5, 6, 6, 6]
        self.number = random.choice(seq)
        if previous2_figure == 9:
            self.number = random.choice(seq)
        else:
            while self.number == previous2_figure or self.number == previous_figure or previous_figure == previous2_figure:
                self.number = random.choice(seq)
        previous2_figure = previous_figure
        previous_figure = self.number
        self.figure = FIGURES[self.number]
        self.shape = FIGURES[self.number]
        self.image = FIGURES[self.number][self.rotation]
        self.color = COLORS[self.number]

    def rotate(self):
        self.rotation += 1
        if self.rotation > len(self.figure) - 1:
            self.rotation = 0

        self.image = self.figure[self.rotation]

    def copy(self, figure_2):
        self.x = figure_2.x
        self.y = figure_2.y
        self.rotation = figure_2.rotation
        self.number = figure_2.number
        self.figure = FIGURES[self.number]
        self.shape = FIGURES[self.number]
        self.image = FIGURES[self.number][self.rotation]
        self.color = COLORS[self.number]


class List:
    def __init__(self, tetris):
        self.master_list = []
        self.master_list.append(Figure(3, 0))
        self.master_list.append(Figure(3, 0))
        self.master_list.append(Figure(3, 0))
        self.left_list_pos = 0
        self.right_list_pos = 0
        tetris.figure_left = Figure(3, 0)
        tetris.figure_left.copy(self.master_list[self.left_list_pos])
        tetris.figure_right = Figure(3, 0)
        tetris.figure_right.copy(self.master_list[self.right_list_pos])
        tetris.next_figure_left = Figure(3, 0)
        tetris.next_figure_left.copy(self.master_list[self.left_list_pos + 1])
        tetris.next_figure_right = Figure(3, 0)
        tetris.next_figure_right.copy(self.master_list[self.right_list_pos + 1])
        self.master_list.append(Figure(3, 0))

    def next_figure(self, tetris, side):
        if side == "left":
            self.left_list_pos += 1
            tetris.figure_left = Figure(3, 0)
            tetris.figure_left.copy(self.master_list[self.left_list_pos])
            tetris.next_figure_left = Figure(3, 0)
            tetris.next_figure_left.copy(self.master_list[self.left_list_pos + 1])
            self.master_list.append(Figure(3, 0))
        elif side == "right":
            self.right_list_pos += 1
            tetris.figure_right = Figure(3, 0)
            tetris.figure_right.copy(self.master_list[self.right_list_pos])
            tetris.next_figure_right = Figure(3, 0)
            tetris.next_figure_right.copy(self.master_list[self.right_list_pos + 1])

    def hold(self, tetris, side):
        if side == "left":
            if tetris.hold_left is None:
                self.left_list_pos += 1
                tetris.hold_left = tetris.figure_left
                tetris.figure_left = tetris.next_figure_left
                tetris.next_figure_left = Figure(3, 0)
                tetris.next_figure_left.copy(self.master_list[self.left_list_pos + 1])
                self.master_list.append(Figure(3, 0))
            else:
                figure_rn = tetris.figure_left
                figure_held = tetris.hold_left
                tetris.figure_left = figure_held
                tetris.hold_left = figure_rn
                tetris.figure_left.x = 3
                tetris.figure_left.y = 0
                tetris.figure_left.rotation = 0
        elif side == "right":
            if tetris.hold_right is None:
                self.right_list_pos += 1
                tetris.hold_right = tetris.figure_right
                tetris.figure_right = tetris.next_figure_right
                tetris.next_figure_right = Figure(3, 0)
                tetris.next_figure_right.copy(self.master_list[self.right_list_pos + 1])
                self.master_list.append(Figure(3, 0))
            else:
                figure_rn = tetris.figure_right
                figure_held = tetris.hold_right
                tetris.figure_right = figure_held
                tetris.hold_right = figure_rn
                tetris.figure_right.x = 3
                tetris.figure_right.y = 0
                tetris.figure_right.rotation = 0

    def update_list(self):
        if self.right_list_pos + 3 > len(self.master_list):
            self.master_list.append(Figure(3, 0))
        if self.left_list_pos + 3 > len(self.master_list):
            self.master_list.append(Figure(3, 0))


class Tetris:
    def __init__(self, mode):
        self.level = 1
        self.speed = 40
        self.mode = mode
        self.computer = False
        self.state = "intro"
        if self.mode == "two":
            self.winner = None
            self.score_left = 0
            self.score_right = 0
            self.used_hold_left = False
            self.used_hold_right = False
            self.used_left = 0
            self.used_right = 0
            self.grid_left = []
            self.grid_right = []
            self.figure_left = None
            self.figure_right = None
            self.next_figure_left = None
            self.next_figure_right = None
            self.figures_list = List(self)
            self.action_list = ["start"]
            self.hold_left = None
            self.hold_right = None

            self.height = GRID_H // BLOCK_H
            self.width = GRID_W // BLOCK_W

            for i in range(self.height):
                new_line = []
                for j in range(self.width):
                    new_line.append(9)
                self.grid_left.append(new_line)

            for i in range(self.height):
                new_line = []
                for j in range(self.width):
                    new_line.append(9)
                self.grid_right.append(new_line)
        elif self.mode == "one":
            self.grid = []
            self.score = 0
            self.score_previous = 0
            self.used_hold = False
            self.figure = Figure(3, 0)
            self.next_figure = Figure(3, 0)
            self.hold = None
            self.height = GRID_H // BLOCK_H
            self.width = GRID_W // BLOCK_W
            for i in range(self.height):
                new_line = []
                for j in range(self.width):
                    new_line.append(9)
                self.grid.append(new_line)
        elif self.mode == "high":
            self.grid = []
            self.score = 0
            self.score_previous = 0
            self.figure = Figure(6, 0)
            self.next_figure = Figure(6, 0)
            for i in range(HROW):
                new_line = []
                for j in range(HCOLUMN):
                    new_line.append(9)
                self.grid.append(new_line)

    def new_figure(self, side=None):
        if self.mode == "one":
            self.figure = self.next_figure
            self.next_figure = Figure(3, 0)
            self.used_hold = False
            if self.check_intersection():
                self.state = "lost"

        elif self.mode == "high":
            self.figure = self.next_figure
            self.next_figure = Figure(6, 0)
            if self.check_intersection():
                self.state = "lost"

        elif self.mode == "two":
            if side == "left":
                self.figures_list.next_figure(self, "left")
                if self.check_intersection("left"):
                    self.winner = "right"
                    self.state = "lost"
                self.action_list = ["start"]
                self.used_hold_left = False
            elif side == "right":
                self.figures_list.next_figure(self, "right")
                if self.check_intersection("right"):
                    self.winner = "left"
                    self.state = "lost"
                self.used_hold_right = False

    def shape_pos(self, side=None):
        if self.mode == "one" or self.mode == "high":
            positions = []
            shape = self.figure.image

            for i, line in enumerate(shape):
                row = list(line)
                for j, column in enumerate(row):
                    if column == "P":
                        positions.append((self.figure.x + j, self.figure.y + i))

            return positions

        elif self.mode == "two":
            if side == "left":
                positions = []
                shape = self.figure_left.image

                for i, line in enumerate(shape):
                    row = list(line)
                    for j, column in enumerate(row):
                        if column == "P":
                            positions.append((self.figure_left.x + j, self.figure_left.y + i))
                return positions

            elif side == "right":
                positions = []
                shape = self.figure_right.image

                for i, line in enumerate(shape):
                    row = list(line)
                    for j, column in enumerate(row):
                        if column == "P":
                            positions.append((self.figure_right.x + j, self.figure_right.y + i))
                return positions

    def check_intersection(self, side=None):
        if self.mode == "one":
            open_pos = []
            for i in range(COLUMN):
                for j in range(ROW):
                    if self.grid[j][i] == 9:
                        open_pos.append((i, j))
            shape_pos = self.shape_pos()
            for pos in shape_pos:
                if pos not in open_pos:
                    return True
            return False
        elif self.mode == "high":
            open_pos = []
            for i in range(HCOLUMN):
                for j in range(HROW):
                    if self.grid[j][i] == 9:
                        open_pos.append((i, j))
            shape_pos = self.shape_pos()
            for pos in shape_pos:
                if pos not in open_pos:
                    return True
            return False
        elif self.mode == "two":
            if side == "left":
                open_pos = []
                for i in range(COLUMN):
                    for j in range(ROW):
                        if self.grid_left[j][i] == 9:
                            open_pos.append((i, j))
                shape_pos = self.shape_pos("left")
                for pos in shape_pos:
                    if pos not in open_pos:
                        return True
                return False
            elif side == "right":
                open_pos = []
                for i in range(COLUMN):
                    for j in range(ROW):
                        if self.grid_right[j][i] == 9:
                            open_pos.append((i, j))
                shape_pos = self.shape_pos("right")
                for pos in shape_pos:
                    if pos not in open_pos:
                        return True
                return False

    def freeze(self, side=None):
        if self.mode == "one" or self.mode == "high":
            shape_pos = self.shape_pos()
            num = self.figure.number
            for pos in shape_pos:
                x, y = pos
                self.grid[y][x] = num

            self.break_lines()

            self.new_figure()

        elif self.mode == "two":
            if side == "left":
                shape_pos = self.shape_pos("left")
                num = self.figure_left.number
                for pos in shape_pos:
                    x, y = pos
                    self.grid_left[y][x] = num

                self.break_lines("left")
                self.new_figure("left")

            elif side == "right":
                shape_pos = self.shape_pos("right")
                num = self.figure_right.number
                for pos in shape_pos:
                    x, y = pos
                    self.grid_right[y][x] = num

                self.break_lines("right")
                self.new_figure("right")

    def break_lines(self, side=None):
        if self.mode == "one":
            lines = 0
            for t in range(4):
                for i in range(len(self.grid) - 1, -1, -1):
                    row = self.grid[i]
                    if 9 not in row:
                        new_line = []
                        lines += 1
                        del self.grid[i]
                        for j in range(COLUMN):
                            new_line.append(9)
                        self.grid.insert(0, new_line)
            if lines == 1:
                self.score += 40
            elif lines == 2:
                self.score += 100
            elif lines == 3:
                self.score += 300
            elif lines == 4:
                self.score += 1200

        elif self.mode == "high":
            lines = 0
            for t in range(4):
                new_line = []
                for i in range(len(self.grid) - 1, -1, -1):
                    row = self.grid[i]
                    if 9 not in row:
                        lines += 1
                        del self.grid[i]
                        for j in range(HCOLUMN):
                            new_line.append(9)
                        self.grid.insert(0, new_line)
                        new_line = []
            if lines == 1:
                self.score += 40
            elif lines == 2:
                self.score += 200
            elif lines == 3:
                self.score += 600
            elif lines == 4:
                self.score += 2400

        elif self.mode == "two":
            if side == "left":
                lines = 0
                for t in range(4):
                    new_line = []
                    for i in range(len(self.grid_left) - 1, -1, -1):
                        row = self.grid_left[i]
                        if 9 not in row and 8 not in row:
                            lines += 1
                            del self.grid_left[i]
                            for j in range(COLUMN):
                                new_line.append(9)
                            self.grid_left.insert(0, new_line)
                            new_line = []
                if lines == 1:
                    self.score_left += 40
                elif lines == 2:
                    self.score_left += 100
                elif lines == 3:
                    self.score_left += 300
                elif lines == 4:
                    self.score_left += 1200
                for i in range(lines):
                    self.attack("left")
            elif side == "right":
                lines = 0
                for t in range(4):
                    new_line = []
                    for i in range(len(self.grid_right) - 1, -1, -1):
                        row = self.grid_right[i]
                        if 9 not in row and 8 not in row:
                            lines += 1
                            del self.grid_right[i]
                            for j in range(COLUMN):
                                new_line.append(9)
                            self.grid_right.insert(0, new_line)
                            new_line = []
                if lines == 1:
                    self.score_right += 40
                elif lines == 2:
                    self.score_right += 100
                elif lines == 3:
                    self.score_right += 300
                elif lines == 4:
                    self.score_right += 1200
                for i in range(lines):
                    self.attack("right")

    def update_high(self, run):
        global time
        key = pygame.key.get_pressed()
        if time % 5 == 0:
            if key[pygame.K_SPACE]:
                self.move_space()
                self.score += 10
            elif key[pygame.K_DOWN]:
                self.move_down()
            elif key[pygame.K_RIGHT]:
                self.move_side(1)
            elif key[pygame.K_LEFT]:
                self.move_side(-1)
            elif key[pygame.K_UP]:
                self.rotate()
        self.speed_control(run)

    def update_one(self, run):
        global time
        key = pygame.key.get_pressed()
        if time % 5 == 0:
            if key[pygame.K_SPACE]:
                self.move_space()
                self.score += 1
            elif key[pygame.K_DOWN]:
                self.move_down()
            elif key[pygame.K_RIGHT]:
                self.move_side(1)
            elif key[pygame.K_LEFT]:
                self.move_side(-1)
            elif key[pygame.K_UP]:
                self.rotate()
            elif key[pygame.K_h]:
                self.holding()
        self.speed_control(run)

    def speed_control(self, run):
        while self.score - self.score_previous > 100 and run.assist_mode is not True:
            self.speed -= 1
            if self.speed == 0:
                self.speed = 2
            self.score_previous += 100
            self.level += 1
            run.levelup.play()
        if self.score - self.score_previous < 0:
            self.score_previous = self.score

    def update_two(self, run):
        global time
        self.figures_list.update_list()
        key = pygame.key.get_pressed()
        if time % 5 == 0:
            if key[pygame.K_SPACE]:
                self.move_space("right")
                self.score_right += 1
            elif key[pygame.K_DOWN]:
                self.move_down("right")
            elif key[pygame.K_RIGHT]:
                self.move_side(1, "right")
            elif key[pygame.K_LEFT]:
                self.move_side(-1, "right")
            elif key[pygame.K_UP]:
                self.rotate("right")
            elif key[pygame.K_h]:
                self.holding("right")
            if not self.computer:
                if key[pygame.K_f]:
                    self.move_space("left")
                    self.score_left += 1
                elif key[pygame.K_s]:
                    self.move_down("left")
                elif key[pygame.K_a]:
                    self.move_side(-1, "left")
                elif key[pygame.K_d]:
                    self.move_side(1, "left")
                elif key[pygame.K_w]:
                    self.rotate("left")
                elif key[pygame.K_q]:
                    self.holding("left")

            elif key[pygame.K_g]:
                self.switch()
            elif key[pygame.K_y]:
                self.clear()

        if self.computer:
            self.intelligent(time)

        if self.score_left or self.score_right > 100:
            self.speed = 40
        elif self.score_left or self.score_right > 200:
            self.speed = 30
        elif self.score_left or self.score_right > 500:
            if self.score_left > 500:
                self.winner = "left"
            elif self.score_right > 500:
                self.winner = "right"
            run.play = False

    def intelligent(self, time_rec):
        if self.action_list == ["start"]:
            record_x = []
            record_y = []
            record_down = []
            x = self.figure_left.x
            y = self.figure_left.y
            for i in range(COLUMN):
                self.figure_left.x = i
                self.figure_left.y = y
                go_down = 0
                while not self.check_intersection("left"):
                    self.figure_left.y += 1
                    go_down += 1
                self.figure_left.y -= 1
                go_down -= 1
                record_x.append(i)
                record_y.append(self.figure_left.y)
                record_down.append(go_down)
            ideal_y = max(record_y)
            ideal_x = record_x[record_y.index(ideal_y)]
            ideal_down = record_down[record_y.index(ideal_y)]
            if x - ideal_x != 0:
                if x - ideal_x < 0:
                    difference = -(x - ideal_x)
                else:
                    difference = x - ideal_x
                for i in range(difference):
                    if x - ideal_x < 0:
                        self.action_list.append("move_right")
                    else:
                        self.action_list.append("move_left")
                for j in range(ideal_down):
                    self.action_list.append("move_down")
                self.action_list.append("end")
                self.figure_left.x = x
                self.figure_left.y = y
            elif x - ideal_x == 0:
                for j in range(ideal_down):
                    self.action_list.append("move_down")
                self.action_list.append("end")
                self.figure_left.x = x
                self.figure_left.y = y

        else:
            if time_rec % 30 == 0:
                try:
                    movement = self.action_list[0]
                    if movement != "end":
                        if movement == "move_left":
                            self.move_side(-1, "left")
                        elif movement == "move_right":
                            self.move_side(1, "left")
                        elif movement == "move_down":
                            self.move_down("left")
                        del self.action_list[0]
                    else:
                        self.action_list = ["start"]
                        self.move_space("left")
                        self.new_figure("left")
                except IndexError:
                    self.action_list = ["start"]

    def clear(self):
        if self.used_left <= 3 and self.used_right <= 3:
            self.grid_left = []
            for i in range(self.height):
                new_line = []
                for j in range(self.width):
                    new_line.append(9)
                self.grid_left.append(new_line)
            self.grid_right = []
            for i in range(self.height):
                new_line = []
                for j in range(self.width):
                    new_line.append(9)
                self.grid_right.append(new_line)

    def attack(self, side):
        global time
        if side == "left":
            del self.grid_right[0]
            new_line = []
            for j in range(10):
                new_line.append(8)
            self.grid_right.append(new_line)
            if self.computer:
                self.action_list = ["start"]
                self.intelligent(time)
        elif side == "right":
            del self.grid_left[0]
            new_line = []
            for j in range(10):
                new_line.append(8)
            self.grid_left.append(new_line)

    def switch(self):
        if self.used_left <= 3 and self.used_right <= 3:
            wait = self.figure_left
            wait_2 = self.figure_right
            self.figure_left = wait_2
            self.figure_right = wait
            self.figure_left.x = 3
            self.figure_left.y = 0
            self.figure_right.x = 3
            self.figure_right.y = 0
            self.used_left += 1
            self.used_right += 1

    def holding(self, side=None):

        if self.mode == "one" and not self.used_hold:
            if self.hold is None:
                self.hold = self.figure
                self.figure = self.next_figure
                self.next_figure = Figure(3, 0)
            else:
                wait = self.hold
                wait_2 = self.figure
                self.figure = wait
                self.hold = wait_2
                self.figure.x = 3
                self.figure.y = 0
                self.figure.rotation = 0
            self.used_hold = True
        elif self.mode == "two":
            if side == "left" and not self.used_hold_left:
                self.figures_list.hold(self, "left")
                self.used_hold_left = True
            elif side == "right" and not self.used_hold_right:
                self.figures_list.hold(self, "right")
                self.used_hold_right = True

    def move_space(self, side=None):
        if self.mode == "one" or self.mode == "high":
            while not self.check_intersection():
                self.figure.y += 1
            self.figure.y -= 1
            self.freeze()
        elif self.mode == "two":
            if side == "left":
                while not self.check_intersection("left"):
                    self.figure_left.y += 1
                self.figure_left.y -= 1
                self.freeze("left")
            elif side == "right":
                while not self.check_intersection("right"):
                    self.figure_right.y += 1
                self.figure_right.y -= 1
                self.freeze("right")

    def move_down(self, side=None):
        if self.mode == "one" or self.mode == "high":
            self.figure.y += 1
            if self.check_intersection():
                self.figure.y -= 1
                self.freeze()
        elif self.mode == "two":
            if side == "left":
                self.figure_left.y += 1
                if self.check_intersection("left"):
                    self.figure_left.y -= 1
                    self.freeze("left")
            elif side == "right":
                self.figure_right.y += 1
                if self.check_intersection("right"):
                    self.figure_right.y -= 1
                    self.freeze("right")

    def move_side(self, x, side=None):
        if self.mode == "one" or self.mode == "high":
            old_x = self.figure.x
            self.figure.x += x
            if self.check_intersection():
                self.figure.x = old_x
        elif self.mode == "two":
            if side == "left":
                old_x = self.figure_left.x
                self.figure_left.x += x
                if self.check_intersection("left"):
                    self.figure_left.x = old_x
            elif side == "right":
                old_x = self.figure_right.x
                self.figure_right.x += x
                if self.check_intersection("right"):
                    self.figure_right.x = old_x

    def rotate(self, side=None):
        if self.mode == "one" or self.mode == "high":
            old_rotation = self.figure.rotation
            self.figure.rotate()
            if self.check_intersection():
                self.figure.rotation = old_rotation
        elif self.mode == "two":
            if side == "left":
                old_rotation = self.figure_left.rotation
                self.figure_left.rotate()
                if self.check_intersection("left"):
                    self.figure_left.rotation = old_rotation
            elif side == "right":
                old_rotation = self.figure_right.rotation
                self.figure_right.rotate()
                if self.check_intersection("right"):
                    self.figure_right.rotation = old_rotation

    def draw_one(self, run):
        for i in range(ROW):
            # Horizontal lines
            pygame.draw.line(run.screen, WHITE, (GRID_X_1, GRID_Y_1 + i * BLOCK_H),
                             (GRID_X_1 + GRID_W, GRID_Y_1 + i * BLOCK_H))
            for j in range(COLUMN):
                # Vertical lines
                pygame.draw.line(run.screen, WHITE, (GRID_X_1 + j * BLOCK_W, GRID_Y_1),
                                 (GRID_X_1 + j * BLOCK_W, GRID_Y_1 + GRID_H))

        run.screen.blit(run.next_figure.image, run.next_figure.rect)
        color = self.next_figure.color
        sx = GRID_X_1 + GRID_W + 50
        sy = GRID_Y_1 + GRID_H // 2 - 100
        s = 0
        q = 0
        for i in self.next_figure.image:
            for j in i:
                if j == "P":
                    x = sx + q * BLOCK_W
                    y = sy + s * BLOCK_H
                    pygame.draw.rect(run.screen, color, (x, y, BLOCK_W, BLOCK_H), 0)
                q += 1
            q = 0
            s += 1

        if self.hold is not None:
            run.screen.blit(run.hold.image, run.hold.rect)
            color = self.hold.color
            sx, sy = GRID_X_1 - (2 * BLOCK_W), GRID_Y_1
            s = 0
            q = 0
            for i in self.hold.image:
                for j in i:
                    if j == "P":
                        x = sx + q * (BLOCK_W//2)
                        y = sy + s * (BLOCK_H//2)
                        pygame.draw.rect(run.screen, color, (x, y, BLOCK_W//2, BLOCK_H//2), 0)
                    q += 1
                q = 0
                s += 1

        s = 0
        q = 0
        color = self.figure.color
        for i in self.figure.image:
            for j in i:
                if j == "P":
                    x = GRID_X_1 + (s + self.figure.x) * BLOCK_W
                    y = GRID_Y_1 + (q + self.figure.y) * BLOCK_H
                    pygame.draw.rect(run.screen, color, (x, y, BLOCK_W, BLOCK_H), 0)

                s += 1
            s = 0
            q += 1

        if run.assist_mode:
            s = 0
            q = 0
            x = self.figure.x
            y = self.figure.y
            while not self.check_intersection():
                self.figure.y += 1
            self.figure.y -= 1
            for i in self.figure.image:
                for j in i:
                    if j == "P":
                        xp = GRID_X_1 + (s + self.figure.x) * BLOCK_W
                        yp = GRID_Y_1 + (q + self.figure.y) * BLOCK_H
                        pygame.draw.rect(run.screen, color, (xp, yp, BLOCK_W, BLOCK_H), 2)
                    s += 1
                s = 0
                q += 1
            self.figure.x = x
            self.figure.y = y

    def draw_left(self, run):
        for i in range(ROW):
            # Horizontal lines
            pygame.draw.line(run.screen, WHITE, (GRID_X_2_left, GRID_Y_2_left + i * BLOCK_H),
                             (GRID_X_2_left + GRID_W, GRID_Y_2_left + i * BLOCK_H))
            for j in range(COLUMN):
                # Vertical lines
                pygame.draw.line(run.screen, WHITE, (GRID_X_2_left + j * BLOCK_W, GRID_Y_2_left),
                                 (GRID_X_2_left + j * BLOCK_W, GRID_Y_2_left + GRID_H))

        run.next_figure.rect.x = 10
        run.next_figure.rect.y = 10
        run.screen.blit(run.next_figure.image, run.next_figure.rect)
        color = self.next_figure_left.color
        sx = GRID_X_2_left // 2 - 50
        sy = GRID_Y_2_left // 2
        s = 0
        q = 0
        for i in self.next_figure_left.image:
            for j in i:
                if j == "P":
                    x = sx + q * BLOCK_W
                    y = sy + s * BLOCK_H
                    pygame.draw.rect(run.screen, color, (x, y, BLOCK_W, BLOCK_H), 0)
                q += 1
            q = 0
            s += 1

        if self.hold_left is not None:
            run.screen.blit(run.hold_left.image, run.hold_left.rect)
            color = self.hold_left.color
            sx = GRID_X_2_left // 2
            sy = WIN_H // 2 + 50
            s = 0
            q = 0
            for i in self.hold_left.image:
                for j in i:
                    if j == "P":
                        x = sx + q * BLOCK_W // 2
                        y = sy + s * BLOCK_H // 2
                        pygame.draw.rect(run.screen, color, (x, y, BLOCK_W // 2, BLOCK_H // 2), 0)
                    q += 1
                q = 0
                s += 1

        s = 0
        q = 0
        color = self.figure_left.color
        for i in self.figure_left.image:
            for j in i:
                if j == "P":
                    x = GRID_X_2_left + (s + self.figure_left.x) * BLOCK_W
                    y = GRID_Y_2_left + (q + self.figure_left.y) * BLOCK_H
                    pygame.draw.rect(run.screen, color, (x, y, BLOCK_W, BLOCK_H), 0)

                s += 1
            s = 0
            q += 1

        if run.assist_mode:
            s = 0
            q = 0
            x = self.figure_left.x
            y = self.figure_left.y
            while not self.check_intersection("left"):
                self.figure_left.y += 1
            self.figure_left.y -= 1
            for i in self.figure_left.image:
                for j in i:
                    if j == "P":
                        xp = GRID_X_2_left + (s + self.figure_left.x) * BLOCK_W
                        yp = GRID_Y_2_right + (q + self.figure_left.y) * BLOCK_H
                        pygame.draw.rect(run.screen, color, (xp, yp, BLOCK_W, BLOCK_H), 2)
                    s += 1
                s = 0
                q += 1
            self.figure_left.x = x
            self.figure_left.y = y

    def draw_right(self, run):
        for i in range(ROW):
            # Horizontal lines
            pygame.draw.line(run.screen, WHITE, (GRID_X_2_right, GRID_Y_2_right + i * BLOCK_H),
                             (GRID_X_2_right + GRID_W, GRID_Y_2_right + i * BLOCK_H))
            for j in range(COLUMN):
                # Vertical lines
                pygame.draw.line(run.screen, WHITE, (GRID_X_2_right + j * BLOCK_W, GRID_Y_2_right),
                                 (GRID_X_2_right + j * BLOCK_W, GRID_Y_2_right + GRID_H))

        run.next_figure.rect.x = WIN_W - run.next_figure.rect.width - 10
        run.next_figure.rect.y = 10
        run.screen.blit(run.next_figure.image, run.next_figure.rect)
        color = self.next_figure_right.color
        sx = GRID_X_2_right + GRID_W + 5
        sy = run.next_figure.rect.y + 2 * run.next_figure.rect.height
        s = 0
        q = 0
        for i in self.next_figure_right.image:
            for j in i:
                if j == "P":
                    x = sx + q * BLOCK_W
                    y = sy + s * BLOCK_H
                    pygame.draw.rect(run.screen, color, (x, y, BLOCK_W, BLOCK_H), 0)
                q += 1
            q = 0
            s += 1

        if self.hold_right is not None:
            run.screen.blit(run.hold_right.image, run.hold_right.rect)
            color = self.hold_right.color
            sx = GRID_X_2_right + GRID_W + 10
            sy = WIN_H // 2 + 10
            s = 0
            q = 0
            for i in self.hold_right.image:
                for j in i:
                    if j == "P":
                        x = sx + q * BLOCK_W // 2
                        y = sy + s * BLOCK_H // 2
                        pygame.draw.rect(run.screen, color, (x, y, BLOCK_W // 2, BLOCK_H // 2), 0)
                    q += 1
                q = 0
                s += 1

        s = 0
        q = 0
        color = self.figure_right.color
        for i in self.figure_right.image:
            for j in i:
                if j == "P":
                    x = GRID_X_2_right + (s + self.figure_right.x) * BLOCK_W
                    y = GRID_Y_2_right + (q + self.figure_right.y) * BLOCK_H
                    pygame.draw.rect(run.screen, color, (x, y, BLOCK_W, BLOCK_H), 0)

                s += 1
            s = 0
            q += 1

        if run.assist_mode:
            s = 0
            q = 0
            x = self.figure_right.x
            y = self.figure_right.y
            while not self.check_intersection("right"):
                self.figure_right.y += 1
            self.figure_right.y -= 1
            for i in self.figure_right.image:
                for j in i:
                    if j == "P":
                        xp = GRID_X_2_right + (s + self.figure_right.x) * BLOCK_W
                        yp = GRID_Y_2_right + (q + self.figure_right.y) * BLOCK_H
                        pygame.draw.rect(run.screen, color, (xp, yp, BLOCK_W, BLOCK_H), 2)
                    s += 1
                s = 0
                q += 1
            self.figure_right.x = x
            self.figure_right.y = y

    def draw_high(self, run):
        for i in range(HROW):
            # Horizontal lines
            pygame.draw.line(run.screen, WHITE, (HGRID_X, HGRID_Y + i * BLOCK_H),
                             (HGRID_X + HGRID_W, HGRID_Y + i * BLOCK_H))
            for j in range(HCOLUMN):
                # Vertical lines
                pygame.draw.line(run.screen, WHITE, (HGRID_X + j * BLOCK_W, HGRID_Y),
                                 (HGRID_X + j * BLOCK_W, HGRID_Y + HGRID_H))

        s = 0
        q = 0
        color = self.figure.color
        for i in self.figure.image:
            for j in i:
                if j == "P":
                    x = HGRID_X + (s + self.figure.x) * BLOCK_W
                    y = HGRID_Y + (q + self.figure.y) * BLOCK_H
                    pygame.draw.rect(run.screen, color, (x, y, BLOCK_W, BLOCK_H), 0)

                s += 1
            s = 0
            q += 1


def high_level_mode(run):
    global time
    time = 0
    tetris = Tetris("high")
    run.intro_music.play(-1)

    info = True
    info1 = Text("In this high-level game,", BLACK, 30)
    info2 = Text("you cannot use", BLACK, 30)
    info3 = Text("assist mode, hold,", BLACK, 30)
    info4 = Text("or view the next figure.", BLACK, 30)
    run.text_group = [info1, info2, info3, info4]
    pre_y = 20
    for text in run.text_group:
        text.rect.centerx = run.screen_rect.centerx
        text.rect.y = pre_y + text.rect.height
        pre_y = text.rect.y

    while info:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.intro_music.stop()
                run.select.play(0)
                run.screen.blit(run.enter.image, run.enter.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                info = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                text = check_click([run.enter], click)
                if text == run.enter:
                    run.intro_music.stop()
                    run.select.play(0)
                    run.screen.blit(run.enter.image, run.enter.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    info = False

        run.screen.blit(run.background_4, run.background_4_rect)
        for text in run.text_group:
            run.screen.blit(text.image, text.rect)
        run.blink(run.enter)
        run.clock.tick(run.fps)
        pygame.display.flip()

    run.begin_game()
    run.theme.play(-1)
    while run.play:
        while tetris.figure is None:
            tetris.new_figure()
        if tetris.state == "lost":
            run.play = False

        if time % tetris.speed == 0:
            tetris.move_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_p] != 0:
                resume = False
                while not resume:
                    for _ in pygame.event.get():
                        if pygame.key.get_pressed()[pygame.K_p] != 0:
                            resume = True
                    run.screen.fill(BLACK)
                    run.blink(run.pause)
                    pygame.display.flip()

        # Update
        tetris.update_high(run)
        tetris.draw_high(run)
        time += 1
        # Draw everything
        run.screen.fill(BLACK)

        for i in range(len(tetris.grid)):
            for j in range(len(tetris.grid[i])):
                num = tetris.grid[i][j]
                if num != 9:
                    color = COLORS[num]
                else:
                    color = BLACK
                pygame.draw.rect(run.screen, color, (HGRID_X + j * 30, HGRID_Y + i * 30, BLOCK_W, BLOCK_H), 0)

        tetris.draw_high(run)

        pygame.draw.rect(run.screen, WHITE, (HGRID_X, HGRID_Y, HGRID_W, HGRID_H), 2)
        score = Text(str(tetris.score), WHITE, 30)
        score.rect.centerx = run.screen_rect.centerx
        score.rect.centery = 10
        run.screen.blit(score.image, score.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()

    num = 0
    while num < tetris.score:
        run.screen.blit(run.background_5, run.background_5_rect)
        final_score = Text("Your final score: " + str(num), BLACK, 40)
        final_score.rect.centerx = run.screen_rect.centerx
        final_score.rect.y = run.gameover.rect.y + run.gameover.rect.height
        run.screen.blit(final_score.image, final_score.rect)
        pygame.display.flip()
        pygame.time.wait(5)
        num += 5
        if num == tetris.score:
            break
    while run.outro:
        if tetris.state == "lost":
            run.screen.blit(run.background_5, run.background_5_rect)
            run.blink(run.reenter)
            run.screen.blit(run.gameover.image, run.gameover.rect)
            final_score = Text("Your final score: " + str(tetris.score), BLACK, 40)
            final_score.rect.centerx = run.screen_rect.centerx
            final_score.rect.y = run.gameover.rect.y + run.gameover.rect.height
            final_level = Text("Your final level: " + str(tetris.level), BLACK, 40)
            final_level.rect.centerx = run.screen_rect.centerx
            final_level.rect.y = final_score.rect.y + final_level.rect.height
            run.screen.blit(final_score.image, final_score.rect)
            run.screen.blit(final_level.image, final_level.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.select.play(0)
                run.screen.blit(run.background_5, run.background_5_rect)
                run.screen.blit(run.reenter.image, run.reenter.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                run.outro = False
                tetris.state = "playing"
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                text = check_click([run.reenter], click)
                if text == run.reenter:
                    run.select.play(0)
                    run.screen.blit(run.background_5, run.background_5_rect)
                    run.screen.blit(run.reenter.image, run.reenter.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.outro = False
                    tetris.state = "playing"
                    main()

        run.clock.tick(run.fps)
        pygame.display.flip()


def one_player(run):
    global time
    time = 0
    tetris = Tetris("one")
    run.intro_music.play(-1)
    while run.intro:
        if tetris.state != "intro":
            run.intro = False

        # Checks if window exit button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.intro_music.stop()
                run.select.play(0)
                run.screen.blit(run.background_4, run.background_4_rect)
                run.screen.blit(run.enter.image, run.enter.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                tetris.state = "playing"
                run.intro = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                text = check_click([run.enter, run.back], click)
                if text == run.enter:
                    run.intro_music.stop()
                    run.select.play(0)
                    run.screen.blit(run.background_4, run.background_4_rect)
                    run.screen.blit(run.enter.image, run.enter.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    tetris.state = "playing"
                    run.intro = False
                elif text == run.back:
                    run.intro_music.stop()
                    run.select.play(0)
                    run.screen.blit(run.background_4, run.background_4_rect)
                    run.screen.blit(run.back.image, run.back.rect)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    main()

        run.screen.blit(run.background_4, run.background_4_rect)
        run.screen.blit(run.back.image, run.back.rect)
        run.blink(run.enter)

        run.clock.tick(run.fps)
        pygame.display.flip()

    run.begin_game()
    run.theme.play(-1)
    while run.play:
        if tetris.state != "playing":
            run.theme.stop()
            run.play = False
        while tetris.figure is None:
            tetris.new_figure()

        if time % tetris.speed == 0:
            tetris.move_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_p] != 0:
                resume = False
                while not resume:
                    for _ in pygame.event.get():
                        if pygame.key.get_pressed()[pygame.K_p] != 0:
                            resume = True
                    run.screen.fill(BLACK)
                    run.blink(run.pause)
                    pygame.display.flip()

        # Update
        tetris.update_one(run)
        time += 1
        # Draw everything
        run.screen.fill(BLACK)

        for i in range(len(tetris.grid)):
            for j in range(len(tetris.grid[i])):
                num = tetris.grid[i][j]
                if num != 9:
                    color = COLORS[num]
                else:
                    color = BLACK
                pygame.draw.rect(run.screen, color, (GRID_X_1 + j * 30, GRID_Y_1 + i * 30, BLOCK_W, BLOCK_H), 0)

        tetris.draw_one(run)

        pygame.draw.rect(run.screen, WHITE, (GRID_X_1, GRID_Y_1, GRID_W, GRID_H), 5)
        pygame.draw.rect(run.screen, WHITE, (GRID_X_1 - (2 * BLOCK_W), GRID_Y_1, 2 * BLOCK_W, 2 * BLOCK_H), 2)
        score = Text(str(tetris.score), WHITE, 30)
        score.rect.centerx = run.screen_rect.centerx
        score.rect.centery = 5
        run.screen.blit(score.image, score.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()

    num = 0
    while num < tetris.score:
        run.screen.blit(run.background_5, run.background_5_rect)
        final_score = Text("Your final score: " + str(num), BLACK, 40)
        final_score.rect.centerx = run.screen_rect.centerx
        final_score.rect.y = run.gameover.rect.y + run.gameover.rect.height
        run.screen.blit(final_score.image, final_score.rect)
        pygame.display.flip()
        pygame.time.wait(5)
        num += 5
        if num == tetris.score:
            break

    while run.outro:
        if tetris.state == "lost":
            run.screen.blit(run.background_5, run.background_5_rect)
            run.blink(run.reenter)
            run.screen.blit(run.gameover.image, run.gameover.rect)
            final_score = Text("Your final score: " + str(tetris.score), BLACK, 40)
            final_score.rect.centerx = run.screen_rect.centerx
            final_score.rect.y = run.gameover.rect.y + run.gameover.rect.height
            final_level = Text("Your final level: " + str(tetris.level), BLACK, 40)
            final_level.rect.centerx = run.screen_rect.centerx
            final_level.rect.y = final_score.rect.y + final_level.rect.height
            run.screen.blit(final_score.image, final_score.rect)
            run.screen.blit(final_level.image, final_level.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.select.play(0)
                run.screen.blit(run.background_5, run.background_5_rect)
                run.screen.blit(run.reenter.image, run.reenter.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                run.outro = False
                tetris.state = "playing"
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                text = check_click([run.reenter], click)
                if text == run.reenter:
                    run.select.play(0)
                    run.screen.blit(run.background_5, run.background_5_rect)
                    run.screen.blit(run.reenter.image, run.reenter.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.outro = False
                    tetris.state = "playing"
                    main()

        run.clock.tick(run.fps)
        pygame.display.flip()


def two_player(run):
    global time
    time = 0
    tetris = Tetris("two")
    run.intro_music.play(-1)
    while run.intro is True:
        if tetris.state != "intro":
            run.intro = False

        # Checks if window exit button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_1] != 0:
                run.intro_music.stop()
                tetris.computer = True
                run.select.play(0)
                run.screen.blit(run.background_4, run.background_4_rect)
                run.screen.blit(run.computer.image, run.computer.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                tetris.state = "playing"
                run.intro = False
            elif pygame.key.get_pressed()[pygame.K_b] != 0:
                run.intro_music.stop()
                run.select.play(0)
                run.screen.blit(run.background_4, run.background_4_rect)
                run.screen.blit(run.back.image, run.back.rect)
                pygame.display.flip()
                pygame.time.wait(1000)
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                text = check_click([run.computer, run.not_computer, run.back], click)
                if text == run.computer:
                    run.intro_music.stop()
                    tetris.computer = True
                    run.select.play(0)
                    run.screen.blit(run.background_4, run.background_4_rect)
                    run.screen.blit(run.computer.image, run.computer.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    tetris.state = "playing"
                    run.intro = False
                elif text == run.not_computer:
                    run.intro_music.stop()
                    tetris.computer = False
                    run.select.play(0)
                    run.screen.blit(run.background_4, run.background_4_rect)
                    run.screen.blit(run.not_computer.image, run.not_computer.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    tetris.state = "playing"
                    run.intro = False
                elif text == run.back:
                    run.intro_music.stop()
                    run.select.play(0)
                    run.screen.blit(run.background_4, run.background_4_rect)
                    run.screen.blit(run.back.image, run.back.rect)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    main()
            elif pygame.key.get_pressed()[pygame.K_2] != 0:
                run.intro_music.stop()
                tetris.computer = False
                run.select.play(0)
                run.screen.blit(run.background_4, run.background_4_rect)
                run.screen.blit(run.not_computer.image, run.not_computer.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                tetris.state = "playing"
                run.intro = False

        run.screen.blit(run.background_4, run.background_4_rect)
        run.screen.blit(run.back.image, run.back.rect)
        run.screen.blit(run.computer.image, run.computer.rect)
        run.screen.blit(run.not_computer.image, run.not_computer.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()

    run.begin_game()
    run.theme.play(-1)
    while run.play:
        if tetris.state != "playing":
            run.theme.stop()
            run.play = False
        if tetris.figure_left is None:
            tetris.new_figure("left")
        if tetris.figure_right is None:
            tetris.new_figure("right")

        if time % tetris.speed == 0:
            if not tetris.computer:
                tetris.move_down("left")
            tetris.move_down("right")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_p] != 0:
                resume = False
                while not resume:
                    for _ in pygame.event.get():
                        if pygame.key.get_pressed()[pygame.K_p] != 0:
                            resume = True
                    run.screen.fill(BLACK)
                    run.blink(run.pause)
                    pygame.display.flip()

        # Update
        tetris.update_two(run)
        time += 1
        # Draw everything
        run.screen.fill(BLACK)

        for i in range(len(tetris.grid_left)):
            for j in range(len(tetris.grid_left[i])):
                num = tetris.grid_left[i][j]
                if num != 9:
                    if num != 8:
                        color = COLORS[num]
                    else:
                        color = GREY
                else:
                    color = BLACK
                pygame.draw.rect(run.screen, color, (GRID_X_2_left + j * 30, GRID_Y_2_left + i * 30, BLOCK_W, BLOCK_H),
                                 0)

        for i in range(len(tetris.grid_right)):
            for j in range(len(tetris.grid_right[i])):
                num = tetris.grid_right[i][j]
                if num != 9:
                    if num != 8:
                        color = COLORS[num]
                    else:
                        color = GREY
                else:
                    color = BLACK
                pygame.draw.rect(run.screen, color,
                                 (GRID_X_2_right + j * 30, GRID_Y_2_right + i * 30, BLOCK_W, BLOCK_H), 0)

        tetris.draw_left(run)
        tetris.draw_right(run)

        pygame.draw.rect(run.screen, WHITE, (GRID_X_2_left, GRID_Y_2_left, GRID_W, GRID_H), 5)
        pygame.draw.rect(run.screen, WHITE, (GRID_X_2_right, GRID_Y_2_right, GRID_W, GRID_H), 5)
        if not tetris.computer:
            score_left = Text(str(tetris.score_left), WHITE, 25)
        else:
            score_left = Text("Computer", WHITE, 25)
        score_left.rect.centerx = run.screen_rect.centerx / 2
        score_left.rect.centery = 10
        run.screen.blit(score_left.image, score_left.rect)
        score_right = Text(str(tetris.score_right), WHITE, 25)
        score_right.rect.centerx = WIN_W * 0.75
        score_right.rect.centery = 10
        run.screen.blit(score_right.image, score_right.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()

    while run.outro:
        run.screen.blit(run.background_5, run.background_5_rect)
        winner = None
        if not tetris.computer:
            if tetris.winner == "right":
                winner = Text("The right player won!", BLACK, 45)
                winner.rect.centerx = run.screen_rect.centerx
                winner.rect.centery = run.screen_rect.centery / 2
            elif tetris.winner == "left":
                winner = Text("The left player won!", BLACK, 45)
                winner.rect.centerx = run.screen_rect.centerx
                winner.rect.centery = run.screen_rect.centery / 2
        else:
            if tetris.winner == "right":
                winner = Text("You won!", BLACK, 45)
                winner.rect.centerx = run.screen_rect.centerx
                winner.rect.centery - run.screen_rect.centerx / 2
            elif tetris.winner == "left":
                winner = Text("The computer won!", BLACK, 45)
                winner.rect.centerx = run.screen_rect.centerx
                winner.rect.centery = run.screen_rect.centery
        run.screen.blit(winner.image, winner.rect)
        run.blink(run.reenter)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.select.play(0)
                run.screen.blit(run.background_5, run.background_5_rect)
                run.screen.blit(run.reenter.image, run.reenter.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                run.outro = False
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                text = check_click([run.reenter], click)
                if text == run.reenter:
                    run.select.play(0)
                    run.screen.blit(run.background_5, run.background_5_rect)
                    run.screen.blit(run.reenter.image, run.reenter.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.outro = False
                    main()

        run.clock.tick(run.fps)
        pygame.display.flip()


def choosing(run):
    while run.choosing:
        # Checks if window exit button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_b] != 0:
                run.screen.blit(run.background_3, run.background_3_rect)
                run.screen.blit(run.back.image, run.back.rect)
                run.select.play(0)
                pygame.display.flip()
                pygame.time.wait(800)
                run.choosing = False
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run.text_group = []
                run.text_group = [run.chose_one, run.chose_two, run.title_2, run.back]
                click = pygame.mouse.get_pos()
                text = check_click(run.text_group, click)
                if text == run.chose_one:
                    run.screen.blit(run.background_3, run.background_3_rect)
                    run.screen.blit(run.chose_one.image, run.chose_one.rect)
                    run.select.play(0)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.choosing = False
                    run.mode = "one"
                    run.update_self()
                elif text == run.chose_two:
                    run.screen.blit(run.background_3, run.background_3_rect)
                    run.screen.blit(run.chose_two.image, run.chose_two.rect)
                    run.select.play(0)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.choosing = False
                    run.mode = "two"
                    run.update_self()
                elif text == run.title_2:
                    run.screen.blit(run.background_3, run.background_3_rect)
                    run.screen.blit(run.title_2.image, run.title_2.rect)
                    run.select.play(0)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    run.choosing = False
                    run.mode = "high_level"
                    run.update_self()
                elif text == run.back:
                    run.screen.blit(run.background_3, run.background_3_rect)
                    run.screen.blit(run.back.image, run.back.rect)
                    run.select.play(0)
                    pygame.display.flip()
                    pygame.time.wait(800)
                    run.choosing = False
                    main()

        run.screen.blit(run.background_3, run.background_3_rect)
        run.screen.blit(run.back.image, run.back.rect)
        run.screen.blit(run.title_2.image, run.title_2.rect)
        run.screen.blit(run.chose_one.image, run.chose_one.rect)
        run.screen.blit(run.chose_two.image, run.chose_two.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()


def mute(run):
    run.choosing_mute_assist = True
    while run.choosing_mute_assist:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                run.text_group = [run.mute_choice, run.not_mute_choice]
                text = check_click(run.text_group, click)
                if text == run.mute_choice:
                    run.select.play(0)
                    run.volume = 0
                    run.theme.set_volume(run.volume)
                    run.select.set_volume(run.volume)
                    run.intro_music.set_volume(run.volume)
                    run.levelup.set_volume(run.volume)
                    run.screen.blit(run.background_2, run.background_2_rect)
                    run.screen.blit(run.mute_choice.image, run.mute_choice.rect)
                    pygame.display.flip()
                    pygame.time.wait(500)
                    run.choosing_mute_assist = False
                elif text == run.not_mute_choice:
                    run.select.play(0)
                    run.volume = 2
                    run.theme.set_volume(run.volume)
                    run.select.set_volume(run.volume)
                    run.intro_music.set_volume(run.volume)
                    run.levelup.set_volume(run.volume)
                    run.screen.blit(run.background_2, run.background_2_rect)
                    run.screen.blit(run.not_mute_choice.image, run.not_mute_choice.rect)
                    pygame.display.flip()
                    pygame.time.wait(500)
                    run.choosing_mute_assist = False

        run.screen.blit(run.background_2, run.background_2_rect)
        run.screen.blit(run.mute_choice.image, run.mute_choice.rect)
        run.screen.blit(run.not_mute_choice.image, run.not_mute_choice.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()


def assist(run):
    run.choosing_mute_assist = True
    while run.choosing_mute_assist:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                run.text_group = [run.assist_choice, run.no_assist_choice]
                text = check_click(run.text_group, click)
                if text == run.assist_choice:
                    run.select.play(0)
                    run.screen.blit(run.background_2, run.background_2_rect)
                    run.screen.blit(run.assist_choice.image, run.assist_choice.rect)
                    pygame.display.flip()
                    pygame.time.wait(500)
                    run.assist_mode = True
                    run.choosing_mute_assist = False
                elif text == run.no_assist_choice:
                    run.select.play(0)
                    run.screen.blit(run.background_2, run.background_2_rect)
                    run.screen.blit(run.no_assist_choice.image, run.no_assist_choice.rect)
                    pygame.display.flip()
                    pygame.time.wait(500)
                    run.assist_mode = False
                    run.choosing_must_assist = False

        run.screen.blit(run.background_2, run.background_2_rect)
        run.screen.blit(run.assist_choice.image, run.assist_choice.rect)
        run.screen.blit(run.no_assist_choice.image, run.no_assist_choice.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()


def how_to(run):
    run.choosing_mute_assist = True
    space = Text("space/f -- hard drop", WHITE, 30)
    space.rect.y = 0
    down = Text("down/s -- soft drop", WHITE, 30)
    down.rect.y = space.rect.y + space.rect.height
    left = Text("left/d -- move left", WHITE, 30)
    left.rect.y = down.rect.y + down.rect.height
    right = Text("right/a -- move right", WHITE, 30)
    right.rect.y = left.rect.y + left.rect.height
    hold = Text("h/q -- hold", WHITE, 30)
    hold.rect.y = right.rect.y + right.rect.height
    two = Text("--during 2 player--", WHITE, 30)
    two.rect.y = hold.rect.y + hold.rect.height
    switch = Text("g -- switch", WHITE, 30)
    switch.rect.y = two.rect.y + two.rect.height
    clear = Text("y -- clear both grids", WHITE, 30)
    clear.rect.y = switch.rect.y + switch.rect.height
    pause = Text("p -- pause the game", WHITE, 30)
    pause.rect.y = clear.rect.y + clear.rect.height
    list_str = [space, down, left, right, hold, two, switch, clear, pause]
    for text in list_str:
        text.rect.centerx = run.screen_rect.centerx

    while run.choosing_mute_assist:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.select.play(0)
                run.screen.blit(run.background_2, run.background_2_rect)
                run.screen.blit(run.enter.image, run.enter.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                run.choosing_mute_assist = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()
                run.text_group = [run.enter]
                text = check_click(run.text_group, click)
                if text == run.enter:
                    run.select.play(0)
                    run.screen.blit(run.background_2, run.background_2_rect)
                    run.screen.blit(run.enter.image, run.enter.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.choosing_mute_assist = False
        run.screen.blit(run.background_2, run.background_2_rect)
        for text in list_str:
            run.screen.blit(text.image, text.rect)

        run.blink(run.enter)
        run.clock.tick(run.fps)
        pygame.display.flip()


def main_menu(run):
    run.enter = Text("Press enter to begin", WHITE, 45)
    run.enter.rect.centerx = run.screen_rect.centerx
    run.enter.rect.y = WIN_H - (run.enter.rect.height * 2)
    while run.main_menu:
        # Checks if window exit button pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                run.select.play(0)
                run.screen.blit(run.background_1, run.background_1_rect)
                run.screen.blit(run.enter.image, run.enter.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                run.main_menu = False
                break
            elif pygame.key.get_pressed()[pygame.K_0] != 0:
                run.select.play(0)
                run.screen.blit(run.background_1, run.background_1_rect)
                run.screen.blit(run.key.image, run.key.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                how_to(run)
            elif pygame.key.get_pressed()[pygame.K_1] != 0:
                run.select.play(0)
                run.screen.blit(run.background_1, run.background_1_rect)
                run.screen.blit(run.mute.image, run.mute.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                mute(run)
            elif pygame.key.get_pressed()[pygame.K_2] != 0:
                run.select.play(0)
                run.screen.blit(run.background_1, run.background_1_rect)
                run.screen.blit(run.assist.image, run.assist.rect)
                pygame.display.flip()
                pygame.time.wait(1500)
                assist(run)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run.text_group = [run.enter, run.key, run.mute, run.assist]
                click = pygame.mouse.get_pos()
                text = check_click(run.text_group, click)
                if text == run.enter:
                    run.select.play(0)
                    run.screen.blit(run.background_1, run.background_1_rect)
                    run.screen.blit(run.enter.image, run.enter.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    run.main_menu = False
                    break
                elif text == run.key:
                    run.select.play(0)
                    run.screen.blit(run.background_1, run.background_1_rect)
                    run.screen.blit(run.key.image, run.key.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    how_to(run)
                elif text == run.mute:
                    run.select.play(0)
                    run.screen.blit(run.background_1, run.background_1_rect)
                    run.screen.blit(run.mute.image, run.mute.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    mute(run)
                elif text == run.assist:
                    run.select.play(0)
                    run.screen.blit(run.background_1, run.background_1_rect)
                    run.screen.blit(run.assist.image, run.assist.rect)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    assist(run)

        run.screen.blit(run.background_1, run.background_1_rect)
        run.blink(run.enter)
        run.screen.blit(run.key.image, run.key.rect)
        run.screen.blit(run.mute.image, run.mute.rect)
        run.screen.blit(run.assist.image, run.assist.rect)

        run.clock.tick(run.fps)
        pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("Tetris")
    run = Game()
    main_menu(run)
    choosing(run)
    if run.mode == "one":
        one_player(run)
    elif run.mode == "two":
        two_player(run)
    elif run.mode == "high_level":
        high_level_mode(run)


if __name__ == "__main__":
    main()
