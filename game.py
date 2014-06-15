# -*- coding: utf-8 -*-
__author__ = 'skydreamer'
import pygame
import grid
import const
import misc
import sys


class Game:
    def __init__(self):
        self.game = None
        self.name = 'Memory Match - Pygame'
        self.background = None
        self.font = None
        self.is_active = True

        self.init_window()
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.load_background()
        self.load_font()

        self.game = MemoryMatch()

    def init_window(self):
        pygame.init()
        pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
        pygame.display.set_caption(self.name)

    def load_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.background, back_rect = misc.load_image('background.jpg')

    def load_font(self):
        self.font = pygame.font.SysFont('monospace', const.FONT_SIZE)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_score_cloud(self):
        out = u'ОЧКИ {0}'.format(self.game.score)
        score_label = self.font.render(out, 1, pygame.Color(const.FONT_COLOR))
        surface = pygame.Surface((const.CLOUD_WIDTH, const.CLOUD_HEIGHT))
        surface.set_alpha(const.CLOUD_APLHA)
        surface.fill(pygame.Color(const.CLOUD_COLOR))
        surface.blit(score_label, (10, 5))
        self.screen.blit(surface, (const.WINDOW_WIDTH - const.CLOUD_WIDTH - const.CLOUD_BORDER, 10))

    def draw_tier_cloud(self):
        out = u'ЭТАП {0} ИЗ {1}'.format(self.game.trial, const.MAX_TRIALS)
        tier_label = self.font.render(out, 1, pygame.Color(const.FONT_COLOR))
        surface = pygame.Surface((const.CLOUD_WIDTH, const.CLOUD_HEIGHT))
        surface.set_alpha(const.CLOUD_APLHA)
        surface.fill(pygame.Color(const.CLOUD_COLOR))
        surface.blit(tier_label, (10, 5))
        self.screen.blit(surface, (const.WINDOW_WIDTH - 2 * const.CLOUD_WIDTH - 2 * const.CLOUD_BORDER, 10))

    def draw_tier_state_cloud(self):
        out = u'ПЛИТКИ {0}'.format(self.game.grid.memory_tiles_count)
        state_label = self.font.render(out, 1, pygame.Color(const.FONT_COLOR))
        surface = pygame.Surface((const.CLOUD_WIDTH, const.CLOUD_HEIGHT))
        surface.set_alpha(const.CLOUD_APLHA)
        surface.fill(pygame.Color(const.CLOUD_COLOR))
        surface.blit(state_label, (10, 5))
        self.screen.blit(surface, (const.WINDOW_WIDTH - 3 * const.CLOUD_WIDTH - 3 * const.CLOUD_BORDER, 10))

    def draw_final_score_cloud(self):
        out = u'РЕЗУЛЬТАТ : {0}'.format(self.game.score)
        state_label = self.font.render(out, 1, pygame.Color(const.FONT_COLOR))
        surface = pygame.Surface((const.CLOUD_WIDTH * 2, const.CLOUD_HEIGHT))
        surface.set_alpha(const.CLOUD_APLHA)
        surface.fill(pygame.Color(const.CLOUD_COLOR))
        surface.blit(state_label, (10, 5))
        screen_center_x = self.screen.get_rect().width / 2
        screen_center_y = self.screen.get_rect().height / 2
        self.screen.blit(surface, (screen_center_x - const.CLOUD_WIDTH, screen_center_y - const.CLOUD_HEIGHT / 2))

    def draw_memory_tails(self):
        field = pygame.Surface((self.game.grid.field_rect.width + 2 * const.TILE_FIELD_BORDER,
                               self.game.grid.field_rect.height + 2 * const.TILE_FIELD_BORDER,))
        field.fill(pygame.Color(const.TILE_FIELD_COLOR))
        self.screen.blit(field, (self.game.grid.field_rect.left - const.TILE_FIELD_BORDER,
                                 self.game.grid.field_rect.top - const.TILE_FIELD_BORDER))

        for tile in self.game.grid.tiles:
            self.screen.blit(tile.surface, (tile.x, tile.y))

    def run(self):
        self.game.start()

        while True:
            if self.game.timer > 0:
                if self.game.is_memory_time:
                    if not self.game.grid.showed:
                        self.game.grid.show_memory()
            else:
                if self.game.is_memory_time:
                    self.game.is_memory_time = False
                    if self.game.grid.showed:
                        self.game.grid.hide_memory()
                    if self.game.next:
                        self.game.next_level()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.MOUSEMOTION:
                    if not self.game.is_memory_time and self.game.timer <= 0:
                        mouse_x, mouse_y = event.pos
                        self.game.check_move(mouse_x, mouse_y)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.game.is_memory_time and self.game.timer <= 0:
                        mouse_x, mouse_y = event.pos
                        self.game.check_click(mouse_x, mouse_y)

            if not self.game.end_game:
                self.draw_background()
                self.draw_memory_tails()
                self.draw_score_cloud()
                self.draw_tier_cloud()
                self.draw_tier_state_cloud()
            else:
                self.draw_final_score_cloud()

            pygame.display.update()

            if self.game.timer >= 0:
                self.game.timer -= self.clock.tick(60)


class MemoryMatch:
    def __init__(self):
        self.score = 0
        self.is_memory_time = False
        self.next = False
        self.end_game = False
        self.level_clicks = 0
        self.win_streak = 0
        self.timer = 0
        self.trial = 0

        self.score_bonuses = []
        self.screen = pygame.display.get_surface()
        self.grid = grid.Grid(self.screen)
        self.generate_score_bonuses(30)

    def generate_score_bonuses(self, length):
        base = 10
        previous = 0
        for level in range(length):
            self.score_bonuses.append(base + previous)
            base, previous = base + previous, base

    def next_level(self):
        if self.trial == const.MAX_TRIALS:
            self.end_game = True
        self.trial += 1
        self.level_clicks = 0
        self.grid.generate_tiles()
        self.is_memory_time = True
        self.next = False
        self.setup_timer(const.MEMORY_TIME)

    def start(self):
        self.next_level()

    def check_click(self, x, y):
        for tile in self.grid.tiles:
            if tile.rect.collidepoint(x, y):
                if self.level_clicks <= self.grid.memory_tiles_count and tile.state == 0:
                    if tile.is_memory:
                        self.score += const.TILE_SCORE
                    self.level_clicks += 1
                    tile.change_state()
                    if self.level_clicks == self.grid.memory_tiles_count:
                        undiscovered = self.grid.number_of_undiscovered()
                        print undiscovered
                        if undiscovered == 0:
                            self.grid.increase_memory()
                            self.win_streak += 1
                            self.score += self.score_bonuses[self.grid.memory_tiles_count - 5]
                            if self.win_streak == 3:
                                self.win_streak = 0
                                self.grid.increase_grid()
                        elif undiscovered == 1:
                            self.win_streak = 0
                        elif undiscovered >= 2:
                            self.win_streak = 0
                            self.grid.decrease_memory()
                            self.grid.decrease_grid()

                        self.is_memory_time = True
                        self.next = True
                        self.setup_timer(const.TIER_DELAY)

    def setup_timer(self, time):
        self.timer = time * 1000

    def check_move(self, x, y):
        for tile in self.grid.tiles:
            if tile.rect.collidepoint(x, y):
                tile.hover = True
                tile.refresh()
            else:
                if tile.hover:
                    tile.hover = False
                    tile.refresh()


if __name__ == '__main__':
    Game().run()