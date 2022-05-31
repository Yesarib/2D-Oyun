import pygame
from settings import *


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(ui_font, ui_font_size)

        self.health_bar_rect = pygame.Rect(10, 10, health_bar, bar_height)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self, current, max_bar, bg_rect, color):
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)

        x = current / max_bar
        current_witdh = bg_rect.width * x
        current_rect = bg_rect.copy()
        current_rect.width = current_witdh

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 3)

    def show_exp(self, exp):
        txt_surf = self.font.render(str(int(exp)), False, txt_color)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        txt_rect = txt_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, ui_bg_color, txt_rect.inflate(10, 10))
        self.display_surface.blit(txt_surf, txt_rect)
        pygame.draw.rect(self.display_surface, ui_border_color, txt_rect.inflate(10, 10), 3)

    def weapon_selection(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, item_box, item_box)
        pygame.draw.rect(self.display_surface, ui_bg_color, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, ui_border_color_active, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, ui_border_color, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.weapon_selection(10, 625, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, health_color)

        self.show_exp(player.exp)
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
