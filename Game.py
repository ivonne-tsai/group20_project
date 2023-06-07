import pygame
from pygame.locals import *
import copy

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((1050, 550))

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

# 定义按钮类
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

class Enemy:
    def __init__(self,path):
        self.path=path
        self.current_pos=0
        self.color=white
        self.speed=0.025

    def move(self):
        if self.current_pos<len(self.path)-1:
            self.current_pos+=self.speed
        else:
            enemies.remove(self)
            row,col=self.path[int(self.current_pos)]
            map1[row][col]=7
            

    def draw(self):
        row,col=self.path[int(self.current_pos)]
        x=map_x+col*map_size
        y=map_y+row*map_size
        pygame.draw.rect(screen,self.color,(x,y,map_size,map_size))

# 计算按钮大小和位置
button_width=(140-3*10)//2
button_height=(550-6*10)//5

# 创建按钮
start_button=Button(525-button_width ,275-button_height//2 ,button_width*2 ,button_height ,"Start",36)
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
#map1 = [[0 for x in range(30)] for y in range(15)]
initial_map =  [
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
map1=initial_map

# 定义变量
selected_button=None
map_size=30
map_x=150
map_y=100

def generate_path(map_data):
    path=[]
    for row in range(len(map_data)):
        for col in range(len(map_data[0])):
            if map_data[row][col]==1:
                path.append((row,col))
    return path

# 绘制地图
def draw_map():
    # 绘制地图
    for row in range(15):
        for col in range(30):
            x=map_x+col*map_size
            y=map_y+row*map_size
            if map1[row][col]==0:
                color=cyan
            elif map1[row][col]==1:
                color=brown
            elif map1[row][col]==3:
                color=green
            elif map1[row][col]==4:
                color=black
            elif map1[row][col]==5:
                color=gray
            elif map1[row][col]==6:
                color=yellow
            elif map1[row][col]==9:
                color=red
            elif map1[row][col]==7:
                color=(255,192,203)
            pygame.draw.rect(screen,color,(x,y,map_size,map_size))
            pygame.draw.rect(screen,black,(x,y,map_size,map_size),1)

# define the path for the enemy
path=generate_path(map1)

# create an instance of the Enemy class
enemies=[]

# 绘制鼠标指针
def draw_pointer():
    global selected_button

    if selected_button is not None:
        x,y=pygame.mouse.get_pos()
        font=pygame.font.Font(None,24)
        text=font.render(selected_button.text,True,black)
        screen.blit(text,(x,y))

# 绘制第一个界面
def draw_first_screen():
    screen.fill((200,200,200))
    start_button.draw()
    pygame.display.update()

def add_enemy():
    global enemies
    if len(enemies)<10:
        new_enemy=Enemy(path)
        enemies.append(new_enemy)
    else:
        pygame.time.set_timer(add_enemy_event, 0) # 禁用定時器事件

# 绘制第二个界面
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
    pygame.display.update()
#繪製結束界面
def draw_end_screen():
    screen.fill((255,255,255))
    pygame.display.update()
#繪製暫停界面
def draw_pause_screen():
    screen.fill((0,0,0))
    continue_button.draw()
    quit_button.draw()
    restart_button.draw()
    pygame.display.update()

add_enemy_event = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy_event, 2500) # 每隔2.5秒觸發一次事件

clock = pygame.time.Clock()
start=False
# 主循环
while True:
    # 获取事件
    pause=False
    #未暫停
    restart=False
    #未重新開始
    while start==False:
        for event in pygame.event.get():
            draw_first_screen()
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                x,y=event.pos
                if start_button.rect.collidepoint(x,y):
                    map1 = copy.deepcopy(initial_map)
                    button_i.text="t1"
                    button_j.text="t2"
                    button_k.text="t3"
                    button_l.text="t4"
                    draw_second_screen()
                    start=True
                    break

    for event in pygame.event.get():
        #判斷是否退出界面
        if event.type == QUIT:
            pygame.quit()
            exit()
        # 判断鼠标点击事件
        elif event.type == MOUSEBUTTONDOWN:
            # 判断鼠标是否在按钮范围内
            # 获取鼠标位置
            x,y=event.pos
            if delete_button.rect.collidepoint(x,y):
                selected_button = delete_button
            elif pause_button.rect.collidepoint(x,y):
                pause=True
            elif button1.rect.collidepoint(x,y):
                button_i.text="t1"
                button_j.text="t2"
                button_k.text="t3"
                button_l.text="t4"
                draw_second_screen()
            elif button2.rect.collidepoint(x,y):
                button_i.text="t5"
                button_j.text="t6"
                button_k.text="t7"
                button_l.text="t8"
                draw_second_screen()
            elif button_i.rect.collidepoint(x,y):
                selected_button=button_i
            elif button_j.rect.collidepoint(x,y):
                selected_button=button_j
            elif button_k.rect.collidepoint(x,y):
                selected_button=button_k
            elif button_l.rect.collidepoint(x,y):
                selected_button=button_l
            else:
                col=(x -map_x) //map_size
                row=(y -map_y) //map_size
                if 0 <=col <30 and 0 <=row <15 and map1[row][col] not in [1, 9]:
                    if selected_button == delete_button:
                        map1[row][col] = 0
                        selected_button = None
                        draw_second_screen()
                    elif selected_button is not None:
                        if map1[row][col] == 0: # check if the position is land (represented by the value 0)
                            if selected_button == button_i and button_i.text == "t1":
                                map1[row][col] = 3
                                selected_button = None
                                draw_second_screen()
                            elif selected_button == button_j and button_j.text == "t2":
                                map1[row][col] = 4
                                selected_button = None
                                draw_second_screen()
                            elif selected_button == button_k and button_k.text == "t3":
                                map1[row][col] = 5
                                selected_button = None
                                draw_second_screen()
                            elif selected_button == button_l and button_l.text == "t4":
                                map1[row][col] = 6
                                selected_button = None
                                draw_second_screen()
                            elif map1[row][col] == 5:
                                map1[row][col] = 0
                            else:
                                map1[row][col]=8
                                selected_button=None
                                draw_second_screen()
        elif event.type == add_enemy_event:
            add_enemy()
    while pause==True:
        draw_pause_screen()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                x,y=event.pos
                if continue_button.rect.collidepoint(x,y):
                    pause=False
                    break
                elif restart_button.rect.collidepoint(x,y):
                    pause=False
                    restart=True
                    break
                elif quit_button.rect.collidepoint(x,y):
                    pygame.quit()
                    exit()

    if restart==True:
        enemies=[]
        continue
    clock.tick(60)
    for enemy in enemies:
        enemy.move()
    draw_second_screen()
    pygame.display.update()

    # 更新屏幕
    if selected_button is not None:
        draw_second_screen()
 

