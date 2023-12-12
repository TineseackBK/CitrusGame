# 202130440811 - 赖言安 - 华南理工大学网络工程
# 背景类

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *
import math

import ResInit
import SceneCreate

pygame.init()

size = width, height = 1280, 720
FPS = 60

# 背景会根据沙糖桔的位置运动
# 第 0 层背景移动最慢，第 1 层中等，第 3 层最快
# 第 2 层和第 4 层不移动

# 背景类
class Background(pygame.sprite.Sprite):
    def __init__(self, img, x, y, id):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.old_x = x
        self.frame = 0
        self.old_frame = -1
        self.first_frame = 0
        self.last_frame = 0
        self.current_time = 0
        self.last_time = 0

        self.background_id = id

    def update(self, current_time):
        self.current_time = current_time

        # 根据屏幕 1/3 处相对地图左侧的位移，计算每一层的位移
        # 只有沙糖桔在特定区域内才会触发
        # 第 0 层：0.2 倍
        # 第 1 层：0.5 倍
        # 第 3 层：1 倍
        map_x = SceneCreate.map.rect.x
        citrus_x = SceneCreate.citrus.rect.x
        if citrus_x <= int(width * (1/3)) or citrus_x >= int(width * (1/2)):
            delta_x = width * (1/3) - map_x
            factor = 0
            if self.background_id == 0:
                factor = 0.2
            if self.background_id == 1:
                factor = 0.5
            if self.background_id == 3:
                factor = 1
            
            self.rect.x = self.old_x - delta_x * factor

            # 如果当前最右侧超出了窗口左边缘，就放到右边去
            # 左侧同理
            if self.background_id == 0 or self.background_id == 1 or self.background_id == 3:
                if self.rect.right < 0:
                    self.rect.x = 1280
                    self.old_x += 1280 * 2
                if self.rect.left > 1280:
                    self.rect.x = -1280
                    self.old_x -= 1280 * 2

    