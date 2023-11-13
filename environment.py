import numpy as np
import random

UNIT = 3 # 픽셀 수
HEIGHT = 250 # 세로
WIDTH = 400 # 가로
SLATE_LENGTH = 168 #석판 크기
SLATE_NUM = 6 # 석판 개수
CARD_NUMBER = 5 #대폭발, 지진, 폭풍우, 해일, 충격파
CARD_REIN = 10
SPECIAL_SLATE_NUMBER = 4

selected_card = 2 #현재 고른 카드의 번호 / 0:왼쪽 1:오른쪽 2:선택안했음
change_num = 2 # 교체 가능 횟수
turn = 0
flag = 0 # 승리시 1
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

    def use_card(self, x, y):
        global selected_card
        self.slate = self.card[selected_card].use_card(self.slate, x, y)
        if self.slate[self.special_slate_x][self.special_slate_y].num == 0:
            print('Break Special Slate : (', self.special_slate_x, ', ', self.special_slate_y, ')', end=' ')
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
        return State(self.slate, self.card, self.nextcard, self.change_num)
    
    def reinforcement_card(self):
        print("reinforcement")
        while self.card[0].num == self.card[1].num:
            tmp = self.card[0].reinforcementStep
            if self.card[0].reinforcementStep < self.card[1].reinforcementStep:
                tmp = self.card[1].reinforcementStep
            self.card[0].reinforcementStep = min(9, tmp + 1)
            self.card[1] = self.nextcard[2]
            self.nextcard[2] = self.nextcard[1]
            self.nextcard[1] = self.nextcard[0]
            self.nextcard[0] = Card()
    
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
            if self.change_num < 9:
                self.change_num += 1
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
    
    def show_current_state(self):
        for row in range(0,SLATE_NUM):
            for col in range(0,SLATE_NUM):
                print(self.slate[row][col].num, end=' ')
            print()
        print('card[0] : ', self.card[0].num, ' ', self.card[0].reinforcementStep)
        print('card[1] : ', self.card[1].num, ' ', self.card[1].reinforcementStep)
        print('nextcard[0] : ', self.nextcard[0].num)
        print('nextcard[1] : ', self.nextcard[1].num)
        print('nextcard[2] : ', self.nextcard[2].num)


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

def main():
    env = Env()
    while flag == 0:
        env.show_current_state()

if __name__ == '__main__':
    main()
