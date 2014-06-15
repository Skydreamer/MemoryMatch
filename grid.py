__author__ = 'skydreamer'
import pygame, os, const, random


class Tile:
    def __init__(self, x=0, y=0, memory=False):
        self.x, self.y = x, y
        self.state = 0  # 0 - close, 1 - open
        self.is_memory = memory
        self.hover = False
        self.rect = pygame.Rect((x, y), (const.CELL_HEIGHT, const.CELL_WEIGHT))
        self.surface = pygame.Surface((const.CELL_HEIGHT, const.CELL_WEIGHT))
        self.surface.fill(pygame.Color(const.HIDE_CELL_COLOR))

    def refresh(self):
        if self.state:
            if self.is_memory:
                self.surface.fill(pygame.Color(const.OPEN_CELL_COLOR))
            else:
                self.surface.fill(pygame.Color(const.WRONG_CELL_COLOR))
        else:
            if self.hover:
                self.surface.fill(pygame.Color(const.HIGHLIGHT_CELL_COLOR))
            else:
                self.surface.fill(pygame.Color(const.HIDE_CELL_COLOR))

    def change_state(self, new_state=1):
        if self.state != new_state:
            self.state = new_state
            self.refresh()



class Grid:
    def __init__(self, screen=None):
        self.showed = False
        self.width = 4
        self.height = 4
        self.memory_tiles_count = const.START_MEMORY_COUNT
        self.tiles = list()
        self.memory_tiles = list()
        self.screen = screen
        self.field_rect = None

    def generate_tiles(self):
        self.tiles = list()
        self.memory_tiles = list()

        tiles_field_width = self.width * const.CELL_WEIGHT + (self.width - 1) * const.CELL_X_DISTANCE
        tiles_field_height = self.height * const.CELL_HEIGHT + (self.height - 1) * const.CELL_Y_DISTANCE

        screen_center_x, screen_center_y = self.screen.get_rect().center

        start_x = screen_center_x - (tiles_field_width / 2)
        start_y = screen_center_y - (tiles_field_height / 2)
        self.field_rect = pygame.Rect((start_x, start_y), (tiles_field_width, tiles_field_height))

        curr_x = start_x
        curr_y = start_y

        for y in range(self.height):
            for x in range(self.width):
                self.tiles.append(Tile(curr_x, curr_y))
                curr_x += const.CELL_X_DISTANCE + const.CELL_WEIGHT
            curr_y += const.CELL_Y_DISTANCE + const.CELL_HEIGHT
            curr_x = start_x

        remain_tiles = self.memory_tiles_count

        while remain_tiles > 0:
            rand_pos = random.randrange(0, self.width * self.height)

            if not self.tiles[rand_pos].is_memory:
                self.tiles[rand_pos].is_memory = True
                self.memory_tiles.append(self.tiles[rand_pos])
                remain_tiles -= 1

    def increase_grid(self):
        if self.height >= 6 or self.height == self.width:
            self.width += 1
        else:
            self.height += 1

    def decrease_grid(self):
        if self.height == 4 and self.width == 4:
            return
        if self.height < self.width:
            self.width -= 1
        else:
            self.height -= 1

    def increase_memory(self):
        self.memory_tiles_count += 1

    def decrease_memory(self):
        if self.memory_tiles_count > 5:
            self.memory_tiles_count -= 1

    def number_of_undiscovered(self):
        num = 0
        for tile in self.memory_tiles:
            if not tile.state:
                num += 1
        return num

    def show_memory(self):
        self.showed = True
        for tile in self.memory_tiles:
            tile.change_state(1)

    def hide_memory(self):
        self.showed = False
        for tile in self.memory_tiles:
            tile.change_state(0)


