# 202130440811 - 赖言安 - 华南理工大学网络工程
# 方块类

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *
from pygame.sprite import Group

import ResInit

pygame.init()

# 普通平台类
class BlockBrick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ResInit.Block_Brick_Medium_Aqua
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.rect.width = 256
        self.rect.height = 16
        self.vx = 0
        self.vy = 0
        self.f = 0
        self.frame = 0
        self.first_frame = 0
        self.last_frame = 3
        self.last_time = 0

    # 更新坐标
    def updateXY(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y

# 金色平台类
# 灯火 >= 50% : 移动速度 +50
# 灯火 < 50% : 移动速度 -50
class BlockBrickGolden(BlockBrick):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = ResInit.Block_Brick_Medium_Golden
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 256
        self.rect.height = 16

# 紫色平台类
# vy 反弹
class BlockBrickPurple(BlockBrick):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = ResInit.Block_Brick_Medium_Purple
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 256
        self.rect.height = 24

# 火把类
class BlockTorch(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.master_image = ResInit.Block_Torch
        self.rect = self.master_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.rect.width = 20
        self.rect.height = 50
        self.vx = 0
        self.vy = 0
        self.f = 0
        self.frame = 0
        self.first_frame = 1
        self.old_frame = -1
        self.last_frame = 4
        self.columns = 5
        self.last_time = 0
        self.frame_width = 20
        self.frame_height = 50
        self.isIgnited = True

    def update(self, current_time, FPS=60):
        self.current_time = current_time
        if self.current_time > self.last_time + FPS * 5 and self.isIgnited:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = self.current_time
        
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            # 新的帧
            frame_rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(frame_rect)
            self.old_frame = self.frame

        return super().update()
    
    # 更新坐标
    def updateXY(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y