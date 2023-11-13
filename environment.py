import tkinter as tk
from tkinter import Button
from tkinter import PhotoImage
import time
import numpy as np
from PIL import ImageTk, Image
import os
import random

UNIT = 3 # 픽셀 수
HEIGHT = 250 # 세로
WIDTH = 400 # 가로
SLATE_LENGTH = 168 #석판 크기
SLATE_NUM = 6 # 석판 개수
CARD_NUMBER = 5 #대폭발, 지진, 폭풍우, 해일, 충격파
CARD_REIN = 10
SPECIAL_SLATE_NUMBER = 4

# PhotoImage list
slate = [[0 for j in range(SLATE_NUM)] for i in range(SLATE_NUM)]
card = [0 for _ in range(2)]
next_card = [0 for _ in range(3)]
card_change_img = [0 for _ in range(2)]
card_name_img = [0 for _ in range(CARD_NUMBER)]
card_type_img = [0 for _ in range(CARD_NUMBER)]
card_rein_img = [0 for _ in range(CARD_REIN)]
next_card_img1 = [0 for _ in range(CARD_NUMBER)]
next_card_img2 = [0 for _ in range(CARD_NUMBER)]
breakprob15img = [0 for _ in range(7)]
breakprob25img = [0 for _ in range(4)]
change_number_img = [0 for _ in range(10)]
special_slate_img = [0 for _ in range(SPECIAL_SLATE_NUMBER)]
special_slate_explanation_img = [0 for _ in range(SPECIAL_SLATE_NUMBER)]


selected_card = 2 #현재 고른 카드의 번호 / 0:왼쪽 1:오른쪽 2:선택안했음
change_num = 2 # 교체 가능 횟수
turn = 0
flag = 0 # 승리시 1

w = tk.Tk()
canvas = tk.Canvas(bg='white', height=HEIGHT * UNIT, width=WIDTH * UNIT)
w.title("Slate Game")
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
special_slate_explanationImg = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_explanation.png'))
                                               .resize((int(160 * UNIT), int(70 * UNIT))))
nextCardPanel = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/next_card_panel.png'))
                                   .resize((int(120 * UNIT), int(40 * UNIT))))
arrow = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/arrow.png'))
                           .resize((int(7.5 * UNIT), int(7.4 * UNIT))))
special_slate_img[0] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_replace.png'))
                              .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
special_slate_img[1] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_append.png'))
                              .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
special_slate_img[2] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_reinforce.png'))
                              .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
special_slate_img[3] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_duplicate.png'))
                              .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
special_slate_explanation_img[0] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_replace_explanation.png'))
                                               .resize((int(160 * UNIT), int(70 * UNIT))))
special_slate_explanation_img[1] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_append_explanation.png'))
                                               .resize((int(160 * UNIT), int(70 * UNIT))))
special_slate_explanation_img[2] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_reinforce_explanation.png'))
                                               .resize((int(160 * UNIT), int(70 * UNIT))))
special_slate_explanation_img[3] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, 'img/special_slate_duplicate_explanation.png'))
                                               .resize((int(160 * UNIT), int(70 * UNIT))))

probname = 'img/slate_breakprob'
cardname = 'img/card_name'
cardtype = 'img/card'
rein = 'img/rein'
nextcardtype = 'img/next_card'
tail = '.png'
change_number = 'img/change_number'

for i in range(0, 7):
    str1 = probname + str(100 - i * 15) + tail
    breakprob15img[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str1))
                              .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))
for i in range(0, 4):
    str1 = probname + str(100 - i * 25) + tail
    breakprob25img[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str1))
                              .resize((int(SLATE_LENGTH * UNIT / SLATE_NUM), int(SLATE_LENGTH * UNIT / SLATE_NUM))))

for i in range(0, CARD_NUMBER):
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

for i in range(0, CARD_REIN):
    str1 = rein + str(i) + tail
    card_rein_img[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str1))
                           .resize((int(12 * UNIT), int(19 * UNIT))))
for i in range(0, 10):
    str1 = change_number + str(i) + tail
    change_number_img[i] = ImageTk.PhotoImage(Image.open(os.path.join(current_dir, str1))
                                       .resize((int(80 * UNIT), int(20 * UNIT))))
    
#석판 생성
slate_img = [[0 for j in range(SLATE_NUM)] for i in range(SLATE_NUM)]
for row in range(0,SLATE_NUM):
    for col in range(0,SLATE_NUM):
        slate[row][col] = slateImg
        slate_img[row][col] = canvas.create_image(16 * UNIT + SLATE_LENGTH * UNIT / (2 * SLATE_NUM) + SLATE_LENGTH * UNIT * row / SLATE_NUM, 
                            16 * UNIT + SLATE_LENGTH * UNIT / (2 * SLATE_NUM) + SLATE_LENGTH * UNIT * col / SLATE_NUM, 
                            image=slate[row][col])
        
#카드 생성
card_img = [0 for _ in range(2)]
card[0] = card_exampleImg
card[1] = card_exampleImg
card_img[0] = canvas.create_image(249 * UNIT, 170 * UNIT, image=card[0])
card_img[1] = canvas.create_image(335 * UNIT, 170 * UNIT, image=card[1])

#카드 교체 생성
card_change = [0 for _ in range(2)]
card_change[0] = card_changeImg
card_change[1] = card_changeImg
card_change_img[0] = canvas.create_image(249 * UNIT, 230 * UNIT, image=card_change[0])
card_change_img[1] = canvas.create_image(335 * UNIT, 230 * UNIT, image=card_change[1])

#특수 석판 설명 생성
special_slate_explanation = canvas.create_image(292 * UNIT, 55 * UNIT, image=special_slate_explanationImg)

#교체 가능 횟수 생성
change_numbering = canvas.create_image(292 * UNIT, 110 * UNIT, image=change_number_img[change_num])

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

turn_text = canvas.create_text(292 * UNIT, 10 * UNIT, text=str(turn) + " turn", fill="black", font=("Helvetica ",str(10 * UNIT), " bold"))

def click(event):
    global flag
    if flag == 0:
        click_card(event)
        click_slate(event)
        click_card_change(event)

hoverflag = 0
def hover(event):
    global selected_card
    global hoverflag
    global flag
    if flag == 0:
        if selected_card != 2:
            if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
            and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
                hoverflag = 1
                hover_slate(event)
            else:
                if hoverflag == 1:
                    hoverflag = 0
                    not_hover_slate(event)

def release(event):
    release_slate(event)

def motion(event):
    motion_slate(event)

#석판 클릭 인식 함수
def click_slate(event):
    global selected_card
    global flag
    global turn
    nextturn = 0
    if selected_card != 2:
        if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
            and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
            for row in range(0,SLATE_NUM):
                for col in range(0,SLATE_NUM):
                    if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                        and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                        if env.slate[row][col].num >0:
                            env.slate[env.special_slate_x][env.special_slate_y].num = 1
                            canvas.itemconfig(slate_img[env.special_slate_x][env.special_slate_y], image=slateImg)
                            canvas.itemconfig(slate_img[row][col], image=slate_clickImg)
                            slate:Slate = env.use_card(row,col).slate
                            canvas.itemconfig(change_numbering, image=change_number_img[env.change_num])
                            env.reinforcement_card()
                            for y in range(0,SLATE_NUM):
                                for x in range(0,SLATE_NUM):
                                    print(slate[x][y].num, end=' ')
                                    if slate[x][y].num == 0 :
                                        canvas.itemconfig(slate_img[x][y], image=slate_breakImg)
                                    elif slate[x][y].num == 1:
                                        canvas.itemconfig(slate_img[x][y], image=slateImg)
                                print()
                            cards_img_switch()
                            if selected_card == 0:
                                canvas.itemconfig(card_img[0], image=card_exampleImg)
                                selected_card = 2
                            if selected_card == 1:
                                canvas.itemconfig(card_img[1], image=card_exampleImg)
                                selected_card = 2
                            nextturn = 1
                            print("select slate : ", end='')
                            print(row, end=' ')
                            print(col, end='\n\n')
                            time.sleep(0.1)
                            turn += 1
                            canvas.itemconfig(turn_text, text = str(turn) + " turn")
            total = 0
            for row in range(0, SLATE_NUM):
                for col in range(0, SLATE_NUM):
                    if env.slate[row][col].num > 0:
                        total += 1
            print("total : ", total)
            if total == 0:
                print("ending!!")
                flag = 1
                env.finish()
            else:
                while nextturn == 1:
                    x = random.randint(0, SLATE_NUM - 1)
                    y = random.randint(0, SLATE_NUM - 1)
                    if env.slate[x][y].num == 1:
                        env.special_slate_num = random.randint(2, SPECIAL_SLATE_NUMBER + 1)
                        env.slate[x][y].num = env.special_slate_num
                        env.special_slate_x = x
                        env.special_slate_y = y
                        canvas.itemconfig(slate_img[x][y], image=special_slate_img[env.slate[x][y].num - 2])
                        canvas.itemconfig(special_slate_explanation, image=special_slate_explanation_img[env.slate[x][y].num - 2])
                        nextturn = 0
                        break
    print("-----------------------------")

#석판 클릭하면서 움직임 인식 함수
def motion_slate(event):
    if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
        and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
        for row in range(0,SLATE_NUM):
            for col in range(0,SLATE_NUM):
                if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                    and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                    canvas.itemconfig(slate_img[row][col], image=slate_clickImg)
                    time.sleep(0.1)

#석판 호버 인식 함수
def hover_slate(event):
    global selected_card
    global turn
    for row in range(0,SLATE_NUM):
        for col in range(0,SLATE_NUM):
            if env.slate[row][col].num == 1:
                canvas.itemconfig(slate_img[row][col], image=slateImg)
            if env.slate[row][col].num == 0:
                canvas.itemconfig(slate_img[row][col], image=slate_breakImg)
    if env.slate[env.special_slate_x][env.special_slate_y].num > 1:
        canvas.itemconfig(slate_img[env.special_slate_x][env.special_slate_y], image=special_slate_img[env.slate[env.special_slate_x][env.special_slate_y].num - 2])
    for row in range(0,SLATE_NUM):
        for col in range(0,SLATE_NUM):
            if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                if env.slate[row][col].num > 0 :
                    canvas.itemconfig(slate_img[row][col], image=breakprob15img[0])
                    if env.card[selected_card].num == 0:
                        for i in range(1, 8):
                            if i - env.card[selected_card].reinforcementStep < 7:
                                if col - i >= 0 and row - i >= 0:
                                    if env.slate[row - i][col - i].num > 0:
                                        canvas.itemconfig(slate_img[row - i][col - i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if row + i < SLATE_NUM and col - i >= 0:
                                    if env.slate[row + i][col - i].num > 0:
                                        canvas.itemconfig(slate_img[row + i][col - i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if row - i >= 0 and col + i < SLATE_NUM:
                                    if env.slate[row - i][col + i].num > 0:
                                        canvas.itemconfig(slate_img[row - i][col + i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if col + i < SLATE_NUM and row + i < SLATE_NUM:
                                    if env.slate[row + i][col + i].num > 0:
                                        canvas.itemconfig(slate_img[row + i][col + i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                    elif env.card[selected_card].num == 1:
                        for i in range(1, 8):
                            if i - env.card[selected_card].reinforcementStep < 7:
                                if row - i >= 0:
                                    if env.slate[row - i][col].num > 0:
                                        canvas.itemconfig(slate_img[row - i][col], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if row + i < SLATE_NUM:
                                    if env.slate[row + i][col].num > 0:
                                        canvas.itemconfig(slate_img[row + i][col], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                    elif env.card[selected_card].num == 2:
                        for i in range(1, 8):
                            if i - env.card[selected_card].reinforcementStep < 7:
                                if col - i >= 0:
                                    if env.slate[row][col - i].num > 0:
                                        canvas.itemconfig(slate_img[row][col - i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if col + i < SLATE_NUM:
                                    if env.slate[row][col + i].num > 0:
                                        canvas.itemconfig(slate_img[row][col + i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                    elif env.card[selected_card].num == 3:
                        for i in range(1, 8):
                            if i - env.card[selected_card].reinforcementStep < 7:
                                if row - i >= 0:
                                    if env.slate[row - i][col].num > 0:
                                        canvas.itemconfig(slate_img[row - i][col], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if row + i < SLATE_NUM:
                                    if env.slate[row + i][col].num > 0:
                                        canvas.itemconfig(slate_img[row + i][col], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if col - i >= 0:
                                    if env.slate[row][col - i].num > 0:
                                        canvas.itemconfig(slate_img[row][col - i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                                if col + i < SLATE_NUM:
                                    if env.slate[row][col + i].num > 0:
                                        canvas.itemconfig(slate_img[row][col + i], image=breakprob15img[max(0, i - env.card[selected_card].reinforcementStep)])
                    elif env.card[selected_card].num == 4:
                        for x in range(0, SLATE_NUM):
                            for y in range(0, SLATE_NUM):
                                distance = max(abs(row - x), abs(col - y))
                                if distance == 0:
                                    if env.slate[x][y].num > 0:
                                        canvas.itemconfig(slate_img[x][y], image=breakprob25img[0])
                                elif distance < env.card[selected_card].reinforcementStep + 2:
                                    if env.slate[x][y].num > 0:
                                        canvas.itemconfig(slate_img[x][y], image=breakprob25img[max(0, 2 + distance - env.card[selected_card].reinforcementStep)])


def not_hover_slate(event):
    for row in range(0,SLATE_NUM):
        for col in range(0,SLATE_NUM):
            if env.slate[row][col].num == 1:
                canvas.itemconfig(slate_img[row][col], image=slateImg)
            elif env.slate[env.special_slate_x][env.special_slate_y].num > 1:
                canvas.itemconfig(slate_img[env.special_slate_x][env.special_slate_y], image=special_slate_img[env.slate[env.special_slate_x][env.special_slate_y].num - 2])

#석판 클릭 해제 인식 함수
def release_slate(event):
    if (event.x > 16 * UNIT and event.x < 16 * UNIT + SLATE_LENGTH * UNIT
        and event.y > 16 * UNIT and event.y < 16 * UNIT + SLATE_LENGTH * UNIT):
        for row in range(0,SLATE_NUM):
            for col in range(0,SLATE_NUM):
                if (event.x > 16 * UNIT + SLATE_LENGTH * UNIT * row / SLATE_NUM and event.x < 16 * UNIT + SLATE_LENGTH * UNIT * (row + 1) / SLATE_NUM 
                    and event.y > 16 * UNIT + SLATE_LENGTH * UNIT * col / SLATE_NUM and event.y < 16 * UNIT + SLATE_LENGTH * UNIT * (col + 1) / SLATE_NUM) :
                    canvas.itemconfig(slate_img[row][col], image=slate_hoverImg)
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
    if(env.change_num > 0):
        if (event.x > 219 * UNIT and event.x < 279 * UNIT
            and event.y > 220 * UNIT and event.y < 240 * UNIT):
            env.change_num -= 1
            canvas.itemconfig(change_numbering, image=change_number_img[env.change_num])
            env.change_card(0)
            print("change card1")
            env.reinforcement_card()
            cards_img_switch()
            if selected_card == 0:
                canvas.itemconfig(card_img[0], image=card_exampleImg)
                selected_card = 2
            if selected_card == 1:
                canvas.itemconfig(card_img[1], image=card_exampleImg)
                selected_card = 2
        if (event.x > 305 * UNIT and event.x < 365 * UNIT
            and event.y > 220 * UNIT and event.y < 240 * UNIT):
            env.change_num -= 1
            canvas.itemconfig(change_numbering, image=change_number_img[env.change_num])
            env.change_card(1)
            print("change card2")
            env.reinforcement_card()
            cards_img_switch()
            if selected_card == 0:
                canvas.itemconfig(card_img[0], image=card_exampleImg)
                selected_card = 2
            if selected_card == 1:
                canvas.itemconfig(card_img[1], image=card_exampleImg)
                selected_card = 2

def cards_img_switch():
    canvas.itemconfig(env_card_rein_img[0], image=card_rein_img[env.card[0].get_rein()])
    canvas.itemconfig(env_card_rein_img[1], image=card_rein_img[env.card[1].get_rein()])
    canvas.itemconfig(env_card_type_img[0], image=card_type_img[env.card[0].get_num()])
    canvas.itemconfig(env_card_type_img[1], image=card_type_img[env.card[1].get_num()])
    canvas.itemconfig(env_card_name_img[0], image=card_name_img[env.card[0].get_num()])
    canvas.itemconfig(env_card_name_img[1], image=card_name_img[env.card[1].get_num()])
    canvas.itemconfig(env_next_card_img[0], image=next_card_img1[env.nextcard[0].get_num()])
    canvas.itemconfig(env_next_card_img[1], image=next_card_img1[env.nextcard[1].get_num()])
    canvas.itemconfig(env_next_card_img[2], image=next_card_img2[env.nextcard[2].get_num()])

#마우스 이벤트
canvas.bind("<Button-1>", click)
canvas.bind("<Motion>", hover)
#canvas.bind("<ButtonRelease-1>", release)
#canvas.bind("<B1-Motion>", motion)

canvas.pack()

class Slate:
    def __init__(self, x, y):
        self.num = 1
        self.x = x
        self.y = y
    
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

    def use_card(self, slate:Slate, x, y):
        slate[x][y].num = 0
        if self.num == 0:
            for i in range(1, 8):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0 and y - i >= 0:
                        slate[x - i][y - i].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM and y - i >= 0:
                        slate[x + i][y - i].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0 and y + i < SLATE_NUM:
                        slate[x - i][y + i].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM and y + i < SLATE_NUM:
                        slate[x + i][y + i].num = 0
        elif self.num == 1:
            for i in range(1, 8):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0:
                        slate[x - i][y].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM:
                        slate[x + i][y].num = 0
        elif self.num == 2:
            for i in range(1, 8):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y - i >= 0:
                        slate[x][y - i].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y + i < SLATE_NUM:
                        slate[x][y + i].num = 0
        elif self.num == 3:
            for i in range(1, 8):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y - i >= 0:
                        slate[x][y - i].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y + i < SLATE_NUM:
                        slate[x][y + i].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0:
                        slate[x - i][y].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM:
                        slate[x + i][y].num = 0
        elif self.num == 4:
            for row in range(0, SLATE_NUM):
                for col in range(0, SLATE_NUM):
                    distance = max(abs(row - x), abs(col - y))
                    if distance < self.reinforcementStep + 2:
                        if random.randint(0, 100) <= 25 * (self.reinforcementStep - distance + 2):
                            slate[row][col].num = 0
        return slate
    
class State:
    def __init__(self, slate, card, nextcard, change_num):
        self.slate = slate
        self.card = [card[0], card[1], nextcard[0], nextcard[1], nextcard[2]]
        self.change_num = change_num

class Env:
    def __init__(self):
        global flag
        global change_num
        self.slate = [[0 for j in range(SLATE_NUM)] for i in range(SLATE_NUM)]
        self.card = [0 for _ in range(0,2)]
        self.nextcard = [0 for _ in range(0,3)]
        for row in range(0,SLATE_NUM):
            for col in range(0,SLATE_NUM):
                self.slate[row][col] = Slate(row,col)
        self.card[0] = Card()
        self.card[1] = Card()
        while self.card[1].num == self.card[0].num:
            self.card[1] = Card()
        self.nextcard[0] = Card()
        self.nextcard[1] = Card()
        self.nextcard[2] = Card()
        self.change_num = change_num
        self.special_slate_x = -1
        self.special_slate_y = -1
        self.special_slate_num = 0
    
    def finish(self):
        if flag == 1:
            print("end")
            canvas.create_text(WIDTH * UNIT / 2, HEIGHT * UNIT / 2, 
                                text="WIN", fill="black", font=("Helvetica 250 bold"))
            canvas.pack()

    def use_card(self, x, y):
        global selected_card
        self.slate = self.card[selected_card].use_card(self.slate, x, y)
        if self.slate[env.special_slate_x][env.special_slate_y].num == 0:
            print('Break Special Slate : (', env.special_slate_x, ', ', env.special_slate_y, '), num : ', self.special_slate_num, end=' ')
            self.break_special_slate(selected_card)
            if self.special_slate_num == 2 or self.special_slate_num == 3:
                self.card[selected_card] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
        else:
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
        return State(self.slate, self.card, self.nextcard, self.change_num)
    
    def reinforcement_card(self):
        print("reinforcement")
        while self.card[0].get_num() == self.card[1].get_num():
            tmp = self.card[0].get_rein()
            if self.card[0].get_rein() < self.card[1].get_rein():
                tmp = self.card[1].get_rein()
            self.card[0].set_rein(min(9, tmp + 1))
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
        return State(self.slate, self.card, self.nextcard, self.change_num)
    
    def break_special_slate(self, use_card_num):
        if self.special_slate_num == 2: # replace
            print('replace', end=' ')
            total = 0
            for row in range(0, SLATE_NUM):
                for col in range(0, SLATE_NUM):
                    if self.slate[row][col].num > 0:
                        total += 1
                        self.slate[row][col].num = 0
            while total > 0:
                x = random.randint(0, SLATE_NUM - 1)
                y = random.randint(0, SLATE_NUM - 1)
                if self.slate[x][y].num == 0:
                    self.slate[x][y].num = 1
                    total -= 1
        elif self.special_slate_num == 3: # append
            print('append')
            if env.change_num < 9:
                env.change_num += 1
        elif self.special_slate_num == 4: # reinforce
            print('reinforce')
            if use_card_num == 0:
                self.card[1].reinforcementStep += 1
                self.card[0] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
            else:
                self.card[0].reinforcementStep += 1
                self.card[1] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
        elif self.special_slate_num == 5: # duplicate
            print('duplicate')
            if use_card_num == 0:
                self.card[1] = self.card[0]
                self.card[0] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
            else:
                self.card[0] = self.card[1]
                self.card[1] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()

    def current_state(self):
        return State(self.slate, self.card, self.nextcard, self.change_num)


class Agent:
    def __init__(self):
        self.q_table = np.zeros((5, 7, 4))
        self.eps = 0.9
        self.alpha = 0.01
        self.change_rate = 0.1
    
    def select_action(self, slate, card, change_num):
        coin = random.random()
        card_change_flag = False
        card_change_num = 0
        card_num = 0
        x = 0
        y = 0

        if coin < self.eps:
            if(self.change_rate < random.random()):
                x = random.randint(0, SLATE_NUM - 1)
                y = random.randint(0, SLATE_NUM - 1)
                while slate[x][y].num == 0:
                    x = random.randint(0, SLATE_NUM - 1)
                    y = random.randint(0, SLATE_NUM - 1)
                card_num = random.randint(0,1)
            else:
                card_change_num = random.randint(0,1)
        else:
            x, y, card_num, card_change_num, card_change_flag = self.step(self, slate, card, change_num)
        return x, y, card_num, card_change_num, card_change_flag
    
    def step(self, slate, card, change_num):
        self

    def anneal_eps(self):
        self.eps -= 0.03
        self.eps = max(self.eps, 0.1)

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

#canvas.create_text(WIDTH * UNIT / 2, HEIGHT * UNIT / 2, text="WIN", fill="black", font=("Helvetica 250 bold"))

canvas.pack()

w.mainloop()
