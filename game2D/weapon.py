import pygame


class Weapons(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        yon = player.status.split('_')[0]
        self.sprite_type = 'weapon'
        full_path = f'silahlar/{player.weapon}/{yon}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        if yon == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif yon == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif yon == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(0, 0))
        elif yon == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(center=player.rect.center)
