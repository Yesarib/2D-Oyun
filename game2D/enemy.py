from entity import Entity
from settings import *
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death, add_exp):

        super().__init__(groups)
        self.sprite_type = 'enemy'

        # grafik setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # hareket
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # canavar stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # mob etkileşimi
        self.can_attack = True
        self.timer = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death = trigger_death
        self.add_exp = add_exp

        self.vulnerable = True
        self.hit_time = None
        self.invincibility = 300

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        yol = f'canavarlar/{name}/'
        for a in self.animations.keys():
            self.animations[a] = import_folder(yol + a)

    def get_player_status(self, player):
        enemy_vc = pygame.math.Vector2(self.rect.center)
        player_vc = pygame.math.Vector2(player.rect.center)
        mesafe = (player_vc - enemy_vc).magnitude()

        if mesafe > 0:
            yon = (player_vc - enemy_vc).normalize()
        else:
            yon = pygame.math.Vector2()
        return mesafe, yon

    def get_status(self, player):
        mesafe = self.get_player_status(player)[0]

        if mesafe <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif mesafe <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.timer = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.yon = self.get_player_status(player)[1]
        else:
            self.yon = pygame.math.Vector2()

    def animated(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Vuruş Efekti
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.timer >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility:
                self.vulnerable = True

    def get_damage(self, player, attack_type):

        if self.vulnerable:
            self.yon = self.get_player_status(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                pass
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death(self.rect.center, self.monster_name)
            self.add_exp(self.exp)

    def hit_reaction(self):
        if not self.vulnerable:
            self.yon *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.hareket(self.speed)
        self.animated()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
