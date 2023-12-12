# 202130440811 - 赖言安 - 华南理工大学网络工程
# UI 类

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *
import math

import ResInit
import SceneCreate
import Map

pygame.init()

size = width, height = 1280, 720
FPS = 60
font = pygame.font.Font('asset/font/ark-pixel-12px-monospaced-zh_cn.otf', 30)

# UI 类
class UI(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = img
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.x = x
        self.rect.y = y
        self.frame = 0
        self.old_frame = -1
        self.first_frame = 0
        self.last_frame = 0
        self.current_time = 0
        self.last_time = 0

    def update(self, current_time):
        self.current_time = current_time

# UI-技能类
class UISkill(UI):
    def __init__(self, img, x, y, id):
        super().__init__(img, x, y)
        self.master_image = img
        self.frame_width = 64
        self.frame_height = 64
        self.rect = self.master_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 192
        self.rect.height = 64
        self.columns = 3
        tmp_rect = self.master_image.get_rect()
        self.last_frame = (tmp_rect.width // self.frame_width) * (tmp_rect.height // self.frame_height) - 1

        # 辨识技能编号
        self.skill_id = id

    def update(self, current_time):
        self.current_time = current_time

        # 更新技能图标
        self.SkillCDIn()

        return super().update(current_time)
    
    def SkillCDIn(self):
        # 技能 1：缓降
        if self.skill_id == 1:
            # 技能持续时：
            # 技能图标转换为橙色
            # 技能持续时间显示在图标上
            if SceneCreate.citrus.du_sf > 0:
                self.frame = 1
                skill_du_text = font.render(str(round(SceneCreate.citrus.du_sf/FPS, 1))+'s', True, (255, 255, 255), None)
                ResInit.screen.blit(skill_du_text, (1200, 90))

            # 技能冷却时：
            # 技能图标转换为灰色
            # 技能 CD 显示在图标上
            if SceneCreate.citrus.cd_sf > 0:
                self.frame = 2
                skill_cd_text = font.render(str(round(SceneCreate.citrus.cd_sf/FPS, 1))+'s', True, (255, 255, 255), None)
                ResInit.screen.blit(skill_cd_text, (1200, 90))

            # 技能冷却结束后：
            # 技能图标恢复彩色
            # 删除技能 CD 显示
            if SceneCreate.citrus.du_sf == 0 and SceneCreate.citrus.cd_sf == 0:
                self.frame = 0
                skill_key_text = font.render('[LS]', True, (255, 255, 255), None)
                ResInit.screen.blit(skill_key_text, (1199, 90))

        # 技能 2：向上冲刺
        if self.skill_id == 2:
            # 技能持续时：
            # 技能图标转换为橙色
            # 技能持续时间显示在图标上
            if SceneCreate.citrus.du_du > 0:
                self.frame = 1
                skill_du_text = font.render(str(round(SceneCreate.citrus.du_du/FPS, 1))+'s', True, (255, 255, 255), None)
                ResInit.screen.blit(skill_du_text, (1096, 90))

            # 技能冷却时：
            # 技能图标转换为灰色
            # 技能 CD 显示在图标上
            if SceneCreate.citrus.cd_du > 0:
                self.frame = 2
                skill_cd_text = font.render(str(round(SceneCreate.citrus.cd_du/FPS, 1))+'s', True, (255, 255, 255), None)
                ResInit.screen.blit(skill_cd_text, (1096, 90))

            # 技能冷却结束后：
            # 技能图标恢复彩色
            # 删除技能 CD 显示
            if SceneCreate.citrus.du_du == 0 and SceneCreate.citrus.cd_du == 0:
                self.frame = 0
                skill_key_text = font.render('[SPACE]', True, (255, 255, 255), None)
                ResInit.screen.blit(skill_key_text, (1076, 90))

        # 更改贴图
        if self.frame > self.last_frame:
            self.frame = self.first_frame
        
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            # 新的帧
            frame_rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(frame_rect)
            self.old_frame = self.frame

# UI——屏幕显示类
class UIDisplay(UI):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# UI——蜡烛侧边栏类
class UICandleBar(UI):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.master_image = img
        self.frame_width = 64
        self.frame_height = 180
        self.rect = self.master_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 1092
        self.rect.height = 180
        self.columns = 17
        tmp_rect = self.master_image.get_rect()
        self.last_frame = (tmp_rect.width // self.frame_width) * (tmp_rect.height // self.frame_height) - 1

    def update(self, current_time):
        fuel_value = SceneCreate.citrus.fuel_value

        self.frame = 16 - math.ceil(fuel_value / 600)

        # 更改贴图
        if self.frame > self.last_frame:
            self.frame = self.first_frame
        
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            # 新的帧
            frame_rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(frame_rect)
            self.old_frame = self.frame

        self.remainDisplay()

        return super().update(current_time)
    
    # 剩余燃料百分比显示
    def remainDisplay(self):
        fuel_value = SceneCreate.citrus.fuel_value
        fuel_remain = int(round((fuel_value / 9600), 2) * 100)
        fuel_remain_text = font.render(str(fuel_remain)+'%', True, (255, 255, 255), None)
        ResInit.screen.blit(fuel_remain_text, (1208, 455))

# UI——按钮类
class UIButton(UI):
    def __init__(self, img, x, y, text, color):
        super().__init__(img, x, y)
        self.color = color
        self.button_text = font.render(text, True, self.color , None)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height // 2
        self.x = x
        self.y = y
        self.player_is_dead = False

    def update(self, current_time):
        # 重开按钮
        if self.player_is_dead:
            self.button_text = font.render(f'你死了!\n你的分数是 {Map.score}\n点我重新开始', True, self.color, None)
            self.rect_text = self.button_text.get_rect()
            self.rect_text.centerx = width // 2
            self.rect_text.centery = height // 2
            ResInit.screen.blit(self.image, self.rect)
            ResInit.screen.blit(self.button_text, self.rect_text)
        return super().update(current_time)