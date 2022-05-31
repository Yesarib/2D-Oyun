import sys
import pygame
import main
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapons
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from upgrade import Upgrade
from buttons import Button

pygame.init()

class Level:
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(ui_font, 32)
        self.running = True

        self.visible_sprites = YKamera()
        self.obstacles_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprite = pygame.sprite.Group()
        self.attackable_sprite = pygame.sprite.Group()

        self.harita()
        # ui
        self.ui = UI()
        self.upgrade = Upgrade(self.player)

        # particles
        self.animations_player = AnimationPlayer()

    def harita(self):
        layouts = {
            'sınır': import_csv_layout('map/map_FloorBlocks.csv'),
            'cim': import_csv_layout('map/map_Grass.csv'),
            'obje': import_csv_layout('map/map_LargeObjects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'cim': import_folder('graphics/grass'),
            'obje': import_folder('graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'sınır':
                            Tile((x, y), [self.obstacles_sprites, self.attackable_sprite], 'invisible')
                        if style == 'cim':
                            random_grass_image = choice(graphics['cim'])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacles_sprites, self.attackable_sprite],
                                'grass',
                                random_grass_image)
                        if style == 'obje':
                            surf = graphics['obje'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacles_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites,
                                                     self.saldırı, self.destroy_attack)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprite],
                                      self.obstacles_sprites,
                                      self.damage_player, self.trigger_death, self.add_xp)

    def saldırı(self):
        self.current_attack = Weapons(self.player, [self.visible_sprites, self.attack_sprite])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprite:
            for attack_sprite in self.attack_sprite:
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprite, False)
                if collision_sprite:
                    for target_sprite in collision_sprite:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animations_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animations_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death(self, pos, particles_type):
        self.animations_player.create_particles(particles_type, pos, self.visible_sprites)

    def add_xp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

        self.dead()

    def dead(self):
        if self.player.health <= 0:
            self.player.kill()
            MainMenu




class MainMenu:
    #level = Level()
    #screen = level.screen
    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)

    def main_menu(self):
        BG = pygame.image.load("assets/Background.png")

        while True:
            self.screen.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")

            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        main
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

class YKamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.yari_genislik = self.display_surface.get_size()[0] // 2
        self.yari_uzunluk = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.zemin = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.zemin_rect = self.zemin.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.yari_genislik
        self.offset.y = player.rect.centery - self.yari_uzunluk

        zemin_offset = self.zemin_rect.topleft - self.offset
        self.display_surface.blit(self.zemin, zemin_offset)

        for s in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset = s.rect.topleft - self.offset
            self.display_surface.blit(s.image, offset)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

