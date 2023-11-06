import tkinter as tk
from tkinter import Button
from tkinter import PhotoImage
import time
import numpy as np
from PIL import ImageTk, Image
import os
import random

UNIT = 2.5 # 픽셀 수
HEIGHT = 250 # 세로
WIDTH = 400 # 가로
SLATE_LENGTH = 168 #석판 크기
SLATE_NUM = 6 # 석판 개수
CARD_NUMBER = 5 #대폭발, 지진, 폭풍우, 해일, 충격파
CARD_REIN = 10

slate = [[0 for j in range(SLATE_NUM)] for i in range(SLATE_NUM)]
slate_img = [[0 for j in range(SLATE_NUM)] for i in range(SLATE_NUM)]
card = [0 for _ in range(2)]
card_img = [0 for _ in range(2)]
next_card = [0 for _ in range(3)]
card_change = [0 for _ in range(2)]
card_change_img = [0 for _ in range(2)]
card_name_img = [0 for _ in range(CARD_NUMBER)]
card_type_img = [0 for _ in range(CARD_NUMBER)]
card_rein_img = [0 for _ in range(CARD_REIN)]
next_card_img1 = [0 for _ in range(CARD_NUMBER)]
next_card_img2 = [0 for _ in range(CARD_NUMBER)]

selected_card = 2 #현재 고른 카드의 번호 / 0:왼쪽 1:오른쪽 2:선택안했음
flag = 0

w = tk.Tk()
canvas = tk.Canvas(bg='white', height=HEIGHT * UNIT, width=WIDTH * UNIT)
current_dir = os.path.dirname(os.path.abspath(__file__))
slateImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/slate.png'))
                              .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
slate_clickImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/slate_click.png'))
                                    .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
slate_hoverImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/slate_hover.png'))
                                    .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
slate_breakImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/slate_break.png'))
                                    .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
card_exampleImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/card_bg.png'))
                                     .resize((int(60 * UNIT), int(90 * UNIT))))
card_click_exampleImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/card_bg_select.png'))
                                           .resize((int(60 * UNIT), int(90 * UNIT))))
card_changeImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/card_change.png'))
                                    .resize((int(60 * UNIT), int(20 * UNIT))))
special_slate_explanation = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_explanation.png'))
                                               .resize((int(160 * UNIT), int(70 * UNIT))))
change_number = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/change_number.png'))
                                   .resize((int(80 * UNIT), int(20 * UNIT))))
nextCardPanel = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/next_card_panel.png'))
                                   .resize((int(120 * UNIT), int(40 * UNIT))))
arrow = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/arrow.png'))
                           .resize((int(7.5 * UNIT), int(7.4 * UNIT))))

cardname = 'img/card_name'
cardtype = 'img/card'
tail = '.png'
rein = 'img/rein'
nextcardtype = 'img/next_card'

for i in range(0,CARD_NUMBER):
    str1 = cardname + str(i) + tail
    str2 = cardtype + str(i) + tail
    str3 = nextcardtype + str(i) + tail
    card_name_img[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str1))
                           .resize((int(37 * UNIT), int(19 * UNIT))))
    card_type_img[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str2))
                           .resize((int(50 * UNIT), int(50 * UNIT))))
    next_card_img1[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str3))
                           .resize((int(20 * UNIT), int(30 * UNIT))))
    next_card_img2[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str3))
                           .resize((int(22 * UNIT), int(33 * UNIT))))

for i in range(0,CARD_REIN):
    str1 = rein+str(i)+tail
    card_rein_img[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str1))
                           .resize((int(12 * UNIT), int(19 * UNIT))))
    
#석판 생성
for col in range(0,SLATE_NUM):
    for row in range(0,SLATE_NUM):
        slate[col][row] = slateImg
        slate_img[col][row] = canvas.create_image(16 * UNIT + SLATE_LENGTH * UNIT / (2 * SLATE_NUM) + SLATE_LENGTH * UNIT * row / SLATE_NUM, 
                            16 * UNIT + SLATE_LENGTH * UNIT / (2 * SLATE_NUM) + SLATE_LENGTH * UNIT * col / SLATE_NUM, 
                            image=slate[col][row])
        
#카드 생성
card[0] = card_exampleImg
card_img[0] = canvas.create_image(249 * UNIT, 170 * UNIT, image=card[0])
card[1] = card_exampleImg
card_img[1] = canvas.create_image(335 * UNIT, 170 * UNIT, image=card[1])

#카드 교체 생성
card_change[0] = card_changeImg
card_change_img[0] = canvas.create_image(249 * UNIT, 230 * UNIT, image=card_change[0])
card_change[1] = card_changeImg
card_change_img[1] = canvas.create_image(335 * UNIT, 230 * UNIT, image=card_change[1])

#특수 석판 설명 생성
canvas.create_image(292 * UNIT, 55 * UNIT, image=special_slate_explanation)

#교체 가능 횟수 생성
canvas.create_image(292 * UNIT, 110 * UNIT, image=change_number)

#다음카드란 생성
canvas.create_image(100 * UNIT, 210 * UNIT, image=nextCardPanel)
next_card[0] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/card_bg.png'))
                   .resize((int(20 * UNIT), int(30 * UNIT))))
canvas.create_image(64 * UNIT, 211 * UNIT, image=next_card[0])
next_card[1] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/card_bg.png'))
                   .resize((int(20 * UNIT), int(30 * UNIT))))
canvas.create_image(99 * UNIT, 211 * UNIT, image=next_card[1])
next_card[2] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/card_bg.png'))
                   .resize((int(22 * UNIT), int(33 * UNIT))))
canvas.create_image(135 * UNIT, 209.5 * UNIT, image=next_card[2])
arrow1 = arrow
canvas.create_image(81.75 * UNIT, 213 * UNIT, image=arrow1)
arrow2 = arrow
canvas.create_image(117.25 * UNIT, 213 * UNIT, image=arrow2)

def click(event):
    click_card(event)
    click_slate(event)
    click_card_change(event)

def hover(event):
    hover_slate(event)

def release(event):
    release_slate(event)

def motion(event):
    motion_slate(event)

#석판 클릭 인식 함수
def click_slate(event):
    global selected_card
    global flag
    if selected_card != 2:
        if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
            and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
            for col in range(0,SLATE_NUM):
                for row in range(0,SLATE_NUM):
                    if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                        and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                        canvas.itemconfig(slate_img[col][row], image=slate_clickImg)
                        slate, card, nextcard = env.use_card(col,row)
                        if flag == 1:
                            canvas.create_text(WIDTH * UNIT / 2, HEIGHT * UNIT / 2, 
                                               text="WIN", fill="black", font=("Helvetica 250 bold"))
                        env.reinforcement_card()
                        for col in range(0,SLATE_NUM):
                            for row in range(0,SLATE_NUM):
                                if slate[col][row] == 0 :
                                    canvas.itemconfig(slate_img[col][row], image=slate_breakImg)
                                elif slate[col][row] == 1:
                                    canvas.itemconfig(slate_img[col][row], image=slateImg)
                        canvas.itemconfig(env_card_rein_img[0], image=card_rein_img[env.card[0].get_rein()])
                        canvas.itemconfig(env_card_rein_img[1], image=card_rein_img[env.card[1].get_rein()])
                        canvas.itemconfig(env_card_type_img[0], image=card_type_img[env.card[0].get_num()])
                        canvas.itemconfig(env_card_type_img[1], image=card_type_img[env.card[1].get_num()])
                        canvas.itemconfig(env_card_name_img[0], image=card_name_img[env.card[0].get_num()])
                        canvas.itemconfig(env_card_name_img[1], image=card_name_img[env.card[1].get_num()])
                        canvas.itemconfig(env_next_card_img[0], image=next_card_img1[env.nextcard[0].get_num()])
                        canvas.itemconfig(env_next_card_img[1], image=next_card_img1[env.nextcard[1].get_num()])
                        canvas.itemconfig(env_next_card_img[2], image=next_card_img2[env.nextcard[2].get_num()])
                        if selected_card == 0:
                            canvas.itemconfig(card_img[0], image=card_exampleImg)
                            selected_card = 2
                        if selected_card == 1:
                            canvas.itemconfig(card_img[1], image=card_exampleImg)
                            selected_card = 2
                        print("select slate : ", end='')
                        print(row, end=' ')
                        print(col, end='\n\n')
                        time.sleep(0.1)

#석판 클릭하면서 움직임 인식 함수
def motion_slate(event):
    if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
        and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
        for col in range(0,SLATE_NUM):
            for row in range(0,SLATE_NUM):
                if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                    and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                    canvas.itemconfig(slate_img[col][row], image=slate_clickImg)
                    print(row, end=' ')
                    print(" ", end=' ')
                    print(col, end='\n\n')
                    time.sleep(0.1)

#석판 호버 인식 함수
def hover_slate(event):
    if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
        and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
        for col in range(0,SLATE_NUM):
            for row in range(0,SLATE_NUM):
                if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                    and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                    canvas.itemconfig(slate_img[col][row], image=slate_hoverImg)
                    #print(row, end=' ')
                    #print(" ", end=' ')
                    #print(col, end='\n\n')

#석판 클릭 해제 인식 함수
def release_slate(event):
    if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
        and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
        for col in range(0,SLATE_NUM):
            for row in range(0,SLATE_NUM):
                if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                    and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                    canvas.itemconfig(slate_img[col][row], image=slate_hoverImg)
                    #print(row, end=' ')
                    #print(" ", end=' ')
                    #print(col, end='\n\n')
                    time.sleep(0.2)

#카드 클릭 인식 함수
def click_card(event):
    global selected_card
    if (event.x > 219 * UNIT and event.x < 279 * UNIT
        and event.y > 125 * UNIT and event.y < 215 * UNIT):
        if selected_card != 0:
            canvas.itemconfig(card_img[0], image=card_click_exampleImg)
            canvas.itemconfig(card_img[1], image=card_exampleImg)
            selected_card = 0
            print("select card1")
    if (event.x > 305 * UNIT and event.x < 365 * UNIT
        and event.y > 125 * UNIT and event.y < 215 * UNIT):
        if selected_card != 1:
            canvas.itemconfig(card_img[0], image=card_exampleImg)
            canvas.itemconfig(card_img[1], image=card_click_exampleImg)
            selected_card = 1
            print("select card2")

#카드 교체 클릭 인식 함수
def click_card_change(event):
    global selected_card
    if (event.x > 219 * UNIT and event.x < 279 * UNIT
        and event.y > 220 * UNIT and event.y < 240 * UNIT):
        env.change_card(0)
        print("change card1")
        env.reinforcement_card()
        canvas.itemconfig(env_card_rein_img[0], image=card_rein_img[env.card[0].get_rein()])
        canvas.itemconfig(env_card_rein_img[1], image=card_rein_img[env.card[1].get_rein()])
        canvas.itemconfig(env_card_type_img[0], image=card_type_img[env.card[0].get_num()])
        canvas.itemconfig(env_card_type_img[1], image=card_type_img[env.card[1].get_num()])
        canvas.itemconfig(env_card_name_img[0], image=card_name_img[env.card[0].get_num()])
        canvas.itemconfig(env_card_name_img[1], image=card_name_img[env.card[1].get_num()])
        canvas.itemconfig(env_next_card_img[0], image=next_card_img1[env.nextcard[0].get_num()])
        canvas.itemconfig(env_next_card_img[1], image=next_card_img1[env.nextcard[1].get_num()])
        canvas.itemconfig(env_next_card_img[2], image=next_card_img2[env.nextcard[2].get_num()])
        if selected_card == 0:
            canvas.itemconfig(card_img[0], image=card_exampleImg)
            selected_card = 2
        if selected_card == 1:
            canvas.itemconfig(card_img[1], image=card_exampleImg)
            selected_card = 2
    if (event.x > 305 * UNIT and event.x < 365 * UNIT
        and event.y > 220 * UNIT and event.y < 240 * UNIT):
        env.change_card(1)
        print("change card2")
        env.reinforcement_card()
        canvas.itemconfig(env_card_rein_img[0], image=card_rein_img[env.card[0].get_rein()])
        canvas.itemconfig(env_card_rein_img[1], image=card_rein_img[env.card[1].get_rein()])
        canvas.itemconfig(env_card_type_img[0], image=card_type_img[env.card[0].get_num()])
        canvas.itemconfig(env_card_type_img[1], image=card_type_img[env.card[1].get_num()])
        canvas.itemconfig(env_card_name_img[0], image=card_name_img[env.card[0].get_num()])
        canvas.itemconfig(env_card_name_img[1], image=card_name_img[env.card[1].get_num()])
        canvas.itemconfig(env_next_card_img[0], image=next_card_img1[env.nextcard[0].get_num()])
        canvas.itemconfig(env_next_card_img[1], image=next_card_img1[env.nextcard[1].get_num()])
        canvas.itemconfig(env_next_card_img[2], image=next_card_img2[env.nextcard[2].get_num()])
        if selected_card == 0:
            canvas.itemconfig(card_img[0], image=card_exampleImg)
            selected_card = 2
        if selected_card == 1:
            canvas.itemconfig(card_img[1], image=card_exampleImg)
            selected_card = 2

#마우스 이벤트
canvas.bind("<Button-1>", click)
#canvas.bind("<Motion>", hover)
#canvas.bind("<ButtonRelease-1>", release)
#canvas.bind("<B1-Motion>", motion)

canvas.pack()

class Card:
    def __init__(self):
        global flag
        self.num = random.randint(0, CARD_NUMBER - 1)
        self.reinforcementStep = 0
    
    def get_num(self):
        return int(self.num)
    
    def get_rein(self):
        return int(self.reinforcementStep)
    
    def set_num(self, num):
        self.num = num
    
    def set_rein(self, rein):
        self.reinforcementStep = rein

    def use_card(self, slate, x, y):
        slate[x][y] = 0
        if self.num == 0:
            for i in range(1, SLATE_NUM):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0 and y - i >= 0:
                        slate[x - i][y - i] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM and y - i >= 0:
                        slate[x - i][y - i] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0 and y + i < SLATE_NUM:
                        slate[x - i][y - i] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM and y + i < SLATE_NUM:
                        slate[x - i][y - i] = 0
        elif self.num == 1:
            for i in range(1, SLATE_NUM):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y - i >= 0:
                        slate[x][y - i] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y + i < SLATE_NUM:
                        slate[x][y + i] = 0
        elif self.num == 2:
            for i in range(1, SLATE_NUM):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0:
                        slate[x - i][y] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM:
                        slate[x + i][y] = 0
        elif self.num == 3:
            for i in range(1, SLATE_NUM):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y - i >= 0:
                        slate[x][y - i] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y + i < SLATE_NUM:
                        slate[x][y + i] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0:
                        slate[x - i][y] = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM:
                        slate[x + i][y] = 0
        elif self.num == 4:
            for i in range(-1,self.reinforcementStep + 1):
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if y - i >= 0:
                        slate[x][y - i] = 0
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if y + i < SLATE_NUM:
                        slate[x][y + i] = 0
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if x - i >= 0:
                        slate[x - i][y] = 0
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if x + i < SLATE_NUM:
                        slate[x + i][y] = 0
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if x - i >= 0 and y - i >= 0:
                        slate[x - i][y - i] = 0
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if x + i < SLATE_NUM and y - i >= 0:
                        slate[x - i][y - i] = 0
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if x - i >= 0 and y + i < SLATE_NUM:
                        slate[x - i][y - i] = 0
                if random.randint(0, 100) <= 25 * (self.reinforcementStep - i):
                    if x + i < SLATE_NUM and y + i < SLATE_NUM:
                        slate[x - i][y - i] = 0
        total = SLATE_NUM * SLATE_NUM
        for i in range(0,SLATE_NUM):
            for j in range(0,SLATE_NUM):
                if slate[i][j] != 0:
                    print(1, end=' ')
                    total = total - 1
                else:
                    print(0, end=' ')
            print()
        if total == 0:
            flag = 1
        return slate

                
        
class Slate:
    def __init__(self, x, y):
        self.num = 1
        self.x = x
        self.y = y

class Env:
    def __init__(self):
        self.slate = [[0 for j in range(SLATE_NUM)] for i in range(SLATE_NUM)]
        self.card = [0 for _ in range(0,2)]
        self.nextcard = [0 for _ in range(0,3)]
        for col in range(0,SLATE_NUM):
            for row in range(0,SLATE_NUM):
                self.slate[col][row] = Slate(col,row)
        self.card[0] = Card()
        self.card[1] = Card()
        self.nextcard[0] = Card()
        self.nextcard[1] = Card()
        self.nextcard[2] = Card()
    
    def use_card(self, x, y):
        global selected_card
        self.slate = self.card[selected_card].use_card(self.slate, x, y)
        self.card[selected_card] = self.nextcard[2]
        self.nextcard[2] = self.nextcard[1]
        self.nextcard[1] = self.nextcard[0]
        self.nextcard[0] = Card()
        print("card1 : ", self.card[0].get_num(), end=' ')
        print(self.card[0].get_rein())
        print("card2 : ", self.card[1].get_num(), end=' ')
        print(self.card[1].get_rein())
        print("nextcard1 : ", self.nextcard[2].get_num(), end=' ')
        print(self.nextcard[2].get_rein())
        print("nextcard2 : ", self.nextcard[1].get_num(), end=' ')
        print(self.nextcard[1].get_rein())
        print("nextcard3 : ", self.nextcard[0].get_num(), end=' ')
        print(self.nextcard[0].get_rein(), end='\n\n')
        return self.slate, self.card, self.nextcard
    
    def reinforcement_card(self):
        while self.card[0].get_num() == self.card[1].get_num():
            tmp = self.card[0].get_rein()
            if self.card[0].get_rein() < self.card[1].get_rein():
                tmp = self.card[1].get_rein()
            self.card[0].set_rein(tmp + 1)
            self.card[1] = self.nextcard[2]
            self.nextcard[2] = self.nextcard[1]
            self.nextcard[1] = self.nextcard[0]
            self.nextcard[0] = Card()
            print("card1 : ", self.card[0].get_num(), end=' ')
            print(self.card[0].get_rein())
            print("card2 : ", self.card[1].get_num(), end=' ')
            print(self.card[1].get_rein())
            print("nextcard1 : ", self.nextcard[2].get_num(), end=' ')
            print(self.nextcard[2].get_rein())
            print("nextcard2 : ", self.nextcard[1].get_num(), end=' ')
            print(self.nextcard[1].get_rein())
            print("nextcard3 : ", self.nextcard[0].get_num(), end=' ')
            print(self.nextcard[0].get_rein(), end='\n\n')
        print("card1 : ", self.card[0].get_num(), end=' ')
        print(self.card[0].get_rein())
        print("card2 : ", self.card[1].get_num(), end=' ')
        print(self.card[1].get_rein())
        print("nextcard1 : ", self.nextcard[2].get_num(), end=' ')
        print(self.nextcard[2].get_rein())
        print("nextcard2 : ", self.nextcard[1].get_num(), end=' ')
        print(self.nextcard[1].get_rein())
        print("nextcard3 : ", self.nextcard[0].get_num(), end=' ')
        print(self.nextcard[0].get_rein(), end='\n\n')
    
    def change_card(self, num):
        self.card[num] = self.nextcard[2]
        self.nextcard[2] = self.nextcard[1]
        self.nextcard[1] = self.nextcard[0]
        self.nextcard[0] = Card()



env = Env()
env_card_rein_img = [0 for _ in range(2)]
env_card_name_img = [0 for _ in range(2)]
env_card_type_img = [0 for _ in range(2)]
env_next_card_img = [0 for _ in range(3)]
env_card_rein_img[0] = canvas.create_image(230 * UNIT, 140 * UNIT, 
                    image=card_rein_img[env.card[0].get_rein()])
env_card_rein_img[1] = canvas.create_image(316 * UNIT, 140 * UNIT, 
                    image=card_rein_img[env.card[1].get_rein()])
env_card_name_img[0] = canvas.create_image(255.5 * UNIT, 140 * UNIT, 
                    image=card_name_img[env.card[0].get_num()])
env_card_name_img[1] = canvas.create_image(341.5 * UNIT, 140 * UNIT, 
                    image=card_name_img[env.card[1].get_num()])
env_card_type_img[0] = canvas.create_image(249 * UNIT, 180 * UNIT, 
                    image=card_type_img[env.card[0].get_num()])
env_card_type_img[1] = canvas.create_image(335 * UNIT, 180 * UNIT, 
                    image=card_type_img[env.card[1].get_num()])

env_next_card_img[0] = canvas.create_image(64 * UNIT, 211 * UNIT, image=next_card_img1[env.nextcard[0].get_num()])
env_next_card_img[1] = canvas.create_image(99 * UNIT, 211 * UNIT, image=next_card_img1[env.nextcard[1].get_num()])
env_next_card_img[2] = canvas.create_image(135 * UNIT, 209.5 * UNIT, image=next_card_img2[env.nextcard[2].get_num()])
canvas.pack()

w.mainloop()