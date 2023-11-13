import numpy as np
import random

SLATE_NUM = 6 # 석판 개수
CARD_NUMBER = 5 # 대폭발, 지진, 폭풍우, 해일, 충격파

selected_card = 2 #현재 고른 카드의 번호 / 0:왼쪽 1:오른쪽 2:선택안했음
change_num = 2 # 카드 교체 가능 횟수
turn = 0 # 턴 수
flag = 0 # 승리시 1

class Slate:
    def __init__(self, x, y):
        self.num = 1 # 석판 상태 / 0:파괴된 석판 1:파괴되지 않은 석판
        self.x = x # 석판의 x좌표
        self.y = y # 석판의 y좌표
    
class Card:
    def __init__(self):
        global flag
        self.num = random.randint(0, CARD_NUMBER - 1) # 카드 번호 / 0:대폭발 1:지진 2:폭풍우 3:해일 4:충격파
        self.reinforcementStep = 0 # 카드 강화 수치

    # env에서 카드 사용했을 때 호출하는 함수
    def use_card(self, slate:Slate, x, y): # 현재 석판, 카드 사용 x좌표, 카드 사용 y좌표
        slate[x][y].num = 0 # 카드 사용한 석판 파괴
        if self.num == 0: # 카드가 대폭발일 때
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
        elif self.num == 1: # 카드가 지진일 때
            for i in range(1, 8):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x - i >= 0:
                        slate[x - i][y].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if x + i < SLATE_NUM:
                        slate[x + i][y].num = 0
        elif self.num == 2: # 카드가 폭풍우일 때
            for i in range(1, 8):
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y - i >= 0:
                        slate[x][y - i].num = 0
                if random.randint(0, 100) >= 15 * (i - self.reinforcementStep):
                    if y + i < SLATE_NUM:
                        slate[x][y + i].num = 0
        elif self.num == 3: # 카드가 해일일 때
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
        elif self.num == 4: # 카드가 충격파일 때
            for row in range(0, SLATE_NUM):
                for col in range(0, SLATE_NUM):
                    distance = max(abs(row - x), abs(col - y))
                    if distance < self.reinforcementStep + 2:
                        if random.randint(0, 100) <= 25 * (self.reinforcementStep - distance + 2):
                            slate[row][col].num = 0
        return slate # 카드를 사용한 후 변경된 석판 리턴
    
class State: # 상태 클래스, 다음 상태를 저장할 때 사용
    def __init__(self, slate, card, nextcard, change_num): # 석판(n*n), 카드(2), 다음 카드(3), 카드 교체 가능 횟수
        self.slate = slate # 석판
        self.card = [card[0], card[1], nextcard[0], nextcard[1], nextcard[2]] # 카드, 다음카드
        self.change_num = change_num # 카드 교체 가능 횟수
    
    def show_state(self): # 상태를 print하는 함수
        for row in range(0, SLATE_NUM):
            for col in range(0, SLATE_NUM):
                print(self.slate[row][col].num, end=' ')
            print()
        print('card[0] : ', self.card[0].num, ' ', self.card[0].reinforcementStep)
        print('card[1] : ', self.card[1].num, ' ', self.card[1].reinforcementStep)
        print('nextcard[0] : ', self.card[2].num)
        print('nextcard[1] : ', self.card[3].num)
        print('nextcard[2] : ', self.card[4].num)
        print('change_num : ', self.change_num)

class Env: # 환경 클래스
    def __init__(self):
        global flag
        global change_num
        global turn
        self.slate = [[0 for j in range(SLATE_NUM)] for i in range(SLATE_NUM)] # 석판
        self.card = [0 for _ in range(0, 2)] # 카드
        self.nextcard = [0 for _ in range(0, 3)] # 다음 카드
        for row in range(0, SLATE_NUM):
            for col in range(0, SLATE_NUM):
                self.slate[row][col] = Slate(row, col)
        self.card[0] = Card()
        self.card[1] = Card()
        while self.card[1].num == self.card[0].num: # 손에 있는 카드 중복 방지
            self.card[1] = Card()
        self.nextcard[0] = Card()
        self.nextcard[1] = Card()
        self.nextcard[2] = Card()
        self.change_num = change_num
        self.special_slate_x = -1 # 특수 석판 x좌표, 0턴에는 특수 석판이 없으므로 -1
        self.special_slate_y = -1 # 특수 석판 y좌표, 0턴에는 특수 석판이 없으므로 -1
        self.special_slate_num = 0 # 특수 석판 번호, 2~5까지가 유의미한 수, 0턴에는 특수 석판이 없으므로 0
        # 상태
        self.state = State(self.slate, [self.card[0], self.card[1]], [self.nextcard[0], self.nextcard[1], self.nextcard[2]], self.change_num)
    
    def finish(self): # 끝내는 함수
        if flag == 1:
            print("end")

    def use_card(self, x, y): # 카드 사용 함수, 사용한 좌표를 인자로 가짐
        global selected_card # 선택된 카드(0 or 1)

        # 선택된 카드를 Card클래스의 use_card를 호출해서 석판을 파괴, 파괴 후 변경된 석판을 다시 env에 저장
        self.slate = self.card[selected_card].use_card(self.slate, x, y)

        if self.slate[self.special_slate_x][self.special_slate_y].num == 0: # 특수 석판이 파괴됐다면
            print('Break Special Slate : (', self.special_slate_x, ', ', self.special_slate_y, ')', end=' ')
            self.break_special_slate(selected_card) # 사용한 카드(0 or 1)을 인자로 함수 호출

            # 특수 석판이 재배치 or 추가일 때 / 다른 특수 석판은 break_special_slate에서 해결하기 때문
            if self.special_slate_num == 2 or self.special_slate_num == 3:
                self.card[selected_card] = self.nextcard[2] # 사용한 카드 자리를 다음 카드로 교체
                self.nextcard[2] = self.nextcard[1] # 카드 당김
                self.nextcard[1] = self.nextcard[0] # 카드 당김
                self.nextcard[0] = Card() # 카드 새로 만듦
        else: # 특수 석판이 파괴되지 않았다면
            self.card[selected_card] = self.nextcard[2]
            self.nextcard[2] = self.nextcard[1]
            self.nextcard[1] = self.nextcard[0]
            self.nextcard[0] = Card()
        return State(self.slate, self.card, self.nextcard, self.change_num) # 변경된 상태를 State클래스로 리턴
    
    def reinforcement_card(self): # 카드 강화 함수
        print("reinforcement")
        while self.card[0].num == self.card[1].num: # 양쪽 카드가 같으면 계속 강화
            tmp = self.card[0].reinforcementStep # 카드 강화 수치 저장
            if self.card[0].reinforcementStep < self.card[1].reinforcementStep:
                tmp = self.card[1].reinforcementStep
            self.card[0].reinforcementStep = min(9, tmp + 1) # 카드 수치 +1 , 카드 강화 수치 최댓값 = 9
            self.card[1] = self.nextcard[2]
            self.nextcard[2] = self.nextcard[1]
            self.nextcard[1] = self.nextcard[0]
            self.nextcard[0] = Card()
    
    def change_card(self, num): # 카드 교체 함수, num이 교체할 카드
        self.card[num] = self.nextcard[2]
        self.nextcard[2] = self.nextcard[1]
        self.nextcard[1] = self.nextcard[0]
        self.nextcard[0] = Card()
        return State(self.slate, self.card, self.nextcard, self.change_num)
    
    def break_special_slate(self, use_card_num): # 특수 석판이 파괴됐을 때 호출되는 함수
        if self.special_slate_num == 2: # replace
            print('replace', end=' ')
            total = 0
            # 석판 수 총합 구하기
            for row in range(0, SLATE_NUM):
                for col in range(0, SLATE_NUM):
                    if self.slate[row][col].num > 0:
                        total += 1
                        self.slate[row][col].num = 0
            while total > 0:# 석판 배치
                x = random.randint(0, SLATE_NUM - 1)
                y = random.randint(0, SLATE_NUM - 1)
                if self.slate[x][y].num == 0:
                    self.slate[x][y].num = 1
                    total -= 1
        elif self.special_slate_num == 3: # append
            print('append')
            if self.change_num < 9: # 카드 교체 가능 횟수 최댓값 = 9
                self.change_num += 1
        elif self.special_slate_num == 4: # reinforce
            print('reinforce')
            if use_card_num == 0: # 사용한 카드가 0자리 카드라면
                self.card[1].reinforcementStep += 1 # 1자리 카드 강화
                self.card[0] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
            else: # 사용한 카드가 1자리 카드라면
                self.card[0].reinforcementStep += 1 # 0자리 카드 강화
                self.card[1] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
        elif self.special_slate_num == 5: # duplicate
            print('duplicate')
            if use_card_num == 0: # 사용한 카드가 0자리 카드라면
                self.card[1] = self.card[0] # 1자리 카드를 사용한 카드로 복제
                self.card[0] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
            else: # 사용한 카드가 1자리 카드라면
                self.card[0] = self.card[1] # 0자리 카드를 사용한 카드로 복제
                self.card[1] = self.nextcard[2]
                self.nextcard[2] = self.nextcard[1]
                self.nextcard[1] = self.nextcard[0]
                self.nextcard[0] = Card()
    
    # 현재 상태를 리턴하는 함수
    def current_state(self):
        return self.state
    
    # 현재 상태를 show하는 함수
    def show_current_state(self):
        self.state.show_state()

    # 파괴되지 않은 석판 개수를 리턴하는 함수
    def total_slate(self):
        total = 0
        for row in range(0, SLATE_NUM):
            for col in range(0, SLATE_NUM):
                if self.slate[row][col] > 0:
                    total += 1
        print("남은 석판 수 : ", total) # 파괴되지 않은 석판 개수를 출력, 불필요하면 주석처리
        return total
        
    # reset 함수
    def reset(self):
        for row in range(0, SLATE_NUM):
            for col in range(0, SLATE_NUM):
                self.slate[row][col] = Slate(row, col)
        self.card[0] = Card()
        self.card[1] = Card()
        while self.card[1].num == self.card[0].num:
            self.card[1] = Card()
        self.nextcard[0] = Card()
        self.nextcard[1] = Card()
        self.nextcard[2] = Card()
        self.change_num = 2
        self.special_slate_x = -1
        self.special_slate_y = -1
        self.special_slate_num = 0
        self.flag = 0
        self.turn = 0


class Agent: # Agent 클래스
    def __init__(self):
        self.q_table = np.zeros((5, 7, 4)) #테이블
        self.eps = 0.9 # epsilon-greedy에 사용할 변수
        self.alpha = 0.01
        self.gamma = 0.9
        self.change_rate = 0.1 # 카드 교체를 선택할 확률
    
    # 액션 선택 함수
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
        # 사용할 x좌표, 사용할 y좌표, 사용할 카드 번호, 교체할 카드 번호, 카드 교체 여부
        # card_change_flag가 False라면 교체하지 않았다는 뜻이므로 사용되는 변수는 x, y, card_num
        # card_change_falg가 True라면 교체한다는 뜻이므로 사용되는 변수는 card_change_num
        return x, y, card_num, card_change_num, card_change_flag
    
    def step(self, slate, card, change_num):
        self

    def anneal_eps(self): # denying-epsilon greedy
        self.eps -= 0.03
        self.eps = max(self.eps, 0.1)

def main():
    env = Env()
    env.show_current_state()

if __name__ == '__main__':
    main()
