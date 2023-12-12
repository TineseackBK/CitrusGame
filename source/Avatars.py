# 202130440811 - 赖言安 - 华南理工大学网络工程
# 角色类

from typing import Any
import pygame
import sys
import pygame.sprite
from pygame.locals import *

import ResInit

pygame.init()

FPS = 60
size = width, height = 1280, 720
g = 0.2

# 砂糖桔类
class AvatarCitrus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.master_image = ResInit.Avatar_Citrus_Idle
        self.rect = self.master_image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 64
        self.rect.height = 56
        self.vx = 0
        self.vy = 0
        self.speed_bonus = 0 # float，速度 +30 等于 0.3
        self.f = 0
        self.facing = 'right'
        self.frame_width = 64
        self.frame_height = 56
        self.frame = 0
        self.first_frame = 0
        self.old_frame = -1
        self.last_frame = 3
        self.columns = 4
        self.current_time = 0
        self.last_time = 0
        self.coyote_time = 0
        self.coyote_time_end = 0.25 * FPS
        # 是否按下过跳跃键
        self.jumped = False
        # 为 0 时，可进行一段跳
        # 为 1 时，可进行二段跳
        # 为 -1 时，不可进行跳跃
        self.jump_count = 0
        # 仅用于土狼时间超时后锁定跳跃
        self.can_jump = True
        # 是否下落中
        self.is_falling = False
        # 燃料值为 0 时死亡
        self.fuel_value = 160 * FPS
        self.is_dead = False
        # 是否按下过 LShift 键
        self.slowed = False
        # 是否按下过空格键
        self.dashed = False
        # 是否可以无视地形
        self.ghosted = False
        # 碰到平台是否反弹
        self.rebound_y = False
        
        self.skillInit()

    # 技能初始化
    def skillInit(self):
        self.cd_sf = 0
        self.du_sf = 0
        self.cd_du = 0
        self.du_du = 0

    def update(self, current_time):
        # 燃料值
        self.fuel()

        # 死亡检测
        self.deathDetect()

        # 动画显示
        self.current_time = current_time
        if self.current_time > self.last_time + FPS * 5 and not self.is_dead:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = self.current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            frame_rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            
            # Alpha 遮罩
            alpha_mask = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            alpha_value = self.fuelToAlpha()
            alpha_mask.set_alpha(alpha_value)

            # Idle
            if self.vx == 0 and not self.is_falling:
                self.master_image = ResInit.Avatar_Citrus_Idle

            # Move
            if self.vx != 0 and not self.is_falling:
                self.master_image = ResInit.Avatar_Citrus_Move

            # Falling
            if self.is_falling and self.vy > 0:
                self.master_image = ResInit.Avatar_Citrus_Falling

            # Slow Falling
            if self.is_falling and self.vy > 0 and self.du_sf > 0:
                self.master_image = ResInit.Avatar_Citrus_Slow_Falling

            # Dash Upwards
            if self.ghosted and self.du_du > 0:
                self.master_image = ResInit.Avatar_Citrus_Dash_Upwards
                # Alpha 值强制设定为 32
                alpha_mask.set_alpha(128)

            # 分左右处理
            if self.facing == 'right':
                image = self.master_image.subsurface(frame_rect)
            elif self.facing == 'left':
                image = self.master_image.subsurface(frame_rect)
                image = pygame.transform.flip(image, True, False)

            alpha_mask.blit(image, (0, 0))
            self.image = alpha_mask

            self.old_frame = self.frame

        # 速度加成检测
        self.speedBonusDetect()
        
        # 位移，检测碰撞
        self.vy += g - self.f
        self.vx = self.vx * (1 + self.speed_bonus)
        self.rect.x += self.vx
        self.collision_x()
        self.rect.y += self.vy
        self.collision_y()

        self.vx = 0
        self.f = 0

        # 上下边界可相互传送，但需要消耗 200 点燃料
        if self.rect.bottom < 0:
            self.rect.y = height
            self.fuel_value -= 200
        if self.rect.top > height:
            self.rect.y = -56
            self.fuel_value -= 200
        if self.rect.right > width:
            self.rect.x = width-64
            self.vx = 0
        if self.rect.left < 0:
            self.rect.x = 0
            self.vx = 0

        # 状态机：检测下落
        self.is_falling = self.isFalling()

        # 土狼时间
        self.coyoteTime()

        # 技能 CD 倒计时
        self.skillCD()

        # 技能持续时间倒计时
        self.skillDuration()

        # 持续释放的技能
        self.skillContinuous()
    
    # 判断是否下落中
    # 首先把角色向下移 1 像素，判断是否有碰撞，如果没有，那就是在下落。最后上移 1 像素恢复
    def isFalling(self):
        import SceneCreate
        self.rect.y += 1
        falling_group = pygame.sprite.Group(SceneCreate.block_brick_group)

        if pygame.sprite.spritecollideany(self, falling_group):
            # 落地后，可以进行下一次跳跃，并且下一次跳跃是一段跳
            self.can_jump = True
            self.jump_count = 0
            self.rect.y -= 1
            return False
        else:
            self.rect.y -= 1
            return True
        
    # 土狼时间 250ms = 15gt
    # 当 self.coyote_time 设置为 0，才开始判断土狼时间
    # 该设置和 self.adjust_coordinate_y() 函数有关
    # 该设置还和是否二段跳有关，如果进行了二段跳，那么一定开启土狼时间判断
    def coyoteTime(self):
        # 如果已经进行了一段跳，jump_count 为 1，将不进行土狼时间判断
        # 只有 jump_count 为 0 的时候才开始判断
        if self.is_falling and self.coyote_time >= 0 and self.jump_count == 0:
            self.coyote_time += 1
        if self.coyote_time == self.coyote_time_end:
            if not self.jumped:
                self.jump_count = 0
        if self.coyote_time > self.coyote_time_end:
            # 如果超过土狼时间，锁定跳跃
            self.can_jump = False
            self.coyote_time = -1

    # 速度加成检测
    def speedBonusDetect(self):
        import SceneCreate
        self.speed_bonus = 0
        self.rebound_y = False
        speed_type = ''

        # 金色砖块类
        # 灯火 >= 50% : 移动速度 +50
        # 灯火 < 50% : 移动速度 -50
        if not self.is_falling:
            self.rect.y += 1
            golden_group = pygame.sprite.Group(SceneCreate.block_brick_golden_group)

            if pygame.sprite.spritecollideany(self, golden_group):
                if self.fuel_value in range(4800, 9601):
                    self.speed_bonus = 0.5
                    speed_type = 'Up'
                elif self.fuel_value in range(0, 4800):
                    self.speed_bonus = -0.5
                    speed_type = 'Down'
            self.rect.y -= 1

        # 紫色砖块类
        # vy 反弹
        # 写在 self.collision_y() 里了

        # 头顶移速标志
        if speed_type == 'Up':
            speed_icon = ResInit.Buff_Speed_Up
            ResInit.screen.blit(speed_icon, (self.rect.centerx - 12, self.rect.centery - 62))
        elif speed_type == 'Down':
            speed_icon = ResInit.Buff_Speed_Down
            ResInit.screen.blit(speed_icon, (self.rect.centerx - 12, self.rect.centery - 62))
        
    # 技能 CD 倒计时
    def skillCD(self):
        # 缓降
        self.cd_sf -= 1
        if self.cd_sf < 0:
            self.cd_sf = 0

        # 向上冲刺
        self.cd_du -= 1
        if self.cd_du < 0:
            self.cd_du = 0

    # 技能持续时间倒计时
    def skillDuration(self):
        # 缓降
        if self.du_sf == 1:
            self.cd_sf = 600
        self.du_sf -= 1
        if self.du_sf < 0:
            self.du_sf = 0

        # 向上冲刺
        if self.du_du == 1:
            self.cd_du = 1200
            self.ghosted = False
        self.du_du -= 1
        if self.du_du < 0:
            self.du_du = 0

    # 持续释放的技能
    def skillContinuous(self):
        # 缓降
        if self.vy > 0 and self.du_sf > 0:
            self.f = 0.15

        # 向上冲刺
        if self.du_du > 0:
            self.ghosted = True
            if self.vy > 0:
                self.ghosted = False

    # 键盘操作
    def moveUp(self):
        # 一段跳
        if self.can_jump and not self.jumped and self.jump_count == 0:
            self.vy = -7
            self.jumped = True
            self.jump_count += 1
            self.fuel_value -= 10
        # 二段跳
        if self.can_jump and not self.jumped and self.jump_count == 1:
            self.vy = -5
            self.jumped = True
            self.jump_count = 0
            self.fuel_value -= 10
            self.coyote_time = 0

    def moveUpJumping(self):
        self.jumped = False

    def moveLeft(self):
        self.vx = -3
        self.facing = 'left'
        self.fuel_value -= 1
    
    def moveRight(self):
        self.vx = 3
        self.facing = 'right'
        self.fuel_value -= 1

    # 技能：缓降
    # CD：10s
    # 持续：5s
    # 消耗：250 燃料
    def slowFalling(self):
        if self.cd_sf == 0 and not self.slowed:
            self.du_sf = 300
            self.slowed = True
            self.fuel_value -= 250

    def slowFallingPressed(self):
        if self.du_sf <= 0:
            self.slowed = False

    # 技能：向上冲刺
    # CD：20s
    # 持续：1s 持续时间内可无视地形移动
    # 消耗：750 燃料
    def dashUpwards(self):
        if self.cd_du == 0 and not self.dashed:
            self.du_du = 60
            self.dashed = True
            self.vy = -12
            self.fuel_value -= 750

    def dashUpwardsPressed(self):
        if self.du_du <= 0:    
            self.dashed = False

    # 香薰燃烧机制
    # 燃料值上限 160(9600)，燃料值为 0 时死亡
    # 每一刻，如果是主动进行移动，燃料值减少 1
    # 每一刻，如果是主动进行跳跃，燃料值减少 10（二段跳同样）
    # 每一刻，如果开启了缓降技能，燃料值减少 250
    def fuel(self):
        if self.fuel_value <= 0:
            self.is_dead = True

    # 死亡检测
    def deathDetect(self):
        if self.is_dead:
            # 强制无法移动，无法释放技能
            self.vx = 0
            self.vy = 0
            self.cd_sf = 0
            self.du_sf = 0
            self.cd_du = 0
            self.du_du = 0
            self.fuel_value = 0

    # 根据当前燃料值计算 Alpha 值
    def fuelToAlpha(self):
        # 燃料 0-9600
        # Alpha 0-255
        return int(self.fuel_value / 9600 * 255)

    # 碰撞检测
    def collision_x(self):
        import SceneCreate

        # 如果位于幽灵状态，在持续时间时直接无视碰撞
        if self.ghosted:
            return

        colli_block_brick = pygame.sprite.spritecollideany(self, SceneCreate.block_brick_group)
        colli_block_torch = pygame.sprite.spritecollide(self, SceneCreate.block_torch_group, False)
       
        # 碰到砖块
        if colli_block_brick:
            self.adjust_coordinate_x(colli_block_brick)
        # 碰到火把加燃料值
        # 燃料值 + 1000
        if len(colli_block_torch) > 0:
            if colli_block_torch[0].isIgnited:
                self.fuel_value += 1000
            if self.fuel_value > 9600:
                self.fuel_value = 9600
            for torch in colli_block_torch:
                torch.frame = 0
                torch.isIgnited = False

    def collision_y(self):
        import SceneCreate
        
        # 如果位于幽灵状态，在持续时间时直接无视碰撞
        if self.ghosted:
            return
        
        colli_block_brick = pygame.sprite.spritecollideany(self, SceneCreate.block_brick_group)
        colli_block_brick_purple = pygame.sprite.spritecollideany(self, SceneCreate.block_brick_purple_group)

        # 碰到紫色砖块
        if colli_block_brick_purple:
            self.rebound_y = True

        # 碰到砖块
        if colli_block_brick:
            self.adjust_coordinate_y(colli_block_brick)

    def adjust_coordinate_x(self, collider):
        # 左侧
        if self.rect.x < collider.rect.x:
            self.rect.right = collider.rect.left
        # 右侧
        else:
            self.rect.left = collider.rect.right

    def adjust_coordinate_y(self, collider):
        # 下方
        if self.rect.top > collider.rect.top:
            self.rect.top = collider.rect.bottom
            self.vy = 0
        # 上方
        else:
            self.rect.bottom = collider.rect.top
            # 如果踩到的是紫色平台，反弹速度，关闭土狼时间判断
            # 可以在空中进行一段跳和二段跳
            if self.rebound_y:
                self.vy = -self.vy
                self.coyote_time = -1
                self.jump_count = 0
            # 如果踩到的是其他平台，速度清零，开启土狼时间判断
            else:
                self.vy = 0
                self.coyote_time = 0

    def reset(self):
        self.rect.x = 60
        self.rect.y = 444
        self.cd_sf = 0
        self.du_sf = 0
        self.cd_du = 0
        self.du_du = 0
        self.fuel_value = 160 * FPS
        self.is_dead = False