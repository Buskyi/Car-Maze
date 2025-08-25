import pygame
from player import Player
from items import Wall, Star, Door, Heart
from utils.collide import collided_rect, collided_circle
import os


class GameManager:
    def __init__(self, screen, level=1):
        self.screen = screen
        self.level = level
        self.player = None
        self.lives = 3
        self.hearts_list = []
        self.stars_cnt = 0
        self.walls = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()  # 生命精灵组
        self.load_hearts()
        self.load()

        self.crash_sound = pygame.mixer.Sound("static/sounds/crash.mp3")
        self.crash_sound.set_volume(0.5)
        self.eat_star_sound = pygame.mixer.Sound("static/sounds/eat_star.mp3")
        self.eat_star_sound.set_volume(0.5)
        self.success = pygame.mixer.Sound("static/sounds/success.mp3")
        self.success.set_volume(0.5)
        self.else_voice_channel = pygame.mixer.Channel(1)

    def load_hearts(self):
        self.lives=3
        self.hearts.empty()
        self.hearts_list.clear()
        for i in range(3):
            heart = Heart(left=10 + i * (32 + 8), top=10)
            self.hearts_list.append(heart)
            self.hearts.add(heart)

    def reset_lives(self):
        self.lives = 3
        self.load_hearts()

    def load_walls(self, walls):
        self.walls.empty()  # 清空
        for wall in walls:
            self.walls.add(wall)

    def load_stars(self, stars):
        self.stars.empty()
        for star in stars:
            self.stars.add(star)

    def load_doors(self, doors):
        self.doors.empty()
        for door in doors:
            self.doors.add(door)

    def load_player(self, center_x, center_y, forward_angle):
        if self.player:
            self.player.kill()
        self.player = Player(center_x, center_y, forward_angle)

    def load(self):
        self.load_hearts()
        with open("static/maps/level%d.txt" % self.level, "r") as fin:
            # 加载墙
            walls_cnt = int(fin.readline())
            walls = []
            for i in range(walls_cnt):
                x, y, w, h = map(int, fin.readline().split())
                walls.append(Wall(x, y, w, h))
            self.load_walls(walls)
            # 加载星星
            self.stars_cnt = int(fin.readline())
            stars = []
            for i in range(self.stars_cnt):
                x, y = map(int, fin.readline().split())
                stars.append(Star(x, y))
            self.load_stars(stars)
            # 加载传送门
            doors_cnt = int(fin.readline())
            doors = []
            for i in range(doors_cnt):
                x, y = map(int, fin.readline().split())
                doors.append(Door(x, y))
            self.load_doors(doors)
            # 加载车
            center_x, center_y, forward_angle = map(int, fin.readline().split())
            self.load_player(center_x, center_y, forward_angle)

    def next_level(self):
        self.level += 1
        if not os.path.isfile("static/maps/level%d.txt" % self.level):
            return False
        self.load()
        return True

    def check_collision(self):  # 检测碰撞
        if pygame.sprite.spritecollide(self.player, self.walls, False, collided_rect):
            self.else_voice_channel.play(self.crash_sound)
            if self.lives > 0:
                self.lives -= 1
                self.hearts_list[self.lives].kill()
            self.player.crash()

        if pygame.sprite.spritecollide(self.player, self.stars, True, collided_circle):
            self.else_voice_channel.play(self.eat_star_sound)
            self.stars_cnt -= 1
        if self.stars_cnt == 0:
            if pygame.sprite.spritecollide(self.player, self.doors, True, collided_circle):
                self.else_voice_channel.play(self.success)
                return True
        return False

    def update(self):
        # 总结：blit 是“贴图”，draw 是“画图”
        self.stars.update()
        self.stars.draw(self.screen)

        self.doors.update()
        self.doors.draw(self.screen)

        self.player.update()
        success = self.check_collision()
        self.screen.blit(self.player.image, self.player.rect)

        self.walls.update()
        self.walls.draw(self.screen)

        self.hearts.update()
        self.hearts.draw(self.screen)

        return success
