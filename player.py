import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, forward_angle):
        super().__init__()
        self.width = 100
        self.height = 50
        self.image_source = pygame.image.load('static/images/car.png').convert_alpha()  # 保留透明通道
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image.set_colorkey("white")

        self.move_sound = pygame.mixer.Sound("static/sounds/move.mp3")
        self.move_sound.set_volume(0.1)
        self.move_voice_channel = pygame.mixer.Channel(0)

        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.cx = center_x
        self.cy = center_y

        self.last_time = pygame.time.get_ticks()  # 返回当前时间(毫秒)
        self.delta_time = 0  # 相邻两帧时间间隔

        self.velocity_limit = 220  # 速度上限
        self.velocity = 0  # 当前速度
        self.friction = 0.9  # 摩擦系数
        self.move_acc = 600  # 加速度

        self.wheel_base = self.width * 0.8
        self.angle = math.degrees(30)  # 方向盘角度(弧度)
        self.rotation = 0  # 角速度
        self.forward_angle = forward_angle  # 行驶角度

    def update_delta_time(self):
        current_time = pygame.time.get_ticks()
        self.delta_time = (current_time - self.last_time) / 1000  # 单位变为秒
        self.last_time = current_time

    def input(self):
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_w] and key_press[pygame.K_s]:
            self.velocity = int(self.velocity * self.friction)
        elif key_press[pygame.K_w] or key_press[pygame.K_s]:
            if not self.move_voice_channel.get_busy():
                self.move_voice_channel.play(self.move_sound)
            if key_press[pygame.K_s]:
                self.velocity -= self.move_acc * self.delta_time
                self.velocity = max(self.velocity, -self.velocity_limit)
            if key_press[pygame.K_w]:
                self.velocity += self.move_acc * self.delta_time
                self.velocity = min(self.velocity, self.velocity_limit)
        else:
            self.move_voice_channel.stop()
            self.velocity = self.velocity * self.friction

        if key_press[pygame.K_d] and key_press[pygame.K_a]:
            self.rotation = 0
        elif key_press[pygame.K_d] or key_press[pygame.K_a]:
            # 计算转向率: ω = v * tan(δ) / L
            # 倒车要加绝对值
            if key_press[pygame.K_d]:
                self.rotation = abs(self.velocity) * math.tan(self.angle) / self.wheel_base
            if key_press[pygame.K_a]:
                self.rotation = -abs(self.velocity) * math.tan(self.angle) / self.wheel_base
            if self.velocity < 0:
                self.rotation *= -1
        else:
            self.rotation = 0

    def update_rotation(self):
        self.forward_angle += math.degrees(self.rotation * self.delta_time)
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("white")
        # 先旋转，再平移（绕左上角旋转->绕中心点旋转）
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update_location(self, direction=1):
        self.update_rotation()
        angle = math.radians(self.forward_angle)
        vx = self.velocity * math.cos(angle) * direction
        vy = self.velocity * math.sin(angle) * direction
        self.cx += vx * self.delta_time
        self.cy += vy * self.delta_time
        self.rect.center = (round(self.cx), round(self.cy))  # 赋值中心点坐标

    def crash(self):
        self.update_location(-1)
        if self.velocity > 0:
            self.velocity = min(-self.velocity, -150)
        else:
            self.velocity = max(-self.velocity, 150)

    def update(self):
        self.update_delta_time()
        self.input()
        self.update_location()
