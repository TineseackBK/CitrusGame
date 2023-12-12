# 202130440811 - 赖言安 - 华南理工大学网络工程
# 屏幕上的各种元素以及组的创建

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *
import pandas as pd
import random

import ResInit
import Block
import UI
import Background
import Map
import Avatars

pygame.init()

# 已加载的区块数量
chunks = 0

# 创建组
avatar_group = pygame.sprite.Group()
map_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
block_brick_group = pygame.sprite.Group()
block_brick_normal_group = pygame.sprite.Group()
block_brick_golden_group = pygame.sprite.Group()
block_brick_purple_group = pygame.sprite.Group()
block_torch_group = pygame.sprite.Group()
ui_group = pygame.sprite.Group()
ui_background_group = pygame.sprite.Group()
ui_foreground_group = pygame.sprite.Group()
ui_button_group = pygame.sprite.Group()
ui_skill_group = pygame.sprite.Group()

# 区块选取
# 前两个区块必定为 level_0/chunk_0.csv 和 level_0/chunk_1.csv
# chunks 在 [0, 10] 的时候，从 level_0 中选取
# chunks 在 [11, +∞) 的时候，从 level_0, level_1 中选取
# （暂时去掉）chunks 在 [11, 20] 的时候，从 level_0, level_1 中选取
# （暂时去掉）chunks 在 [21, +∞) 的时候，从 level_0, level_1, level_2 中选取
def chunkSelect():
    global chunks
    level = ''
    chunk_data_path = ''

    if chunks in range(0, 11):
        level = 'level_0'
    
    if chunks > 10:
        level_id = str(random.randint(0, 1))
        level = f'level_{level_id}'
    
    # if chunks > 20:
    #     level_id = str(random.randint(0, 1, 2))
    #     level = f'level_{level_id}'

    chunk_id = str(random.randint(0, 9))
    chunk_data_path = f'map_data/{level}/chunk_{chunk_id}.csv'

    return chunk_data_path

# 区块加载
def chunkLoad(map_data, offset_x=0):
    # map_data 为 .csv 文件，列分别为 index block_x block_y block_type
    # type==0 普通平台
    # type==1 金色平台
    # type==2 紫色平台
    # type==100 火把
    # 可以输入 x 的偏移量，默认为 0
    # 移动中加载后续区块的时候，偏移量为 1280
    global chunks

    for line in range(len(map_data)):
        block_x = map_data.iloc[line, 1]
        block_y = map_data.iloc[line, 2]
        block_type = map_data.iloc[line, 3]

        if block_type == 0:
            new_block = Block.BlockBrick(block_x + offset_x * chunks, block_y)
            block_brick_normal_group.add(new_block)
        if block_type == 1:
            new_block = Block.BlockBrickGolden(block_x + offset_x * chunks, block_y)
            block_brick_golden_group.add(new_block)
        if block_type == 2:
            new_block = Block.BlockBrickPurple(block_x + offset_x * chunks, block_y)
            block_brick_purple_group.add(new_block)
        if block_type == 100:
            new_block = Block.BlockTorch(block_x + offset_x * chunks + 118, block_y - 50)
            block_torch_group.add(new_block)

    # 整合平台和火把为一个组
    block_brick_group.add(
        block_brick_normal_group,
        block_brick_golden_group,
        block_brick_purple_group
    )
    block_group.add(block_brick_group, block_torch_group)
    
    chunks += 1

# 创建砂糖桔
citrus = Avatars.AvatarCitrus(60, 444)
avatar_group.add(citrus)

# 创建地图
map = Map.Map()
map_group.add(map)

# 初始区域加载
chunk_data_path = 'map_data/level_0/chunk_0.csv'
chunk_data = pd.read_csv(chunk_data_path)
chunkLoad(chunk_data)
chunk_data_path = 'map_data/level_0/chunk_1.csv'
chunk_data = pd.read_csv(chunk_data_path)
chunkLoad(chunk_data, 1280)

# 背景
ui_background_0 = Background.Background(ResInit.UI_Background_0, 0, 0, 0)
ui_background_1 = Background.Background(ResInit.UI_Background_1, 0, 0, 1)
ui_background_2 = Background.Background(ResInit.UI_Background_2, 0, 0, 2)
ui_background_3 = Background.Background(ResInit.UI_Background_3, 0, 0, 3)
ui_background_4 = Background.Background(ResInit.UI_Background_4, 0, 0, 4)
ui_background_0_extension = Background.Background(ResInit.UI_Background_0, 1280, 0, 0)
ui_background_1_extension = Background.Background(ResInit.UI_Background_1, 1280, 0, 1)
ui_background_2_extension = Background.Background(ResInit.UI_Background_2, 1280, 0, 2)
ui_background_3_extension = Background.Background(ResInit.UI_Background_3, 1280, 0, 3)
ui_background_4_extension = Background.Background(ResInit.UI_Background_4, 1280, 0, 4)
ui_background_group.add(ui_background_0)
ui_background_group.add(ui_background_0_extension)
ui_background_group.add(ui_background_1)
ui_background_group.add(ui_background_1_extension)
ui_background_group.add(ui_background_2)
ui_background_group.add(ui_background_2_extension)
ui_background_group.add(ui_background_3)
ui_background_group.add(ui_background_3_extension)
ui_background_group.add(ui_background_4)
ui_background_group.add(ui_background_4_extension)

# 前景
ui_foreground_dark = UI.UIDisplay(ResInit.UI_Foreground_Dark, 0, 0)
ui_foreground_group.add(ui_foreground_dark)

# UI
ui_display = UI.UIDisplay(ResInit.UI_Display, 0, 0)
ui_group.add(ui_display)
ui_candle_bar = UI.UICandleBar(ResInit.UI_Candle_Bar, 1196, 270)
ui_group.add(ui_candle_bar)
ui_skill_1 = UI.UISkill(ResInit.Skill_SlowFalling, 1196, 20, 1)
ui_skill_group.add(ui_skill_1)
ui_skill_2 = UI.UISkill(ResInit.Skill_DashUpwards, 1092, 20, 2)
ui_skill_group.add(ui_skill_2)

# 按钮
ui_button_reset = UI.UIButton(ResInit.UI_Mission_Failed, 640, 360, '', (255, 255, 255))
ui_button_group.add(ui_button_reset)

# 场景初始化
def sceneInit():
    # 创建地图
    map = Map.Map()
    map_group.add(map)

    # 初始区域加载
    chunk_data_path = 'map_data/level_0/chunk_0.csv'
    chunk_data = pd.read_csv(chunk_data_path)
    chunkLoad(chunk_data)
    chunk_data_path = 'map_data/level_0/chunk_1.csv'
    chunk_data = pd.read_csv(chunk_data_path)
    chunkLoad(chunk_data, 1280)

    # 背景
    ui_background_0 = Background.Background(ResInit.UI_Background_0, 0, 0, 0)
    ui_background_1 = Background.Background(ResInit.UI_Background_1, 0, 0, 1)
    ui_background_2 = Background.Background(ResInit.UI_Background_2, 0, 0, 2)
    ui_background_3 = Background.Background(ResInit.UI_Background_3, 0, 0, 3)
    ui_background_4 = Background.Background(ResInit.UI_Background_4, 0, 0, 4)
    ui_background_0_extension = Background.Background(ResInit.UI_Background_0, 1280, 0, 0)
    ui_background_1_extension = Background.Background(ResInit.UI_Background_1, 1280, 0, 1)
    ui_background_2_extension = Background.Background(ResInit.UI_Background_2, 1280, 0, 2)
    ui_background_3_extension = Background.Background(ResInit.UI_Background_3, 1280, 0, 3)
    ui_background_4_extension = Background.Background(ResInit.UI_Background_4, 1280, 0, 4)
    ui_background_group.add(ui_background_0)
    ui_background_group.add(ui_background_0_extension)
    ui_background_group.add(ui_background_1)
    ui_background_group.add(ui_background_1_extension)
    ui_background_group.add(ui_background_2)
    ui_background_group.add(ui_background_2_extension)
    ui_background_group.add(ui_background_3)
    ui_background_group.add(ui_background_3_extension)
    ui_background_group.add(ui_background_4)
    ui_background_group.add(ui_background_4_extension)

    # 前景
    ui_foreground_dark = UI.UIDisplay(ResInit.UI_Foreground_Dark, 0, 0)
    ui_foreground_group.add(ui_foreground_dark)

    # UI
    ui_display = UI.UIDisplay(ResInit.UI_Display, 0, 0)
    ui_group.add(ui_display)
    ui_candle_bar = UI.UICandleBar(ResInit.UI_Candle_Bar, 1196, 270)
    ui_group.add(ui_candle_bar)
    ui_skill_1 = UI.UISkill(ResInit.Skill_SlowFalling, 1196, 20, 1)
    ui_skill_group.add(ui_skill_1)
    ui_skill_2 = UI.UISkill(ResInit.Skill_DashUpwards, 1092, 20, 2)
    ui_skill_group.add(ui_skill_2)

# 场景重置
def sceneReset():
    global chunks
    chunks = 0

    for i in map_group.sprites():
        del i
    for i in block_group.sprites():
        del i
    for i in block_brick_group.sprites():
        del i
    for i in block_brick_normal_group.sprites():
        del i
    for i in block_brick_golden_group.sprites():
        del i
    for i in block_brick_purple_group.sprites():
        del i
    for i in block_torch_group.sprites():
        del i
    for i in ui_group.sprites():
        del i
    for i in ui_background_group.sprites():
        del i
    for i in ui_foreground_group.sprites():
        del i
    for i in ui_skill_group.sprites():
        del i
    
    map_group.empty()
    block_group.empty()
    block_brick_group.empty()
    block_brick_normal_group.empty()
    block_brick_golden_group.empty()
    block_brick_purple_group.empty()
    block_torch_group.empty()
    ui_group.empty()
    ui_background_group.empty()
    ui_foreground_group.empty()
    ui_skill_group.empty()

    # 重新调用初始化函数
    sceneInit()