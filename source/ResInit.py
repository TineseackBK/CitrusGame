# 202130440811 - 赖言安 - 华南理工大学网络工程
# 资源初始化

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *

pygame.init()

# 字体初始化
font = pygame.font.Font('asset/font/ark-pixel-12px-monospaced-zh_cn.otf', 30)
font_45 = pygame.font.Font('asset/font/ark-pixel-12px-monospaced-zh_cn.otf', 45)

size = width, height = 1280, 720

# 创建窗口
screen = pygame.display.set_mode(size)
pygame.display.set_caption('沙糖桔的大冒险 β-0.1')
icon = pygame.image.load('asset/CitrusGame.ico').convert_alpha()
pygame.display.set_icon(icon)

Avatar_Citrus_Idle = pygame.image.load('asset/Avatar_Citrus_Idle.png').convert_alpha()
Avatar_Citrus_Move = pygame.image.load('asset/Avatar_Citrus_Move.png').convert_alpha()
Avatar_Citrus_Falling = pygame.image.load('asset/Avatar_Citrus_Falling.png').convert_alpha()
Avatar_Citrus_Slow_Falling = pygame.image.load('asset/Avatar_Citrus_Slow_Falling.png').convert_alpha()
Avatar_Citrus_Dash_Upwards = pygame.image.load('asset/Avatar_Citrus_Dash_Upwards.png').convert_alpha()
Block_Ground = pygame.image.load('asset/Block_Ground.png').convert_alpha()
Block_Brick_Medium_Aqua = pygame.image.load('asset/Block_Brick_Medium_Aqua.png').convert_alpha()
Block_Brick_Medium_Golden = pygame.image.load('asset/Block_Brick_Medium_Golden.png').convert_alpha()
Block_Brick_Medium_Purple = pygame.image.load('asset/Block_Brick_Medium_Purple.png').convert_alpha()
Block_Torch = pygame.image.load('asset/Block_Torch.png').convert_alpha()

UI_Background_0 = pygame.image.load('asset/Background_0.png').convert_alpha()
UI_Background_1 = pygame.image.load('asset/Background_1.png').convert_alpha()
UI_Background_2 = pygame.image.load('asset/Background_2.png').convert_alpha()
UI_Background_3 = pygame.image.load('asset/Background_3.png').convert_alpha()
UI_Background_4 = pygame.image.load('asset/Background_4.png').convert_alpha()
UI_Background_4.set_alpha(204)
UI_Foreground_Dark = pygame.image.load('asset/Foreground_Dark.png').convert_alpha()
UI_Foreground_Dark.set_alpha(0)
UI_Display = pygame.image.load('asset/UI_Display.png').convert_alpha()
UI_Candle_Bar = pygame.image.load('asset/UI_Candle_Bar.png').convert_alpha()
UI_Mission_Failed = pygame.image.load('asset/UI_Mission_Failed.png').convert_alpha()

Skill_SlowFalling = pygame.image.load('asset/Skill_SlowFalling.png').convert_alpha()
Skill_DashUpwards = pygame.image.load('asset/Skill_DashUpwards.png').convert_alpha()

Buff_Speed_Up = pygame.image.load('asset/Buff_Speed_Up.png').convert_alpha()
Buff_Speed_Down = pygame.image.load('asset/Buff_Speed_Down.png').convert_alpha()
