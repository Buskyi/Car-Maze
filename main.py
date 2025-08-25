import pygame
import config
from game_manager import GameManager
from utils.draw_text import draw_text

pygame.init()
pygame.mixer.init()  # 初始化声音
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

ico=pygame.image.load("static/images/maze.png").convert_alpha()
pygame.display.set_icon(ico)
pygame.display.set_caption("汽车迷宫")

# pygame.mixer.music.load("static/sounds/bgm.mp3")
# pygame.mixer.music.set_volume(0.1)
# pygame.mixer.music.play(-1) # -1循环播放

running = True
success_time = -1
finished = False
died = False
game_manager = GameManager(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if finished and event.type == pygame.KEYDOWN:
            running = False

        if died and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:  # 重试本关
                game_manager.reset_lives()  # 恢复 3 条命
                game_manager.load()  # 重新载入当前关卡
                died = False
            elif event.key == pygame.K_n:  # 退出
                running = False

    screen.fill("white")
    if finished:
        draw_text(screen, "Win!", 200, 600, 450)
        draw_text(screen, "Press any key to continue...", 50, 600, 550)
    elif died:
        draw_text(screen, "Game Over T_T", 100, 600, 450)
        draw_text(screen, "Press Y to retry, N to exit.", 50, 600, 550)
    else:
        if success_time >= 0:
            if pygame.time.get_ticks() - success_time >= 1000:
                if not game_manager.next_level():  # 没有下一关了
                    finished = True
                    continue
                success_time = -1
        if game_manager.update():
            success_time = pygame.time.get_ticks()
        if game_manager.lives <= 0:
            died = True

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
