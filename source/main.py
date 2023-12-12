# 202130440811 - 赖言安 - 华南理工大学网络工程

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *

import ResInit
import SceneCreate

pygame.init()

# 帧率上限 60
FPS = 60
FPS_clock = pygame.time.Clock()

# 物理量初始化
g = 0.2
size = width, height = 1280, 720

# 计算器初始化
night_timer = -1

# 重开标识
game_reset = False

# 背景音乐
pygame.mixer.music.load('asset/sound/music0.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# 前景黑幕以及局部照亮机制
def nightFallInit():
    global night_timer
    ResInit.UI_Foreground_Dark.set_alpha(0)
    # 初始 30s 后进入傍晚
    night_timer = 5400

nightFallInit()

def nightFall():
    global night_timer
    if night_timer >= 0 and not game_reset:
        night_timer += 1
        if night_timer > 16200:
            night_timer = 0
    
    # 白天时间：120s = 7200gt
    # 傍晚时间：30s = 1800gt 天慢慢变黑 9000
    # 夜晚时间：90s = 5400gt 天全黑 14400
    # 黎明时间：30s = 1800gt 天慢慢变亮 16200
    if night_timer >= 7200:
        if night_timer in range (7200, 9000):
            foreground_alpha_value = int(round(((night_timer - 7200) / 1800), 2) * 255)
            if foreground_alpha_value > 255:
                foreground_alpha_value = 255

        if night_timer in range (9000, 14400):
            foreground_alpha_value = 255

        if night_timer in range (14400, 16201):
            foreground_alpha_value = 255 - int(round(((night_timer - 14400) / 1800), 2) * 255)
            if foreground_alpha_value < 0:
                foreground_alpha_value = 0

        ResInit.UI_Foreground_Dark.set_alpha(foreground_alpha_value)


        # 根据沙糖桔和火把的位置，抠出光亮部分
        if SceneCreate.citrus.fuel_value <= 0:
            return
        citrus_centerx = SceneCreate.citrus.rect.centerx
        citrus_centery = SceneCreate.citrus.rect.centery
        original_alpha = pygame.Color(0, 0, 0, foreground_alpha_value)
        low_alpha = pygame.Color(0, 0, 0, 76)
        no_alpha = pygame.Color(0, 0, 0, 0)
        if night_timer >= 3600:
            lightmask_citrus = pygame.PixelArray(ResInit.UI_Foreground_Dark)
            lightmask_citrus[:, :] = original_alpha

            # 火炬
            for torch in SceneCreate.block_torch_group.sprites():
                # 火炬熄灭则没有光
                if torch.isIgnited == False:
                    continue
                
                torch_centerx = torch.rect.centerx
                torch_centery = torch.rect.centery

                # 如果火炬中心在屏幕外则不显示光，防止渲染出错
                if torch_centerx > width or torch_centerx < 0 or torch_centery > height or torch_centery < 0:
                    continue

                lightmask_torch = pygame.PixelArray(ResInit.UI_Foreground_Dark)

                light_range_torch = 80
                
                light_x_min = torch_centerx - light_range_torch
                light_x_max = torch_centerx + light_range_torch
                light_y_min = torch_centery - light_range_torch
                light_y_max = torch_centery + light_range_torch

                range_x = []
                range_y = []

                range_x.append(int(light_x_min))
                range_x.append(int(light_x_max))
                range_y.append(int(light_y_min + (2/3) * light_range_torch))
                range_y.append(int(light_y_max - (2/3) * light_range_torch))

                range_x.append(int(light_x_min + (2/3) * light_range_torch))
                range_x.append(int(light_x_max - (2/3) * light_range_torch))
                range_y.append(int(light_y_min))
                range_y.append(int(light_y_max))

                range_x.append(int(light_x_min + (1/8) * light_range_torch))
                range_x.append(int(light_x_max - (1/8) * light_range_torch))
                range_y.append(int(light_y_min + (1/2) * light_range_torch))
                range_y.append(int(light_y_max - (1/2) * light_range_torch))

                range_x.append(int(light_x_min + (1/2) * light_range_torch))
                range_x.append(int(light_x_max - (1/2) * light_range_torch))
                range_y.append(int(light_y_min + (1/8) * light_range_torch))
                range_y.append(int(light_y_max - (1/8) * light_range_torch))

                range_x.append(int(light_x_min + (1/4) * light_range_torch))
                range_x.append(int(light_x_max - (1/4) * light_range_torch))
                range_y.append(int(light_y_min + (1/4) * light_range_torch))
                range_y.append(int(light_y_max - (1/4) * light_range_torch))

                for i in range(0, 9):
                    if range_x[i] < 0:
                        range_x[i] = 0
                    if range_x[i] > 1280:
                        range_x[i] = 1280
                    if range_y[i] < 0:
                        range_y[i] = 0
                    if range_y[i] > 720:
                        range_y[i] = 720

                lightmask_torch[range_x[0]:range_x[1], range_y[0]:range_y[1]] = low_alpha
                lightmask_torch[range_x[2]:range_x[3], range_y[2]:range_y[3]] = low_alpha
                lightmask_torch[range_x[4]:range_x[5], range_y[4]:range_y[5]] = low_alpha
                lightmask_torch[range_x[6]:range_x[7], range_y[6]:range_y[7]] = low_alpha
                lightmask_torch[range_x[8]:range_x[9], range_y[8]:range_y[9]] = low_alpha

                del lightmask_torch

            # 根据不同的燃料值，分为三个等级的照亮范围
            if SceneCreate.citrus.fuel_value in range(0, 3200):
                light_range_small = 80
                light_range_big = 128
            if SceneCreate.citrus.fuel_value in range(3200, 6400):
                light_range_small = 112
                light_range_big = 160
            if SceneCreate.citrus.fuel_value in range(6400, 9601):
                light_range_small = 144
                light_range_big = 192

            # range big
            light_x_min = citrus_centerx - light_range_big
            light_x_max = citrus_centerx + light_range_big
            light_y_min = citrus_centery - light_range_big
            light_y_max = citrus_centery + light_range_big

            range_x = []
            range_y = []

            range_x.append(int(light_x_min))
            range_x.append(int(light_x_max))
            range_y.append(int(light_y_min + (2/3) * light_range_big))
            range_y.append(int(light_y_max - (2/3) * light_range_big))

            range_x.append(int(light_x_min + (2/3) * light_range_big))
            range_x.append(int(light_x_max - (2/3) * light_range_big))
            range_y.append(int(light_y_min))
            range_y.append(int(light_y_max))

            range_x.append(int(light_x_min + (1/8) * light_range_big))
            range_x.append(int(light_x_max - (1/8) * light_range_big))
            range_y.append(int(light_y_min + (1/2) * light_range_big))
            range_y.append(int(light_y_max - (1/2) * light_range_big))

            range_x.append(int(light_x_min + (1/2) * light_range_big))
            range_x.append(int(light_x_max - (1/2) * light_range_big))
            range_y.append(int(light_y_min + (1/8) * light_range_big))
            range_y.append(int(light_y_max - (1/8) * light_range_big))

            range_x.append(int(light_x_min + (1/4) * light_range_big))
            range_x.append(int(light_x_max - (1/4) * light_range_big))
            range_y.append(int(light_y_min + (1/4) * light_range_big))
            range_y.append(int(light_y_max - (1/4) * light_range_big))

            for i in range(0, 9):
                if range_x[i] < 0:
                    range_x[i] = 0
                if range_x[i] > 1280:
                    range_x[i] = 1280
                if range_y[i] < 0:
                    range_y[i] = 0
                if range_y[i] > 720:
                    range_y[i] = 720

            lightmask_citrus[range_x[0]:range_x[1], range_y[0]:range_y[1]] = low_alpha
            lightmask_citrus[range_x[2]:range_x[3], range_y[2]:range_y[3]] = low_alpha
            lightmask_citrus[range_x[4]:range_x[5], range_y[4]:range_y[5]] = low_alpha
            lightmask_citrus[range_x[6]:range_x[7], range_y[6]:range_y[7]] = low_alpha
            lightmask_citrus[range_x[8]:range_x[9], range_y[8]:range_y[9]] = low_alpha

            # range small
            light_x_min = citrus_centerx - light_range_small
            light_x_max = citrus_centerx + light_range_small
            light_y_min = citrus_centery - light_range_small
            light_y_max = citrus_centery + light_range_small

            range_x = []
            range_y = []

            range_x.append(int(light_x_min))
            range_x.append(int(light_x_max))
            range_y.append(int(light_y_min + (2/3) * light_range_small))
            range_y.append(int(light_y_max - (2/3) * light_range_small))

            range_x.append(int(light_x_min + (2/3) * light_range_small))
            range_x.append(int(light_x_max - (2/3) * light_range_small))
            range_y.append(int(light_y_min))
            range_y.append(int(light_y_max))

            range_x.append(int(light_x_min + (1/8) * light_range_small))
            range_x.append(int(light_x_max - (1/8) * light_range_small))
            range_y.append(int(light_y_min + (1/2) * light_range_small))
            range_y.append(int(light_y_max - (1/2) * light_range_small))

            range_x.append(int(light_x_min + (1/2) * light_range_small))
            range_x.append(int(light_x_max - (1/2) * light_range_small))
            range_y.append(int(light_y_min + (1/8) * light_range_small))
            range_y.append(int(light_y_max - (1/8) * light_range_small))

            range_x.append(int(light_x_min + (1/4) * light_range_small))
            range_x.append(int(light_x_max - (1/4) * light_range_small))
            range_y.append(int(light_y_min + (1/4) * light_range_small))
            range_y.append(int(light_y_max - (1/4) * light_range_small))

            for i in range(0, 9):
                if range_x[i] < 0:
                    range_x[i] = 0
                if range_x[i] > 1280:
                    range_x[i] = 1280
                if range_y[i] < 0:
                    range_y[i] = 0
                if range_y[i] > 720:
                    range_y[i] = 720

            lightmask_citrus[range_x[0]:range_x[1], range_y[0]:range_y[1]] = no_alpha
            lightmask_citrus[range_x[2]:range_x[3], range_y[2]:range_y[3]] = no_alpha
            lightmask_citrus[range_x[4]:range_x[5], range_y[4]:range_y[5]] = no_alpha
            lightmask_citrus[range_x[6]:range_x[7], range_y[6]:range_y[7]] = no_alpha
            lightmask_citrus[range_x[8]:range_x[9], range_y[8]:range_y[9]] = no_alpha

            del lightmask_citrus

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 按钮
        if event.type == MOUSEBUTTONDOWN:
            if game_reset and SceneCreate.ui_button_reset.rect.collidepoint(event.pos):
                SceneCreate.sceneReset()
                SceneCreate.citrus.reset()
                SceneCreate.ui_button_reset.player_is_dead = False
                nightFallInit()
                game_reset = False

    nightFall()

    # 获取按键
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        SceneCreate.citrus.moveUp()
    if not keys[pygame.K_UP]:
        SceneCreate.citrus.moveUpJumping()
    if keys[pygame.K_LEFT]:
        SceneCreate.citrus.moveLeft()
    if keys[pygame.K_RIGHT]:
        SceneCreate.citrus.moveRight()
    if keys[pygame.K_LSHIFT]:
        SceneCreate.citrus.slowFalling()
    if not keys[pygame.K_LSHIFT]:
        SceneCreate.citrus.slowFallingPressed()
    if keys[pygame.K_SPACE]:
        SceneCreate.citrus.dashUpwards()
    if not keys[pygame.K_SPACE]:
        SceneCreate.citrus.dashUpwardsPressed()

    # 角色死亡检测
    if SceneCreate.citrus.is_dead:
        SceneCreate.ui_button_reset.player_is_dead = True
        game_reset = True

    # 刷新显示
    gametick = pygame.time.get_ticks()
    ResInit.screen.fill('black')
    SceneCreate.ui_background_group.update(gametick)
    SceneCreate.ui_background_group.draw(ResInit.screen)
    SceneCreate.block_group.update(gametick)
    SceneCreate.block_group.draw(ResInit.screen)
    SceneCreate.avatar_group.update(gametick)
    SceneCreate.avatar_group.draw(ResInit.screen)
    SceneCreate.map_group.update()
    SceneCreate.map_group.draw(ResInit.screen)
    SceneCreate.ui_foreground_group.update(gametick)
    SceneCreate.ui_foreground_group.draw(ResInit.screen)
    SceneCreate.ui_group.update(gametick)
    SceneCreate.ui_group.draw(ResInit.screen)
    SceneCreate.ui_button_group.update(gametick)
    SceneCreate.ui_skill_group.update(gametick)
    SceneCreate.ui_skill_group.draw(ResInit.screen)

    # 显示分数
    score_name = ResInit.font.render('Score', True, (255, 255, 255), None)
    score_name_rect = score_name.get_rect()
    score_name_rect.centerx = width / 2
    score_name_rect.centery = 20
    score_value = ResInit.font_45.render(f'{SceneCreate.Map.score}', True, (252, 167, 27), None)
    score_value_rect = score_value.get_rect()
    score_value_rect.centerx = width / 2
    score_value_rect.centery = 60
    ResInit.screen.blit(score_name, score_name_rect)
    ResInit.screen.blit(score_value, score_value_rect)

    pygame.display.update()

    # 设置最大帧率为 60
    FPS_clock.tick(60)
