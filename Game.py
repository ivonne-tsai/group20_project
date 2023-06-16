import pygame
import copy
import math
import os

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
font = pygame.font.Font(None, 36)
selected_button=None
map_size=30
map_x=150
map_y=100
button_width=55    
button_height=80
enemies=[]  # create an instance of the Enemy class
bullets = []
player_health = 100
player_money = 500  # Starting amount of money for the player
total_enemies=0
timer = 0
wave = 1
waves = 1
max_enemies = 1
enemiesSpawned = 0
spawnInterval = 2 # 敵人生成之間的秒數
max_health = 10
health = 10

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
    def __init__(self,x,y,w,h,speed,damage,text,text_size=24):
        self.rect=pygame.Rect(x,y,w,h)
        self.text=text
        self.text_size=text_size
        self.speed = speed
        self.damage = damage
        self.range = range

    def draw(self):
        pygame.draw.rect(screen ,white ,self.rect)
        font=pygame.font.Font(None,self.text_size)
        text=font.render(self.text,True ,red)
        text_rect=text.get_rect(center=self.rect.center)
        screen.blit(text,text_rect)

    def shoot(self):
        global timer
        timer += 1
        # Check if enough time has passed since the tower last shot a bullet
        if timer % (100 // self.speed) == 0:
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
                #if nearest_distance>150:
                #    nearest_enemy=None

            # 檢查是否找到最近的敵人
            if nearest_enemy is not None:
                # 獲取最近敵人的位置
                row,col=nearest_enemy.path[int(nearest_enemy.current_pos)]
                x=map_x+col*map_size
                y=map_y+row*map_size
                # 計算從塔到最近敵人的方向
                direction = (x - self.rect.centerx, y - self.rect.centery)
                direction_length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
                direction = (direction[0] / direction_length, direction[1] / direction_length)
                if nearest_distance < 200:
                    # 創建一顆瞄準最近敵人方向的新子彈
                    bullet = Bullet(self.rect.centerx, self.rect.centery, direction,speed,damage)
                    bullet.damage = self.damage
                    # 將新的項目符號添加到項目符號列表中
                    bullets.append(bullet)
        
class Enemy:
    def __init__(self,path):
        self.path=path
        self.current_pos=0
        self.color=purple
        self.speed=0.025
        self.max_health = 10
        self.health = self.max_health

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
    def __init__(self, x, y, direction,speed,damage):
        # 設置子彈的初始位置和方向
        self.x = x
        self.y = y
        self.direction = direction
        # 設置子彈的速度和傷害
        self.speed = speed # 調整這個值來改變子彈的速度
        self.damage = damage # 調整這個值來改變子彈的傷害

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
button1=Button(150 ,0 ,button_width*2 ,button_height/2 ,"1")
button2=Button(150 ,button_height/2 ,button_width*2 ,button_height/2 ,"2")
button_i=Tower(10 ,10 ,115 ,button_height , 1, 1, "t1")
button_j=Tower(10 ,button_height +35 ,115 ,button_height , 1, 2, "t2")
button_k=Tower(10 ,button_height*3 -25,115 ,button_height ,1, 3, "t3")
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
           [9,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0], #2
           [9,9,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #3
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #4
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #5
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #6
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #7
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #8
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #9
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #10
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #11
           [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #12
           [0,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,9,9], #13
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
            if map_now[row][col]==0:  # 0 land
                color=cyan
            elif map_now[row][col]==1:  # 1 road
                color=white
            elif map_now[row][col]==2:   #t1,t4
                color=yellow
            elif map_now[row][col]==3:   #t2,t5
                color=pink
            elif map_now[row][col]==4:   #t3,t6
                color=green
            elif map_now[row][col]==5:   # 5 enemies
                color=purple
            elif map_now[row][col]==9:   # 9 start/end
                color=black
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

lastSpawnTime = 0
waveInterval = 10
totalEnemiesSpawned = 0

#出現敵人
def add_enemy(enemies,max_enemies,health,max_health,wave,waves,enemiesSpawned,lastSpawnTime,totalEnemiesSpawned):
    if totalEnemiesSpawned < max_enemies:
        # 計算上一次生成敵人後經過的時間
        timeSinceLastSpawn = (pygame.time.get_ticks() - lastSpawnTime) / 1000

        # 檢查是否該生成敵人
        if (enemiesSpawned == 0 and timeSinceLastSpawn >= waveInterval) or (enemiesSpawned > 0 and timeSinceLastSpawn >= spawnInterval):
            # 更新上一次生成敵人的時間
            lastSpawnTime = pygame.time.get_ticks()
            # 設置敵人的血量
            max_health = health + (wave - 1) * 10

            # 使用 Enemy 類在指定的生成點生成敵人
            enemy = Enemy(path)
            enemy.health = max_health
            enemy.max_health = max_health
            enemies.append(enemy)

            enemiesSpawned += 1
            totalEnemiesSpawned += 1

            # 檢查是否該進入下一波
            if (enemiesSpawned == max_enemies//waves ):
                wave += 1
                enemiesSpawned = 0


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
    delete_button.draw()
    pause_button.draw()
    draw_map()
    draw_pointer()
    for enemy in enemies:
        enemy.draw()
        enemy.draw_health_bar()  # Draw the health bar for each enemy
    # Draw HP and Money
    update_state()

    font_size = 24
    font = pygame.font.Font(None, font_size)

    i_text = font.render("50", True, black)
    j_text = font.render("100", True, black)
    k_text = font.render("150", True, black)
    screen.blit(i_text, (60, 90))
    screen.blit(j_text, (52, 195))
    screen.blit(k_text, (52, 295))

    pygame.display.update()

def update_state():
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

    # 計算已經出現的敵人數量、當前波數和百分比
    #spawned_enemies = totalEnemiesSpawned

    if wave<waves:
        current_wave = wave
    else:
        current_wave = waves
    # = spawned_enemies / max_enemies * 100

    # 在屏幕上顯示信息
    font = pygame.font.Font(None, 36)
    text = font.render(f"Enemies: {totalEnemiesSpawned}/{max_enemies} (Wave {current_wave})", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen_width // 2
    text_rect.top = 10
    screen.blit(text, text_rect)

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
spawn_interval = 2000 # 以毫秒為單位
wave_interval = 10000 # 以毫秒為單位
pygame.time.set_timer(bullets_event, 1000) # 每隔2.5秒觸發一次事件
clock = pygame.time.Clock()

def main():
    # 用 global 來 更新 外部同名變量的值
    current_screen = 1
    global selected_button,map_now,rmap,enemies,player_health,player_money,path,total_enemies,speed,damage,max_enemies,waves,bullet,current_wave,totalEnemiesSpawned

    while True:
        # 获取事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标位置
                x,y=event.pos
                if current_screen == 1:
                    if game_1_button.rect.collidepoint(x,y):
                        map_now=first_map
                        path=generate_path(map_now)
                        map_now = copy.deepcopy(first_map)    #刷新地圖
                        rmap = copy.deepcopy(first_map)
                        max_enemies = 15
                        waves = 3
                    if game_2_button.rect.collidepoint(x,y):
                        map_now=second_map
                        path=generate_path(map_now)
                        map_now = copy.deepcopy(second_map) 
                        rmap = copy.deepcopy(second_map)
                        max_enemies = 30
                        waves = 3
                    if game_3_button.rect.collidepoint(x,y):
                        map_now=third_map
                        path=generate_path(map_now)
                        map_now = copy.deepcopy(third_map) 
                        rmap = copy.deepcopy(third_map)
                        max_enemies = 50
                        waves = 5
                    current_screen = 2
                    enemies = []
                    total_enemies =0
                    player_money = 500
                    current_wave = 1
                    totalEnemiesSpawned = 0
                    selected_button = None
                    # 開始生成敵人
                    pygame.time.set_timer(add_enemy_event, spawn_interval)          
                elif current_screen == 2:
                    if pause_button.rect.collidepoint(x,y):
                        current_screen = 3
                    elif button1.rect.collidepoint(x,y):
                        selected_button=None
                        button_i.text="t1"
                        button_j.text="t2"
                        button_k.text="t3"
                        draw_second_screen()
                    elif button2.rect.collidepoint(x,y):
                        selected_button=None
                        button_i.text="t4"
                        button_j.text="t5"
                        button_k.text="t6"
                        draw_second_screen()
                    elif button_i.rect.collidepoint(x,y):
                        selected_button = button_i
                    elif button_j.rect.collidepoint(x,y):
                        selected_button = button_j
                    elif button_k.rect.collidepoint(x,y):
                        selected_button = button_k
                    elif delete_button.rect.collidepoint(x,y):
                        selected_button = delete_button
                    else:
                        col=(x -map_x) //map_size
                        row=(y -map_y) //map_size
                        if 0 <=col <30 and 0 <=row <15 and map_now[row][col] not in [1, 9]:
                            if selected_button == delete_button:
                                if map_now[row][col] == 2:
                                    player_money+=25
                                if map_now[row][col] == 3:
                                    player_money+=50
                                if map_now[row][col] == 4:
                                    player_money+=75
                                map_now[row][col] = 0
                                selected_button = None
                                draw_second_screen()
                            elif selected_button is not None:
                                if map_now[row][col] == 0: # check if the position is land (represented by the value 0)
                                    #if selected_button == button_i and button_i.text == "t1":
                                    if selected_button == button_i:
                                        if button_i.text == "t1" or button_i.text == "t4":
                                            if player_money >= 50:
                                                map_now[row][col] = 2
                                                selected_button = None
                                                player_money-=50
                                                draw_second_screen()
                                    elif selected_button == button_j: 
                                        if button_j.text == "t2" or button_j.text == "t5":
                                            if player_money >= 100:
                                                map_now[row][col] = 3
                                                selected_button = None
                                                player_money-=100
                                                draw_second_screen()
                                    elif selected_button == button_k:
                                        if button_k.text == "t3" or button_k.text == "t6":
                                            if player_money >= 150:
                                                map_now[row][col] = 4
                                                selected_button = None
                                                player_money-=150
                                                draw_second_screen()
                                    else:
                                        map_now[row][col]=5
                                        selected_button=None
                                        draw_second_screen()
                elif current_screen == 3 or current_screen == 4:
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
                        player_money = 500
                        current_wave = 1
                        totalEnemiesSpawned = 0
                        selected_button = None
                        pygame.time.set_timer(add_enemy_event, 1500)  # 重新啟用定時器事件
                    player_health = 100 # reset player health to initial value 
            elif current_screen==2 and event.type == add_enemy_event:
                add_enemy(enemies,max_enemies,health,max_health,wave,waves,enemiesSpawned,lastSpawnTime,totalEnemiesSpawned)
             
        # Check player health and update screen accordingly 
        if player_health <= 0:
            current_screen = 4

        # 更新塔和子彈
        if current_screen == 2:
            # 遍歷地圖上的所有位置
            for row in range(15):
                for col in range(30):
                    # 檢查這個位置是否有塔
                    if map_now[row][col] in [2, 3, 4]:
                        x=map_x+col*map_size 
                        y=map_y+row*map_size
                        # 在這個位置創建一個臨時的 Tower 對象 
                        if map_now[row][col] == 2:
                            speed = 1
                            damage = 1
                        elif map_now[row][col] == 3:
                            speed = 3
                            damage = 3
                        elif map_now[row][col] == 4:
                            speed = 5
                            damage = 5
                        tower=Tower(x,y,map_size,map_size,speed, damage,"")
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
                    if bullet.x < 150 or bullet.x > 1050  or bullet.y < 100 or bullet.y > 550:
                        # 從遊戲中移除子彈
                        bullets.remove(bullet)
                    if restart_button.rect.collidepoint(x,y):
                        bullets.remove(bullet)
                    elif game_1_button.rect.collidepoint(x,y):
                        bullets.remove(bullet)
                    elif game_2_button.rect.collidepoint(x,y):
                        bullets.remove(bullet)
                    elif game_3_button.rect.collidepoint(x,y):
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
