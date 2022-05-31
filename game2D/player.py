import pygame
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):

    def __init__(self, pos, grup, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(grup)
        self.image = pygame.image.load('Karakter/down_idle/idle_down.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image,(32,32))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, hitbox_offset['player'])


        # grafik
        self.player_animasyon()
        self.status = 'down'

        self.attack = False
        self.attack_aralik = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # ui
        self.stats = {'health': 100, 'attack': 10, 'speed': 5}
        self.max_stats = {'health': 300, 'attack': 20, 'speed': 10}
        self.upgrade_cost = {'health': 100, 'attack': 100, 'speed': 100}
        self.health = self.stats['health'] * 0.5
        self.max_health = self.max_stats['health']
        self.exp = 5000
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability = 500

    def player_animasyon(self):
        karakter_path = 'Karakter/'
        self.animasyon = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [],
                          'left_idle': [], 'up_idle': [], 'down_idle': [], 'up_attack': [], 'down_attack': [],
                          'left_attack': [], 'right_attack': []}
        for animation in self.animasyon.keys():
            full_path = karakter_path + animation
            self.animasyon[animation] = import_folder(full_path)

    def klavye(self):
        if not self.attack:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.yon.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.yon.y = 1
                self.status = 'down'
            else:
                self.yon.y = 0
            if keys[pygame.K_RIGHT]:
                self.yon.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.yon.x = -1
                self.status = 'left'
            else:
                self.yon.x = 0

            if keys[pygame.K_SPACE]:
                self.attack = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_c]:
                cost = 100
                if self.health != self.max_health:
                    if self.exp >= cost:
                        self.health += 20
                        self.exp -= cost
                        if self.health >= self.stats['health']:
                            self.stats['health'] = self.health

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attack:
            if current_time - self.attack_time >= self.attack_aralik + weapon_data[self.weapon]['cooldown']:
                self.attack = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability:
                self.vulnerable = True

    def get_status(self):
        if self.yon.x == 0 and self.yon.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attack:
            var = self.yon.x == 0
            var = self.yon.y == 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animete(self):
        animasyon = self.animasyon[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animasyon):
            self.frame_index = 0

        self.image = animasyon[int(self.frame_index)]
        # self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def update(self):
        self.klavye()
        self.cooldowns()
        self.get_status()
        self.animete()
        self.hareket(self.stats['speed'])
