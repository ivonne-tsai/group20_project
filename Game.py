import pygame
import copy
import random
import math
import os
import sys

pygame.init()

# 设置颜色
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
gray = (128, 128, 128)
cyan = (0, 255, 255)
brown = (165, 42, 42)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
pink = (255, 192, 203) 

# 定义变量
# Set font
font = pygame.font.Font(None, 36)
selected_button=None
map_size=30
map_x=150
map_y=100
button_width=55    
button_height=98
enemies=[]  # create an instance of the Enemy class
bullets = []
player_health = 100
player_money = 500  # Starting amount of money for the player
total_enemies=0
timer = 0

# 設置螢幕大小和標題
screen_width = 1050
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tower Defense")

# 定義按鈕類
class Button:
    def __init__(self, x, y, w, h, text, text_size=24):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.text_size = text_size

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)
        font = pygame.font.Font(None,self.text_size)
        text=font.render(self.text,True ,black)
        text_rect=text.get_rect(center=self.rect.center)
        screen.blit(text,text_rect)

# 定义炮塔类
class Tower:
    def __init__(self,x,y,w,h,text,text_size=24):
        self.rect=pygame.Rect(x,y,w,h)
        self.text=text
        self.text_size=text_size

    def draw(self):
        pygame.draw.rect(screen ,white ,self.rect)
        font=pygame.font.Font(None,self.text_size)
        text=font.render(self.text,True ,black)
        text_rect=text.get_rect(center=self.rect.center)
        screen.blit(text,text_rect)

    def shoot(self):
        global timer
        timer += 1
        # Check if enough time has passed since the tower last shot a bullet
        #if self.shoot_timer <= 0:
            # 初始化變量以跟踪最近的敵人及其與塔的距離
        nearest_enemy = None
        nearest_distance = float('inf')
        for enemy in enemies:
            # 獲取敵人當前位置
            row,col=enemy.path[int(enemy.current_pos)]
            x=map_x+col*map_size
            y=map_y+row*map_size
            # 計算塔和敵人之間的距離
            distance = math.sqrt((self.rect.centerx - x) ** 2 + (self.rect.centery - y) ** 2)
            # 檢查這個敵人是否比當前最近的敵人更近
            if distance < nearest_distance:
                # 更新最近的敵人及其距離
                nearest_distance = distance
                nearest_enemy = enemy

        # 檢查是否找到最近的敵人
        if nearest_enemy is not None:
            if timer % 50 == 0:
            # 獲取最近敵人的位置
                row,col=nearest_enemy.path[int(nearest_enemy.current_pos)]
                x=map_x+col*map_size
                y=map_y+row*map_size
            # 計算從塔到最近敵人的方向
                direction = (x - self.rect.centerx, y - self.rect.centery)
                direction_length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
                direction = (direction[0] / direction_length, direction[1] / direction_length)
            # 創建一顆瞄準最近敵人方向的新子彈
                bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
            # 將新的項目符號添加到項目符號列表中
                bullets.append(bullet)
        
class Enemy:
    def __init__(self,path):
        self.path=path
        self.current_pos=0
        self.color=white
        self.speed=0.025
        self.health = 10
        self.max_health = 10

    def move(self):
        global player_health

        if self.current_pos<len(self.path)-1:
            self.current_pos+=self.speed
        else:
            enemies.remove(self)
            row,col=self.path[int(self.current_pos)]
            map_now[row][col]=7

            # Decrease player health
            player_health -= self.max_health
            
    def draw(self):
        row,col=self.path[int(self.current_pos)]
        x=map_x+col*map_size
        y=map_y+row*map_size
        pygame.draw.rect(screen,self.color,(x,y,map_size,map_size))
    
    def draw_health_bar(self):
        # 設置健康條的大小和位置
        bar_width = map_size
        bar_height = 5
        row,col=self.path[int(self.current_pos)]
        x=map_x+col*map_size
        y=map_y+row*map_size - 10
        
        # 設置健康條的大小和位置
        fill_width = int(bar_width * (self.health / self.max_health))
        # 繪製血條背景
        pygame.draw.rect(screen, red, (x, y, bar_width, bar_height))
        # 繪製健康條的填充部分
        pygame.draw.rect(screen, green, (x, y, fill_width, bar_height))

class Bullet:
    def __init__(self, x, y, direction):
        # 設置子彈的初始位置和方向
        self.x = x
        self.y = y
        self.direction = direction
        # 設置子彈的速度和傷害
        self.speed = 1 # 調整這個值來改變子彈的速度
        self.damage = 1 # 調整這個值來改變子彈的傷害

    def update(self):
        # 調整這個值來改變子彈的傷害
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

    def draw(self):
        # 在屏幕上將子彈畫成一個黑色的小圓圈
        pygame.draw.circle(screen, black, (int(self.x), int(self.y)), 3)

# 创建按钮
game_1_button=Button(105,200,210,100,"game 1")
game_2_button=Button(420,200,210,100,"game 2")
game_3_button=Button(735,200,210,100,"game 3")
button1=Button(140+10 ,0 ,button_width*2 ,button_height/2 ,"1")
button2=Button(140+10 ,button_height/2 ,button_width*2 ,button_height/2 ,"2")
button_i=Tower(10 ,10 ,140-25 ,button_height ,"t1")
button_j=Tower(10 ,button_height +20 ,140-25 ,button_height ,"t2")
button_k=Tower(10 ,button_height *2 +30 ,140-25 ,button_height ,"t3")
button_l=Tower(10 ,button_height *3 +40 ,140-25 ,button_height ,"t4")
delete_button=Button(10 ,550-button_height -10 ,button_width ,button_height ,"delete")
pause_button=Button(70 ,550-button_height -10 ,button_width ,button_height ,"pause")
continue_button=Button(105,200,210,100,"continue")
quit_button=Button(420,200,210,100,"quit")
restart_button=Button(735,200,210,100,"restart")

# 创建地图
first_map =  [
           [9,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
           [9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
           [9,9,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #5
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #6
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #7
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #10
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #11
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #12
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,9,9], #13
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9], #14
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,9]  #15
        ]
second_map =  [
           [9,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
           [9,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
           [9,9,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
           [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
           [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #5
           [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #6
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #7
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #8
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #9
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0], #10
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], #11
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], #12
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,9,9], #13
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,9], #14
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,9]  #15
        ]
third_map =  [
           [9,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
           [9,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #2
           [9,9,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #3
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #4
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #5
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #6
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0], #7
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], #8
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], #9
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], #10
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], #11
           [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], #12
           [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,9,9], #13
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,9], #14
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,9]  #15
        ]

# get the road
def generate_path(map_data):
    path=[(1,1)]
    row_change=0
    column_change=0
    while path[-1] != (13,28):
        row,column=path[-1]
        if map_data[row][column+1]==1 and column_change!=-1:
            column+=1
            column_change=1
            row_change=0
        elif map_data[row][column-1]==1 and column_change!=1:
            column-=1
            column_change=1
            row_change=0
        elif map_data[row+1][column]==1 and row_change!=-1:
            row+=1
            row_change=1
            column_change=0
        elif map_data[row-1][column]==1 and row_change!=1:
            row-=1
            row_change=-1
            column_change=0
        path.append((row,column))
    return path

# 绘制地图
def draw_map():
    # 绘制地图
    for row in range(15):
        for col in range(30):
            x=map_x+col*map_size
            y=map_y+row*map_size
            if map_now[row][col]==0:
                color=cyan
            elif map_now[row][col]==1:
                color=brown
            elif map_now[row][col]==3:
                color=green
            elif map_now[row][col]==4:
                color=black
            elif map_now[row][col]==5:
                color=gray
            elif map_now[row][col]==6:
                color=yellow
            elif map_now[row][col]==9:
                color=red
            elif map_now[row][col]==7:
                color=(255,192,203)
            pygame.draw.rect(screen,color,(x,y,map_size,map_size))
            pygame.draw.rect(screen,black,(x,y,map_size,map_size),1)

# 绘制鼠标指针
def draw_pointer():
    global selected_button
    if selected_button is not None:
        x,y=pygame.mouse.get_pos()
        font=pygame.font.Font(None,24)
        text=font.render(selected_button.text,True,black)
        screen.blit(text,(x,y))

def add_enemy():
    global enemies
    global total_enemies

    if len(enemies)<10 and total_enemies<10:
        new_enemy=Enemy(path)
        enemies.append(new_enemy)
        total_enemies +=1
    else:
        pygame.time.set_timer(add_enemy_event, 0) # 禁用定時器事件

# 繪製第一個界面
def draw_first_screen():
    screen.fill((200,200,200))
    game_1_button.draw()
    game_2_button.draw()
    game_3_button.draw()
    pygame.display.update()

# 繪製第二個界面
def draw_second_screen():
    screen.fill((200,200,200))
    pygame.draw.line(screen ,black ,(140 ,0) ,(140 ,550) ,10)
    button1.draw()
    button2.draw()
    button_i.draw()
    button_j.draw()
    button_k.draw()
    button_l.draw()
    delete_button.draw()
    pause_button.draw()
    draw_map()
    draw_pointer()
    for enemy in enemies:
        enemy.draw()
        enemy.draw_health_bar()  # Draw the health bar for each enemy
    # Draw HP and Money
    draw_hp_money()
    pygame.display.update()

def draw_hp_money():
    # Set the font size
    font_size = 36
    # Draw the rectangle
    pygame.draw.rect(screen, white, (840, 0, 210, 100))

    # Render the text
    font = pygame.font.Font(None, font_size)
    hp_text = font.render(f"HP: {player_health}", True, black)
    money_text = font.render(f"Money: {player_money}", True, black)
    
    # Calculate the position of the text
    hp_text_x = 840  + 15
    hp_text_y = 20
    money_text_x = 840 + 15
    money_text_y = 60

    # Draw the text on the screen
    screen.blit(hp_text, (hp_text_x, hp_text_y))
    screen.blit(money_text, (money_text_x, money_text_y))

#繪製暫停界面
def draw_pause_screen():
    screen.fill((0,0,0))
    continue_button.draw()
    quit_button.draw()
    restart_button.draw()
    pygame.display.update()

#繪製結束界面
def draw_end_screen():
    screen.fill((0,0,0))
    quit_button.draw()
    restart_button.draw()
    pygame.display.update()

add_enemy_event = pygame.USEREVENT + 1
bullets_event = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy_event, 1500) # 每隔2.5秒觸發一次事件
pygame.time.set_timer(bullets_event, 3000) # 每隔2.5秒觸發一次事件
clock = pygame.time.Clock()

start=False
def main():
    #global current_screen
    current_screen = 1
    global start             # 用 global 來 更新 外部同名變量的值
    global selected_button
    global map_now
    global rmap
    global enemies
    global player_health
    global player_money
    global path
    global total_enemies

    while True:
        # 获取事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标位置
                x,y=event.pos
                if current_screen == 1:
                    if game_1_button.rect.collidepoint(x,y):
                        current_screen = 2
                        map_now=first_map
                        path=generate_path(map_now)
                        map_now = copy.deepcopy(first_map)    #刷新地圖
                        rmap = copy.deepcopy(first_map)
                        enemies = []
                        total_enemies =0
                        selected_button = None              #    鼠標
                    if game_2_button.rect.collidepoint(x,y):
                        current_screen = 2
                        map_now=second_map
                        path=generate_path(map_now)
                        map_now = copy.deepcopy(second_map) 
                        rmap = copy.deepcopy(second_map) 
                        enemies = []
                        total_enemies =0
                        total_enemies = 0
                        selected_button = None              
                    if game_3_button.rect.collidepoint(x,y):
                        current_screen = 2
                        map_now=third_map
                        path=generate_path(map_now)
                        map_now = copy.deepcopy(third_map) 
                        rmap = copy.deepcopy(third_map)
                        enemies = []
                        total_enemies =0
                        selected_button = None             
                elif current_screen == 2:
                    if pause_button.rect.collidepoint(x,y):
                        current_screen = 3
                    elif button1.rect.collidepoint(x,y):
                        selected_button=None
                        button_i.text="t1"
                        button_j.text="t2"
                        button_k.text="t3"
                        button_l.text="t4"
                        draw_second_screen()
                    elif button2.rect.collidepoint(x,y):
                        selected_button=None
                        button_i.text="t5"
                        button_j.text="t6"
                        button_k.text="t7"
                        button_l.text="t8"
                        draw_second_screen()
                    elif button_i.rect.collidepoint(x,y):
                        selected_button = button_i
                    elif button_j.rect.collidepoint(x,y):
                        selected_button = button_j
                    elif button_k.rect.collidepoint(x,y):
                        selected_button = button_k
                    elif button_l.rect.collidepoint(x,y):
                        selected_button = button_l
                    elif delete_button.rect.collidepoint(x,y):
                        selected_button = delete_button
                    else:
                        col=(x -map_x) //map_size
                        row=(y -map_y) //map_size
                        if 0 <=col <30 and 0 <=row <15 and map_now[row][col] not in [1, 9]:
                            if selected_button == delete_button:
                                map_now[row][col] = 0
                                selected_button = None
                                draw_second_screen()
                            elif selected_button is not None:
                                if map_now[row][col] == 0: # check if the position is land (represented by the value 0)
                                    if selected_button == button_i and button_i.text == "t1":
                                        if player_money >= 50:
                                            map_now[row][col] = 3
                                            selected_button = None
                                            player_money-=50
                                            draw_second_screen()
                                    elif selected_button == button_j and button_j.text == "t2":
                                        if player_money >= 50:
                                            map_now[row][col] = 4
                                            selected_button = None
                                            player_money-=50
                                            draw_second_screen()
                                    elif selected_button == button_k and button_k.text == "t3":
                                        if player_money >= 50:
                                            map_now[row][col] = 5
                                            selected_button = None
                                            player_money-=50
                                            draw_second_screen()
                                    elif selected_button == button_l and button_l.text == "t4":
                                        if player_money >= 50:
                                            map_now[row][col] = 6
                                            selected_button = None
                                            player_money-=50
                                            draw_second_screen()
                                    elif map_now[row][col] == 5:
                                            map_now[row][col] = 0
                                    else:
                                        map_now[row][col]=8
                                        selected_button=None
                                        draw_second_screen()
                #elif current_screen == 3 or current_screen == 4:
                elif current_screen == 3:
                    if quit_button.rect.collidepoint(x,y):
                        current_screen = 1
                    elif continue_button.rect.collidepoint(x,y):
                        current_screen = 2
                        selected_button = None
                    elif restart_button.rect.collidepoint(x,y):
                        current_screen = 2
                        map_now = copy.deepcopy(rmap)
                        enemies = []
                        total_enemies =0
                        player_health = 100 # reset player health to initial value 
                        player_money = 500
                        selected_button = None
                        pygame.time.set_timer(add_enemy_event, 1500)  # 重新啟用定時器事件
                elif current_screen == 4:
                    if quit_button.rect.collidepoint(x,y):
                        current_screen = 1
                    elif restart_button.rect.collidepoint(x,y):
                        current_screen = 2
                        map_now = copy.deepcopy(rmap)
                        enemies = []
                        total_enemies =0
                        player_health = 100 # reset player health to initial value 
                        player_money = 500
                        selected_button = None
                        pygame.time.set_timer(add_enemy_event, 1500)  # 重新啟用定時器事件

                        
                    

            elif current_screen==2 and event.type == add_enemy_event:
                add_enemy()
             
        # Check player health and update screen accordingly 
        if player_health <= 0:
            current_screen = 4

        # 更新塔和子彈
        if current_screen == 2:
            # 遍歷地圖上的所有位置
            for row in range(15):
                for col in range(30):
                    # 檢查這個位置是否有塔
                    if map_now[row][col] in [3, 4, 5, 6]:
                        x=map_x+col*map_size 
                        y=map_y+row*map_size
                        # 在這個位置創建一個臨時的 Tower 對象 
                        tower=Tower(x,y,map_size,map_size,"")
                        tower.shoot()

            # 遍歷所有子彈
            for bullet in bullets[:]:
                # 更新子彈的位置
                bullet.update()
                # 檢查與敵人的碰撞
                for enemy in enemies[:]:
                    # 獲取敵人的位置
                    row,col=enemy.path[int(enemy.current_pos)]
                    x=map_x+col*map_size
                    y=map_y+row*map_size
                    # 檢查子彈是否靠近敵人
                    if math.sqrt((bullet.x - x) ** 2 + (bullet.y - y) ** 2) < map_size / 2:
                        enemy.health -= bullet.damage # Subtract the damage of the bullet from the health of the enemy
                        bullets.remove(bullet)
                        # 檢查敵人的生命值是否達到 0 或以下
                        if enemy.health <= 0:
                            # 從遊戲中移除敵人
                            enemies.remove(enemy)
                            player_money += 10  # Increase the player's money by 10 when an enemy is defeated
                        break
                else:
                    # 檢查子彈是否移出屏幕
                    #if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
                    if bullet.x < 150 or bullet.x > 1050  or bullet.y < 100 or bullet.y > 550:
                        # 從遊戲中移除子彈
                        bullets.remove(bullet)


        # Draw screen
        if current_screen == 1:
            draw_first_screen()
        elif current_screen == 2:
            draw_second_screen()
            for enemy in enemies:
                enemy.move()
            for bullet in bullets:
                bullet.draw()
        elif current_screen == 3:
            draw_pause_screen()
        elif current_screen == 4:
            draw_end_screen()

        clock.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    main()

    # 更新屏幕
    if selected_button is not None:
        draw_second_screen()
