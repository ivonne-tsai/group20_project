import pygame
import sys
import time
import random
import math
import copy
from PIL import Image

screen = pygame.display.set_mode((1500, 750))
background_image = pygame.image.load("bg.jpg")

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

button_width=55    
button_height=80

pygame.font.init()
font = pygame.font.Font(None, 32)

def main():
    game = Game()
    while True:
        game.handle_events()
        if game.current_screen == "start":
            start_screen(screen)
        elif game.current_screen == "game":
            second_screen(screen, game)
        elif game.current_screen == "pause":
            pause_menu(screen)
        elif game.current_screen == "l_w":
            lose_win(screen)
        pygame.display.update()

def start_screen(screen):
    screen.fill(pink)
    
    Map1.draw(screen)
    Map2.draw(screen)
    Map3.draw(screen)

def second_screen(screen, game):
    start_time = time.time()
    while game.current_screen == "game":
        game.handle_events()
        screen.fill(white)
        pygame.draw.line(screen, black, (147, 0), (147, screen.get_height()), 4)
        game.draw_map(screen)
        
        for row,col,tower in game.towers:
            x = 150 + cell_size * col
            y = 75 + cell_size * row
            # 检查炮塔周围是否有敌人
            for enemy_pos in enemies:
                enemy_x = 150 + enemy_pos[0] * cell_size
                enemy_y = 75 + enemy_pos[1] * cell_size
                dx = enemy_x - x
                dy = enemy_y - y
                distance = math.sqrt(dx*dx + dy*dy)
                # 如果有敌人，则发射子弹
                if distance < tower.range:
                    current_time = time.time()
                    if current_time - tower.last_attack_time > tower.attack_speed:
                        game.add_bullet(x,y ,enemy_x ,enemy_y ,tower)
                        tower.last_attack_time = current_time
                    break


            tower.update_frame()
            screen.blit(tower.frames[tower.current_frame], (x, y))
        button1.draw(screen)
        #button2.draw(screen)
        tower_i.draw()
        tower_j.draw()
        tower_k.draw()
        tower_l.draw()
        sale.draw(screen)
        pause.draw(screen)
        draw_pointer(game)
        game.add_enemy(screen,start_time)

        wave_text = font.render(f'Wave:  {game.wave_count} / {game.waves}', True, black)
        wave_text_rect = wave_text.get_rect(center=(screen.get_width() // 2  - 200, font.get_height()*2))
        screen.blit(wave_text, wave_text_rect)

        enemy_text = font.render(f'Enemies:  {game.enemy_count} / {game.max_enemies}', True, black)
        enemy_text_rect = enemy_text.get_rect(center=(screen.get_width() // 2  + 200, font.get_height()*2))
        screen.blit(enemy_text, enemy_text_rect)

        draw_player_info(screen, game)

        game.update_bullets()
        game.draw_bullets()

        pygame.display.flip()

def pause_menu(screen):
    screen_width, screen_height = screen.get_size()
    menu_width = 500
    menu_height = 563
    menu_x = (screen_width - menu_width) // 2
    menu_y = (screen_height - menu_height) // 2
    pygame.draw.rect(screen, cyan, [menu_x, menu_y, menu_width, menu_height])

    font = pygame.font.Font(None, 50)
    text = font.render("Pause Menu", True, black)
    text_rect = text.get_rect(center=(screen_width // 2, menu_y + text.get_height() + 25))
    screen.blit(text, text_rect)
        
    continue_b.draw(screen)
    restart.draw(screen)
    quit.draw(screen)

def lose_win(screen):
    screen_width, screen_height = screen.get_size()
    menu_width = 500
    menu_height = 563
    menu_x = (screen_width - menu_width) // 2
    menu_y = (screen_height - menu_height) // 2
    pygame.draw.rect(screen, cyan, [menu_x, menu_y, menu_width, menu_height])

    restart.draw(screen)
    quit.draw(screen)

# 定義按鈕類
class Button:
    def __init__(self, x, y, w, h, text, text_size=24):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.text_size = text_size

    def draw(self, screen):
        pygame.draw.rect(screen, purple, self.rect)
        font = pygame.font.Font(None,self.text_size)
        text=font.render(self.text,True ,black)
        text_rect=text.get_rect(center=self.rect.center)
        screen.blit(text,text_rect)

selected_tower = None

# 定義按鈕類
class Tower:
    def __init__(self, screen, x, y, w, h, frames,size=None,cost=0, damage=0, range=0,attack_speed=1):
        self.screen = screen
        self.rect = pygame.Rect(x, y, w, h)
        self.frames = frames
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_interval = 100
        if size is not None:
            self.frames = [pygame.transform.scale(frame, size) for frame in frames]
        else:
            self.frames = frames
        self.cost = cost
        self.damage = damage
        self.range = range
        self.last_attack_time = 0
        self.attack_speed = attack_speed

    def update_frame(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_interval:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def draw(self):
        self.update_frame()
        self.screen.blit(self.frames[self.current_frame], self.rect)

# 设置地图大小
map_size = 15
# 设置格子大小
cell_size = 45

# 初始化 mixer 模块
pygame.mixer.init()

def load_tower(filename):
    frames = []
    with Image.open(filename) as im:
        if im.is_animated:
            for frame in range(im.n_frames):
                im.seek(frame)
                frame_image = im.convert("RGBA")
                frame_surface = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
                frames.append(frame_surface)
    return frames

tw1 = load_tower("tw1.gif")
tw2 = load_tower("tw2.gif")
tw3 = load_tower("tw3.gif")
tw4 = load_tower("tw4.gif")

Map1 = Button(750 - (button_width*3)//2, 280 - button_height, button_width*3, button_height, "Map 1", text_size=36)
Map2 = Button(750 - (button_width*3)//2, 300, button_width*3, button_height, "Map 2", text_size=36)
Map3 = Button(750 - (button_width*3)//2, 400, button_width*3, button_height, "Map 3", text_size=36)
button1=Button(150 ,0 ,button_width*2 ,38 ,"Robot")
#button2=Button(150 ,38 ,button_width*2 ,38 ,"Human")
tower_i = Tower(screen, 15, 15, 115, (button_height*3)//2, tw1)
tower_j = Tower(screen, 15, 150, 115, (button_height*3)//2, tw2)
tower_k = Tower(screen, 15, 285, 115, (button_height*3)//2, tw3)
tower_l = Tower(screen, 15, 420, 115, (button_height*3)//2, tw4)
sale=Button(15 ,750-button_height -10 ,button_width ,button_height ,"sale")
pause=Button(80 ,750-button_height -10 ,button_width ,button_height ,"pause")
continue_b=Button(750 - (button_width*3)//2, 320 - button_height, button_width*3, button_height, "Continue", text_size=36)
restart=Button(750 - (button_width*3)//2, 440 - button_height, button_width*3, button_height, "Restart", text_size=36)
quit=Button(750 - (button_width*3)//2, 570 - button_height, button_width*3, button_height, "Quit", text_size=36)


tower_i_map = Tower(screen, 15, 15, 115, (button_height*3)//2, tw1, (cell_size, cell_size),cost=50,damage=1,
                    range=5*cell_size)
tower_j_map = Tower(screen, 15, 150, 115, (button_height*3)//2, tw2, (cell_size, cell_size),cost=100,damage=2,
                    range=5*cell_size)
tower_k_map = Tower(screen, 15, 285, 115, (button_height*3)//2, tw3, (cell_size, cell_size),cost=150,damage=1,
                    range=6*cell_size)
tower_l_map = Tower(screen, 15, 420, 115, (button_height*3)//2, tw4, (cell_size, cell_size),cost=200,damage=2,
                    range=6*cell_size)

# 设置敌人图片位置
enemy_images = ["e1.gif", "e2.gif", "e3.gif"]
enemy_damages = {0: 10, 1: 20, 2: 30}
enemy_speeds = {0: 0.03, 1: 0.01, 2: 0.02}
enemy_healths = {0: 10, 1: 20, 2: 15}


def load_enemy_images(enemy_image):
    # 加载敌人图片
    gif = Image.open(enemy_image)
    frame_count = gif.n_frames
    frames = []
    frame_delays = []
    for frame in range(frame_count):
        gif.seek(frame)
        frame_image = gif.copy().convert("RGBA")
        frame_data = frame_image.tobytes()
        frame_surface = pygame.image.fromstring(frame_data, frame_image.size, frame_image.mode)
        frames.append(frame_surface)
        frame_delays.append(gif.info['duration'])

    # 调整敌人图片大小
    for i in range(len(frames)):
        frames[i] = pygame.transform.scale(frames[i], (cell_size, cell_size))
    
    # 更改特定 GIF 的帧速率
    if enemy_image == enemy_images[0]:
        for i in range(len(frame_delays)):
            frame_delays[i] *= 3
    
    return frames, frame_delays

# 加载敌人图片
enemies_frames = []
enemies_frame_delays = []
for enemy_image in enemy_images:
    frames, frame_delays = load_enemy_images(enemy_image)
    enemies_frames.append(frames)
    enemies_frame_delays.append(frame_delays)

map1 =  [   [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #1
            [0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0], #2
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #3
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #4
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #5
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #6
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #7
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #8
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #9
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #10
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #11
            [0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0], #12
            [0,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0], #13
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0], #14
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
        ]
map2 = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], #1
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0], #2
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0], #3
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0], #4
            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #5
            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0], #6
            [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0], #7
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0], #8
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0], #9
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0], #10
            [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0], #11
            [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0], #12
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], #13
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0], #14
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]  #15
        ]

map3 = [
            [1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,0], #1
            [0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,0,0], #2
            [0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,1,0,1,0,0], #3
            [0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,1,1,1], #4
            [0,1,0,1,1,1,0,1,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,0,1,0,0,0,1], #5
            [0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1], #6
            [0,1,0,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,1], #7
            [0,1,0,1,0,1,0,1,0,0,0,1,1,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0], #8
            [0,1,0,1,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0], #9
            [0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0], #10
            [0,1,0,1,0,1,1,1,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0], #11
            [0,1,0,1,1,1,0,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0], #12
            [0,1,0,0,0,0,0,1,0,1,0,0,0,1,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0], #13
            [0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0], #14
            [0,1,1,1,0,1,1,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1]  #15
        ]


land_image = pygame.image.load("land2.jpg")
road_image = pygame.image.load("road3.jpg")

class Game:
    def __init__(self):
        self.enemy_count = 0
        self.enemy_type = 0
        self.last_enemy_time = time.time()
        self.spawn_time = 0
        self.wave_count = 0
        self.max_enemies = 0
        self.waves = 0
        self.player_health = 100
        self.player_money = 500
        self.selected_tower = None
        self.towers = []
        self.current_screen = "start"
        self.bullets = []
        self.pointer_text = None
        self.map_now = None

    def reset_game(self):
    # 重置游戏状态
        self.enemy_count = 0
        self.enemy_type = 0
        self.last_enemy_time = time.time()
        self.spawn_time = 0
        self.wave_count = 0
        self.player_health = 100
        self.player_money = 500
        self.selected_tower = None
        self.towers = []
        self.bullets = []
        self.pointer_text = None

        # 清空敌人列表
        enemies.clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_screen == "start":
                    if Map1.rect.collidepoint(event.pos):
                        self.max_enemies = 30
                        self.waves = 3 
                        self.map_now = map1
                        self.current_screen = "game"
                    elif Map2.rect.collidepoint(event.pos):
                        self.max_enemies = 50 
                        self.waves = 5 
                        self.map_now = map2
                        self.current_screen = "game"
                    elif Map3.rect.collidepoint(event.pos):
                        self.max_enemies = 80 
                        self.waves = 8 
                        self.map_now = map3
                        self.current_screen = "game"
                elif self.current_screen == "game":
                    if pause.rect.collidepoint(event.pos):
                        self.current_screen = "pause"
                    if sale.rect.collidepoint(event.pos):
                        self.pointer_text = sale.text
                    else:
                        if self.pointer_text == sale.text:
                            x, y = event.pos
                            row = (y - 75) // cell_size
                            col = (x - 150) // cell_size
                            if 0 <= row < map_size and 0 <= col < map_size*2:
                                # 检查该单元格是否有炮塔
                                for tower in self.towers:
                                    if tower[0] == row and tower[1] == col:
                                        # 移除炮塔并返还金钱
                                        self.towers.remove(tower)
                                        self.player_money += tower[2].cost // 2
                                        break
                            # 清除鼠标指针文本
                            self.pointer_text = None
                    if tower_i.rect.collidepoint(event.pos):
                        #self.selected_tower = tower_i_map
                        self.selected_tower = Tower(screen, 15, 15, 115, (button_height*3)//2, tw1, (cell_size, cell_size),cost=50,damage=1,
                    range=5*cell_size)
                    elif tower_j.rect.collidepoint(event.pos):
                        #self.selected_tower = tower_j_map
                        self.selected_tower = Tower(screen, 15, 150, 115, (button_height*3)//2, tw2, (cell_size, cell_size),cost=100,damage=2,
                    range=5*cell_size)
                    elif tower_k.rect.collidepoint(event.pos):
                        #self.selected_tower = tower_k_map
                        self.selected_tower = Tower(screen, 15, 285, 115, (button_height*3)//2, tw3, (cell_size, cell_size),cost=150,damage=1,
                    range=6*cell_size)
                    elif tower_l.rect.collidepoint(event.pos):
                        #self.selected_tower = tower_l_map
                        self.selected_tower = Tower(screen, 15, 420, 115, (button_height*3)//2, tw4, (cell_size, cell_size),cost=200,damage=2,
                    range=6*cell_size)
                    else:
                        # 检查是否选择了塔
                        if self.selected_tower:
                            # 在地图上放置所选塔
                            x, y = event.pos
                            row = (y - 75) // cell_size
                            col = (x - 150) // cell_size
                            if 0 <= row < map_size and 0 <= col < map_size*2:
                                if self.map_now[row][col] == 0:
                                    if not any(tower_row == row and tower_col == col for tower_row,tower_col,_ in self.towers):
                                        if self.player_money >= self.selected_tower.cost:
                                            self.towers.append((row,col,self.selected_tower))
                                            self.player_money -= self.selected_tower.cost
                            self.selected_tower = None
                elif self.current_screen == "pause" or self.current_screen == "l_w":
                    if continue_b.rect.collidepoint(event.pos):
                        self.paused = False
                        self.current_screen = "game"
                    elif restart.rect.collidepoint(event.pos):
                        self.reset_game()
                        self.map_now = copy.deepcopy(self.rmap)
                        self.current_screen = "game"
                    elif quit.rect.collidepoint(event.pos):
                        self.reset_game()
                        self.current_screen = "start"

    def draw_map(self, screen):
        for row in range(map_size):
            for col in range(map_size*2):
                x = 150 + cell_size * col
                y = 75 + cell_size * row
                if self.map_now[row][col] == 0:
                    screen.blit(land_image, (x, y))
                else:
                    screen.blit(road_image, (x, y))
    
    def add_bullet(self, x, y, target_x, target_y, tower):
        # 计算子弹移动的方向
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx*dx + dy*dy)
        # 计算子弹移动的速度
        speed = 5
        vx = dx / distance * speed
        vy = dy / distance * speed
        self.bullets.append([x, y, vx, vy, tower])

    def update_bullets(self):
        for bullet in self.bullets:
            x, y, vx, vy, tower = bullet
            # 更新子弹的位置
            bullet[0] += vx
            bullet[1] += vy

            # 检查子弹是否击中敌人
            for enemy_pos in enemies:
                enemy_x = 150 + enemy_pos[0] * cell_size + cell_size/2
                enemy_y = 75 + enemy_pos[1] * cell_size + cell_size/2
                if math.sqrt((x-enemy_x)**2 + (y-enemy_y)**2) < cell_size/2:
                    # 扣除敌人的血量并移除子弹
                    tower = bullet[4]
                    enemy_pos[3] -= tower.damage # 根据发射子弹的炮塔扣除敌人的血量
                    
                    if enemy_pos[3] <= 0:
                        self.player_money += 30

                    self.bullets.remove(bullet)
                    break

            # 检查子弹是否超出地图范围
            if x < 150 or x > 150 + map_size*2*cell_size or y < 75 or y > 75 + map_size*cell_size:
                self.bullets.remove(bullet)

        # 移除血量为零的敌人
        for enemy_pos in enemies:
            if enemy_pos[3] <= 0:
                enemies.remove(enemy_pos)

    
    def draw_bullets(self):
        for bullet in self.bullets:
            x, y, _, _, _ = bullet

            pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 5)

    def add_enemy(self, screen, start_time):
        current_time = time.time()
        if not enemies:
            self.enemy_type = random.choice(range(len(enemy_images)))
        if self.enemy_count % 5 == 0:
            prev_enemy_type = self.enemy_type
            self.enemy_type = random.choice(range(len(enemy_images)))
            if self.enemy_type != prev_enemy_type:
                pygame.mixer.music.load(f'e{self.enemy_type+1}.mp3')
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
            self.spawn_time = 10
        else:
            self.spawn_time = 2
        if current_time - start_time > 5:
            if current_time - self.last_enemy_time > self.spawn_time:
                if self.enemy_count < self.max_enemies: # 检查当前敌人数量是否小于最大敌人数量
                    if self.enemy_count % (self.max_enemies // self.waves) == 0:
                        self.wave_count += 1
                    health = enemy_healths[self.enemy_type] # 获取当前敌人类型对应的初始血量
                    path = self.get_path()
                    speed = random.uniform(0.1, 0.5) # 给敌人一个随机速度
                    enemies.append([0, path, self.enemy_type, health, speed]) # 添加路径和速度属性
                    self.enemy_count += 1
                    self.last_enemy_time = current_time
                    

                        
        for enemy_pos in enemies:
            # Move the enemy along the path
            speed = enemy_pos[4]
            enemy_pos[0] += speed
            if int(enemy_pos[0]) >= len(enemy_pos[1]) - 1:
                enemy_pos[0] = len(enemy_pos[1]) - 1

            # Get the current position of the enemy on the map
            current_pos = enemy_pos[1][int(enemy_pos[0])]
            row = current_pos[0]
            col = current_pos[1]
        
            # Draw the enemy and its health bar
            self.draw_enemy(screen, (col, row), enemy_pos[2], enemy_pos[3])

            if int(enemy_pos[0]) >= len(enemy_pos[1]) - 1:
                self.player_health -= 10
                enemies.remove(enemy_pos)

            if self.player_health <= 0:
                self.current_screen = "l_w"

    
    def draw_enemy(self, screen, enemy_pos, enemy_type, health):
        #print(enemy_pos) # print the position of the enemy
        frames = enemies_frames[enemy_type]
        frame_delays = enemies_frame_delays[enemy_type]
        current_time = pygame.time.get_ticks()
        current_frame = 0
        while current_time > frame_delays[current_frame]:
            current_time -= frame_delays[current_frame]
            current_frame = (current_frame + 1) % len(frames)
        screen.blit(frames[current_frame], (150 + enemy_pos[0]*cell_size + cell_size/2 - frames[current_frame].get_width()/2,
                            75 + enemy_pos[1]*cell_size + cell_size/2 - frames[current_frame].get_height()/2))
    
        # 绘制血条
        health_bar_width = cell_size
        health_bar_height = 5
        health_bar_x = 150 + enemy_pos[0]*cell_size + cell_size/2 - health_bar_width/2
        health_bar_y = 75 + enemy_pos[1]*cell_size - health_bar_height - 5
        pygame.draw.rect(screen, (255, 0, 0), [health_bar_x, health_bar_y, health_bar_width, health_bar_height])
        pygame.draw.rect(screen, (0, 255, 0), [health_bar_x, health_bar_y, health / enemy_healths[enemy_type] * health_bar_width, health_bar_height])

    def get_path(self):
    # Find the starting position
        start_row = 0
        start_col = 0
        for row in range(len(self.map_now)):
            for col in range(len(self.map_now[0])):
                if self.map_now[row][col] == 1:
                    start_row = row
                    start_col = col
                    break
            else:
                continue
            break

        # Initialize the path with the starting position
        path = [(start_row, start_col)]
        current_row = start_row
        current_col = start_col

        # Define the directions for moving up, down, left and right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while True:
            found_next = False
            for direction in directions:
                next_row = current_row + direction[0]
                next_col = current_col + direction[1]
                if (next_row >= 0 and next_row < len(self.map_now) and next_col >= 0 and next_col < len(self.map_now[0]) and self.map_now[next_row][next_col] == 1 and (next_row, next_col) not in path):
                    path.append((next_row, next_col))
                    current_row = next_row
                    current_col = next_col
                    found_next = True
                    break

            if not found_next:
                break
    
        return path

# Create an instance of the Game class
game = Game()

# Set the current map
game.map_now = map1

# Get the path for the current map
path = game.get_path()

# Print the path
#print(path)


def draw_player_info(screen, game):
    # 绘制血条
    hp_text = font.render(f'HP    : {game.player_health}', True, black)
    hp_text_rect = hp_text.get_rect(topright=(screen.get_width() - 100 , font.get_height()))
    screen.blit(hp_text, hp_text_rect)
    
    # 绘制金币数量
    money_text = font.render(f'Money: {game.player_money}', True, black)
    money_text_rect = money_text.get_rect(topright=(screen.get_width()- 100 , font.get_height()*2))
    screen.blit(money_text, money_text_rect)

# 设置敌人列表
enemies = []

def draw_pointer(game):
    if game.selected_tower is not None:
        x, y = pygame.mouse.get_pos()
        image = game.selected_tower.frames[0]
        screen.blit(image, (x, y))

    if game.pointer_text is not None:
        x, y = pygame.mouse.get_pos()
        pointer_text = font.render(game.pointer_text, True, black)
        screen.blit(pointer_text, (x, y))

if __name__ == '__main__':
    pygame.init()
    main()
