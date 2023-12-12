# 202130440811 - 赖言安 - 华南理工大学网络工程
# 地图类

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *
import math
import pandas as pd

from pygame.sprite import Group

import ResInit
import SceneCreate

pygame.init()

size = width, height = 1280, 720
FPS = 60

# 分数，基于移动的最大距离
score = 0

# 地图类
class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        map_img = pygame.Surface((2160, 720), pygame.SRCALPHA)
        self.image = map_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.old_x = 0
        self.delta_x_max = 0

    def update(self):

        # 地图滚动
        self.mapRoll()

        # 下一个区块读取
        self.chunkLoad()

        return super().update()

    # 地图滚动
    def mapRoll(self):
        role_x = SceneCreate.citrus.rect.x
        
        # 在左侧 1/3 的时候，向左滚动
        # 在右侧 1/2 的时候，向右滚动
        if role_x < width * (1/3):
            if self.rect.x < 0:
                self.rect.x += width * (1/3) - role_x
                SceneCreate.citrus.rect.x = width * (1/3)
            else:
                self.rect.x = 0
        elif role_x >= width * (1/2):
            self.rect.x -= role_x - width * (1/2)
            SceneCreate.citrus.rect.x = width * (1/2)

        for block in SceneCreate.block_group.sprites():
            block.updateXY(block.x + self.rect.x, block.y)

    # 下一个区块读取
    # 初始会读取 chunk_0 和 chunk_1 两个区块，偏移量分别为 0 和 1280
    # 此后，每当沙糖桔相对地图左端移动 1280，就读取下一个的区块
    def chunkLoad(self):
        role_x = SceneCreate.citrus.rect.x
        delta_x = role_x - self.rect.x
        self.delta_x_max = max(delta_x, self.delta_x_max)

        # 分数机制
        global score
        score = self.delta_x_max - 60

        if self.delta_x_max % 1280 > 1277 or self.delta_x_max % 1280 < 3:
            chunk_data_path = SceneCreate.chunkSelect()
            chunk_data = pd.read_csv(chunk_data_path)
            SceneCreate.chunkLoad(chunk_data, 1280)
            self.delta_x_max += 6