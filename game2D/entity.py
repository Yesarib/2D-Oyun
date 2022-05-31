import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.yon = pygame.math.Vector2()

    def hareket(self, speed):
        if self.yon.magnitude() != 0:
            self.yon = self.yon.normalize()

        self.hitbox.x += self.yon.x * speed
        self.carpısma('horizontal')
        self.hitbox.y += self.yon.y * speed
        self.carpısma('vertical')
        self.rect.center = self.hitbox.center

    def carpısma(self, yon):
        if yon == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.yon.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.yon.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if yon == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.yon.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.yon.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        # Vuruş Efekti
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else: return 0

