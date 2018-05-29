#coding=utf-8
import pygame,sys
from pygame.locals import *
import random
size=width,height=480,600
#子弹类：
class Bullet(pygame.sprite.Sprite):
    """docstring for Bullet"""
    def __init__(self, bullet_img,init_pos):
#        super(Bullet, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_img
        self.rect=self.image.get_rect()
        self.rect.midbottom=init_pos
        self.speed=4
    def move(self):
            self.rect.top -= self.speed
#敌机类：
class Enemy(pygame.sprite.Sprite):
    """docstring for ClassName"""
    def __init__(self,enemy_img,enemy_down_imgs,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect=self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs=enemy_down_imgs
        self.speed=2
        self.down_index=0
    #敌机移动，边界判断及其删除在游戏主循环里处理
    def move(self):
        self.rect.top+=self.speed

#玩家飞机类：
class Player(pygame.sprite.Sprite):
    """docstring for Player"""
    def __init__(self,player_img, player_rect,init_pos):
        self.image = []
        for i in player_rect:
            self.image.append(plane_img.subsurface(i).convert_alpha())
        #for i in range(len(player_rect)):
        #    self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]#初始化图片所在矩形
        self.rect.topleft = init_pos#初始化矩形左上角坐标
        self.img_index=0#玩家飞机图片索引
        self.speed=2#初始化玩家飞机速度
        self.bullets=pygame.sprite.Group()
    #射击
    def shoot(self,bullet_img):
        bullet=Bullet(bullet_img,self.rect.midtop)
        self.bullets.add(bullet)
    #向上移动
    def moveUp(self):
        if self.rect.top<=0:
            self.rect.top=0
        else:
            self.rect=self.rect.move(0,-self.speed)
    #向下移动
    def moveDown(self):
        if self.rect.bottom>=height:
            self.rect.bottom=height
        else:
            self.rect=self.rect.move(0,self.speed)
    #向右移动
    def moveRight(self):
        if self.rect.right>=width:
            self.rect.right=width
        else:
            self.rect=self.rect.move(self.speed,0)
    #向左移动
    def moveLeft(self):
        if self.rect.left<=0:
            self.rect.left=0
        else:
            self.rect=self.rect.move(-self.speed,0)






#______main______
#1. 初始化 pygame
pygame.init()
pygame.mixer.init()
#2. 设置游戏界面大小、背景图片及标题
# 游戏界面像素大小

screen = pygame.display.set_mode(size)
# 游戏循环帧率设置
clock = pygame.time.Clock()
# 游戏界面标题
pygame.display.set_caption('飞机大战')
# 背景图
background = pygame.image.load('resources/image/background.png').convert()
# Game Over 的背景图
game_over = pygame.image.load('resources/image/gameover.png')
# 飞机图片
plane_img = pygame.image.load('resources/image/shoot.png')
# 对玩家进行设置,不同状态的图片
player_rect=[]
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360,102,126))
player_rect.append(pygame.Rect(165, 234,102,126))
player_rect.append(pygame.Rect(330, 624,102,126))
player_rect.append(pygame.Rect(330, 498,102,126))
player_rect.append(pygame.Rect(432, 624,102,126))
player_pos=[200,480]
player=Player(plane_img,player_rect,player_pos)
ticks=1
ticks_a=60
#设置子弹
bullet_rect=pygame.Rect(69, 78, 9, 21)
bullet_img=plane_img.subsurface(bullet_rect)
shoot_frequency = 1
#设置敌机图片
enemy1_rect=pygame.Rect(534,612,57,43)
enemy1_img=plane_img.subsurface(enemy1_rect)
#设置敌机死掉之后的图片
enemy1_down_imgs=[]
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267,347,57,43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873,697,57,43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267,296,57,43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930,697,57,43)))

enemies1=pygame.sprite.Group()
#存储被击毁的飞机，用来做击毁动画
enemies_down=pygame.sprite.Group()

#音乐
pygame.mixer.music.load('music/KNOW.mp3')
pygame.mixer.music.play(-1,12.0)

running=True
score=0
enemy_frequency=0
#3. 游戏主循环内需要处理游戏界面的初始化、更新及退出
while running:
    # 控制游戏最大帧率为 60
    clock.tick(60)
    # 初始化游戏屏幕
    screen.fill(0)
    screen.blit(background, (0, 0))
    # 显示玩家飞机在位置[200,600]
    if ticks%ticks_a<(ticks_a/2):
        screen.blit(player.image[0],player.rect)
    else:
        screen.blit(player.image[1],player.rect)
    #飞机喷气动画
    ticks+=1

    #产生敌机频率与位置
    if enemy_frequency%50==0:
        #??????
        enemy1_pos=[random.randint(0,width-enemy1_rect.width),0]
        enemy1=Enemy(enemy1_img,enemy1_down_imgs,enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency+=1
    if enemy_frequency>=200:
        enemy_frequency=0
    #移动敌机
    for enemy in enemies1:
        enemy.move()
        if enemy.rect.top<0:
            enemies1.remove(enemy)
    #获取键盘事件，玩家的上下左右移动
    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.moveUp()
            #player2.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
            #player2.moveDown()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()
            #player2.moveRight()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
            #player2.moveLeft()
    #发射子弹，子弹超过边界时删除
    # if key_pressed[K_SPACE]:
    #     if shoot_frequency % 15 == 0:
    #         player.shoot(bullet_img)
    #     shoot_frequency += 1
    #     print shoot_frequency
    #     if shoot_frequency >= 15:
            # shoot_frequency = 0
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom<0:
            player.bullets.remove(bullet)
    #敌机被子弹击中
    enemies1_down=pygame.sprite.groupcollide(enemies1,player.bullets,1,1)
    for i in enemies1_down:
        enemies_down.add(i)
    #敌机被击中后动画
    for enemy_down in enemies_down:
        if enemy_down.down_index==0:
            pass
        if enemy_down.down_index>7:
            enemies_down.remove(enemy_down)
            # enemy_down.down_index=0
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index//2],enemy_down.rect)
        enemy_down.down_index+=1
    # 显示子弹
    player.bullets.draw(screen)
    # 显示敌机
    enemies1.draw(screen)
    # 更新游戏屏幕----更新屏幕一定要在draw之前
    pygame.display.update()
    # 游戏退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_SPACE:
                player.shoot(bullet_img)
            if event.key==pygame.K_q:
                player.speed+=1
                print player.speed
                ticks_a-=4
                if ticks_a<=20:
                    ticks_a=20
            if event.key==pygame.K_e:
                player.speed-=1
                ticks_a+=4
                if ticks_a>=70:
                    ticks_a=70
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                sys.exit()