import pygame
from pygame.transform import scale


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Star(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image_source = pygame.image.load("static/images/star.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_source, (50, 50))
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.scale = 1
        self.scale_delta = 0.001

    def update(self):
        self.scale += self.scale_delta
        if self.scale >= 1.05 or self.scale <= 0.95:
            self.scale_delta *= -1
        self.image = pygame.transform.scale(self.image_source, (50 * self.scale, 50 * self.scale))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


class Door(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image_source = pygame.image.load("static/images/door.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_source, (100, 100))
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.scale = 1
        self.scale_delta = 0.0005

    def update(self):
        self.scale += self.scale_delta
        if self.scale >= 1.02 or self.scale <= 0.98:
            self.scale_delta *= -1
        self.image = pygame.transform.scale(self.image_source, (100 * self.scale, 100 * self.scale))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


class Heart(pygame.sprite.Sprite):
    def __init__(self, left, top):
        super().__init__()
        self.image = pygame.image.load("static/images/heart.png").convert_alpha()
        self.image.set_colorkey("white")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=(left, top))
