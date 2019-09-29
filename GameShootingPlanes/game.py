import pygame
import random
from pygame.locals import *
import time

local_url = "/Users/qiushili/PythonFullStackProjects/SecondWeek"

class Plane(object):
    def __init__(self, screen):
        self.x = 200
        self.y = 400
        self.screen = screen
        self.image = pygame.image.load(local_url + "/images/me.png")
        self.bullet_list = []  # 用于存放玩家的子弹列表

    def display(self):
        for b in self.bullet_list:
            b.display()
            if b.move():
                self.bullet_list.remove(b)
        self.screen.blit(self.image, (self.x, self.y))

    def left_move(self):
        self.x -= 5
        self.x = max(self.x, 0)

    def right_move(self):
        self.x += 5
        self.x = min(self.x, 406)

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))
        print(len(self.bullet_list))


class Bullet(object):
    def __init__(self, screen, x, y, att='f'):
        self.x = x + 53
        self.y = y
        self.screen = screen
        self.image = pygame.image.load(local_url + "/images/pd.png")
        self.att = att  # 'f': hero, 'e': enemy
        return

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        return

    def move(self):
        if self.att == 'f':
            self.y -= 10
            if self.y <= -20:
                return True

        if self.att == 'e':
            self.y += 10
            if self.y >= 600:
                return True

        self.display()

        return False


class EnemyPlane(object):
    def __init__(self, screen):
        self.x = random.choice(range(408))
        self.y = -75
        self.screen = screen
        self.type = random.choice(range(3))
        self.image = pygame.image.load(local_url + "/images/e" + str(self.type) + ".png")

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self, plane, screen):
        self.y += 4
        bullet = []
        # 不同飞机不同子弹频率
        if self.type == 0 and self.y % 9 == 0:
            bullet.append(Bullet(screen, self.x - 2, self.y + 55, att='e'))

        if self.type == 1 and self.y % 13 == 0:
            bullet.append(Bullet(screen, self.x - 2, self.y + 55, att='e'))

        if self.type == 2 and random.choice(range(10)) == 5:
            bullet.append(Bullet(screen, self.x - 2, self.y + 55, att='e'))

        # 超出屏幕则删除对象
        if self.y > 568:
            return True, bullet

        for i in plane.bullet_list:
            if i.x > self.x + 12 and i.x < self.x + 92 and i.y > self.y + 20 and i.y < self.y + 60:
                plane.bullet_list.remove(i)
                display_boom(self.screen, i.x, i.y)
                return True, bullet

        return False, bullet


def display_boom(screen, x, y):
    image_boom1 = pygame.image.load(local_url + "/images/bomb1.png")
    image_boom2 = pygame.image.load(local_url + "/images/bomb2.png")
    image_boom3 = pygame.image.load(local_url + "/images/bomb3.png")
    image_boom4 = pygame.image.load(local_url + "/images/bomb4.png")

    for i in [image_boom1, image_boom2, image_boom3, image_boom4]:
        screen.blit(i, (x - 12, y))
        time.sleep(0.01)

def key_control(plane):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit()")
            exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT] or pressed_keys[K_a]:
        print("Left...")
        plane.left_move()

    elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
        print("Right...")
        plane.right_move()

    if pressed_keys[K_SPACE]:
        print("space...")
        plane.fire()


def main():
    '''主函数'''
    # 创建窗口
    screen = pygame.display.set_mode((512, 568), 0, 0)
    background = pygame.image.load(local_url + "/images/bg2.jpg")

    #创建飞机
    plane = Plane(screen)

    m = -968
    enemy_list = []
    bullet_list = []

    while True:
        screen.blit(background, (0, m))
        m += 2
        if m >= -200:
            m = -968

        plane.display()
        key_control(plane)

        if random.choice(range(50)) == 10:
            enemy_list.append(EnemyPlane(screen))

        for i in enemy_list:
            i.display()
            stat, bullet = i.move(plane, screen)
            bullet_list = bullet_list + bullet

            if stat:
                enemy_list.remove(i)

        for j in bullet_list:
            j.move()
            if j.x > plane.x + 12 and j.x < plane.x + 92 and j.y > plane.y + 20 and j.y < plane.y + 60:
                display_boom(screen, j.x, j.y)
                exit()  # 主机被击中 游戏结束
                bullet_list.remove(j)

        pygame.display.update()
        time.sleep(0.04)

if __name__ == "__main__":
    main()