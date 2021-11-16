import pygame
import random
import keyboard
########################################

# 기본 초기화
pygame.init()

# 화면 크기 설정
screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

# FPS
clock = pygame.time.Clock()

# 폰트 설정
game_font = pygame.font.Font('source/D2Coding.ttf', 60)

# 창 제목
pygame.display.set_caption("무단 횡단")

#####################################
# 사용자 게임 초기와 (배경, 이미지, 좌표, 속도 등)

total_score = 0
temp_score = 0
total_level = 10

characterSize = (40, 70)
carSize = (25, 50)

is_right = None
is_left = None

ranking = []  #게임 기록 저장할 빈 리스트
names=[]    # 닉네임 저장할 빈 리스트

running = True  # 게임이 진행중인가 확인하는 변수
play = False

# 배경 이미지 및 효과음 불러오기
background = pygame.image.load("source/background.png")
readyScreen = pygame.image.load("source/readyScreen/readyscreen.png")
character = [pygame.transform.scale(pygame.image.load("source/character/walk (1).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (2).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (3).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (4).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (5).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (6).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (7).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (8).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (9).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (10).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (11).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (12).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (13).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (14).png"), characterSize),
             pygame.transform.scale(pygame.image.load("source/character/walk (15).png"), characterSize)]
carsUp = [pygame.transform.scale(pygame.image.load("source/cars/porcheup.png"), carSize),
          pygame.transform.scale(pygame.image.load("source/cars/benzup.png"), carSize),
          pygame.transform.scale(pygame.image.load("source/cars/f1up.png"), carSize),
          pygame.transform.scale(pygame.image.load("source/cars/volvoup.png"), carSize)]
carsDown = [pygame.transform.scale(pygame.image.load("source/cars/porchedown.png"), carSize),
            pygame.transform.scale(pygame.image.load("source/cars/benzdown.png"), carSize),
            pygame.transform.scale(pygame.image.load("source/cars/f1down.png"), carSize),
            pygame.transform.scale(pygame.image.load("source/cars/volvodown.png"), carSize)]
clear_sound = pygame.mixer.Sound("source/audio/stage_clear.wav")
crash_sound = pygame.mixer.Sound("source/audio/traffic_accident.wav")
start_icon = pygame.transform.scale(pygame.image.load("source/readyScreen/Start.png"), (100, 100))
quit_icon = pygame.transform.scale(pygame.image.load("source/readyScreen/quit.png"), (100, 100))

# 캐릭터 정보
walkCount = 1
character_size = character[walkCount].get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = 0
character_y_pos = screen_height / 2 - character_height / 2

# 캐릭터 이동 관련
to_x = 0
to_y = 0
character_speed = 0.5

# 장애물 클래스
object_list = list()
class object_class:
    object_image = pygame.image.load("source/cars/object.png")

    object_size = object_image.get_rect().size
    object_width = object_size[0]
    object_height = object_size[1]
    object_x_pos = 0
    object_y_pos = 0
    object_speed = 0
    object_rad = 0
    object_spawnpoint = None

    object_rect = object_image.get_rect()
    object_rect.left = object_x_pos
    object_rect.top = object_y_pos

    def __init__(self):
        self.object_speed = random.choice([0.2, 0.4, 0.6]) * dt
        a = random.randint(1, 100)
        if (a % 10 == 0):  # 10분의 1의 확률로 차량 소환
            self.object_spawnPoint = random.choice(['UP', 'DOWN'])
        else:
            self.object_spawnPoint = 'NONE'

        # 스폰 지점 설정
        if self.object_spawnPoint == 'UP':
            self.object_image = random.choice(carsDown)
            self.object_x_pos = random.choice([130, 200, 270, 340, 410, 480, 550])
            self.object_y_pos = - self.object_height
            self.object_rad = 1
        elif self.object_spawnPoint == 'DOWN':
            self.object_image = random.choice(carsUp)
            self.object_x_pos = random.choice([155, 225, 295, 365, 435, 505, 575])
            self.object_y_pos = screen_height
            self.object_rad = -1
        elif self.object_spawnPoint == 'NONE':
            self.object_x_pos = screen_width
            self.object_y_pos = screen_height

    def object_move(self):
        self.object_x_pos += 0
        self.object_y_pos += self.object_speed * self.object_rad
        global total_score

        if self.object_spawnPoint == 'UP':
            if self.object_y_pos > screen_height:
                object_list.remove(self)

        if self.object_spawnPoint == 'DOWN':
            if self.object_y_pos < -self.object_height:
                object_list.remove(self)

        if self.object_spawnPoint == 'NONE':
            object_list.remove(self)

    # 충돌 처리를 위한 장애물 위치 확인
    def object_collide(self):
        self.object_rect = self.object_image.get_rect()
        self.object_rect.left = self.object_x_pos
        self.object_rect.top = self.object_y_pos

# 버튼 클래스
class Button:
    def __init__(self, img, x, y, width, height, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            screen.blit(img, (x, y))
            if click[0]:
                pygame.time.wait(1)
                action()
        else:
            screen.blit(img, (x, y))


###############################
# 게임 중지 함수
def close():
    f = open("source/score.txt", 'w')
    for name, rank in zip(names, ranking):  # names와 ranking리스트에서 각 요소를
        w = name + ":" + str(rank) + "\n"  # :와 \n로 합쳐 한줄로 만든다.
        f.write(w)  # 파일에 한줄씩 기록
    f.close()

def quitgame():
    global running, play, names,ranking

    pygame.time.wait(10)
    play = False
    running = False
    pygame.quit()

def loading():
    f=open("source/score.txt",'r')
    lines=f.readlines() #파일 전체 내용 lines에 저장
    for line in lines:
        names.append(line[:line.index(":")])     #이름은 ranking의 0인덱스에
        ranking.append(int(line[line.index(":")+1:-1])) # 랭킹은 int형으로 ranking 0인덱스에 삽입 ( -1인 한 이유는 \n 제거 위함 )
    f.close()

def playgame():
    global play
    play=True

# 캐릭터 이동 함수
def character_Move():
    global walkCount, character_y_pos, character_x_pos, to_x, to_y, is_left, is_right

    if is_right == True:
        to_x = character_speed
        walkCount += 1
    elif is_left == True:
        to_x = -character_speed
        walkCount -= 1

    # walkCount가 범위를 넘어가면 초기화
    if walkCount > 13:
        walkCount = 0
    elif walkCount < 1:
        walkCount = 14


# 점수 계산 함수
def score_cal():  # 우측 도달 시 좌측으로 이동 및 점수 계산, 한 차선 당 1점
    global character_x_pos, total_score, temp_score
    if character_x_pos > 610:
        character_x_pos = 0
        clear_sound.play()
        total_score += 7
        temp_score = 0
    elif character_x_pos >= 550:
        temp_score = 6
    elif character_x_pos >= 480:
        temp_score = 5
    elif character_x_pos >= 410:
        temp_score = 4
    elif character_x_pos >= 340:
        temp_score = 3
    elif character_x_pos >= 270:
        temp_score = 2
    elif character_x_pos >= 200:
        temp_score = 1


# 범위 제한 함수
def boundary():
    global character_x_pos, character_y_pos
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height


# 출력 함수
def printer():
    # 배경 출력
    if play:
        screen.blit(background, (0, 0))
        # 캐릭터 출력
        screen.blit(character[walkCount], (character_x_pos, character_y_pos))
        # 장애물들 출력
        for i in object_list:
            i.object_move()
            screen.blit(i.object_image, (i.object_x_pos, i.object_y_pos))
    else:
        screen.blit(readyScreen, (0, 0))
        screen.blit(start_icon, (100, 455))
        screen.blit(quit_icon, (480, 455))


def crash():
    # 충돌 처리를 위한 캐릭터 위치 확인
    character_rect = character[walkCount].get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 충돌체크
    for i in object_list:
        i.object_collide()
        # 충돌하였다면 게임 종료
        if character_rect.colliderect(i.object_rect):
            crash_sound.play()
            print("충돌!!")

            if len(ranking) == 0 or ranking[0] < total_score+temp_score:  #최고기록이라면
                msg4 = game_font.render("콘솔에 이름입력", True, (0, 0, 0), (150, 150, 150))  # 검은색 글씨, 회색 바탕
                msg4_rect = msg4.get_rect()
                msg4_rect.center = (int(screen_width / 2), int(screen_height / 2) - 55)
                screen.blit(msg4, msg4_rect)
                pygame.display.update()
                name = input("\n닉네임을 입력하세요 >> ")  # 닉네임 입력받음
                names.insert(0, name)  # 이름리스트; 최고 기록이니까 0번째 인덱스에 삽입한다.
                ranking.insert(0, total_score+temp_score)  # 기록리스트; #최고 기록이니까 0번째 인덱스에 삽입한다.
                close()
                print("게임화면을 보세요.")

            while (1):
                screen.fill((255,255,255))
                # 게임 오버 메시지
                msg1 = game_font.render(" CRASH!! ", True, (0, 0, 0), (150, 150, 150))  # 검은색 글씨, 회색 바탕
                msg2 = game_font.render(f' SCORE : {total_score + temp_score}', True, (0, 0, 0), (150, 150, 150))
                msg3 = game_font.render(" PRESS \'esc\' TO QUIT. ", True, (0, 0, 0), (150, 150, 150))
                msg5 = game_font.render(f'최고기록 : {names[0]}의 {ranking[0]}점', True, (0, 0, 0), (150, 150, 150))
                # 메시지 출력위치를 가져온다
                msg1_rect = msg1.get_rect()
                msg2_rect = msg2.get_rect()
                msg3_rect = msg3.get_rect()
                msg5_rect = msg5.get_rect()
                # 택스트객체의 중심을 설정한 좌표로 한다.
                msg1_rect.center = (int(screen_width / 2), int(screen_height / 2) - 55)
                msg2_rect.center = (int(screen_width / 2), int(screen_height / 2))
                msg3_rect.center = (int(screen_width / 2), int(screen_height / 2) + 55)
                msg5_rect.center = (int(screen_width / 2), int(screen_height / 2) + 110)
                # 텍스트 객체를 출력한다.
                screen.blit(msg1, msg1_rect)
                screen.blit(msg2, msg2_rect)
                screen.blit(msg3, msg3_rect)
                screen.blit(msg5, msg5_rect)

                pygame.display.update()
                # esc 혹은 창닫기를 누르면 종료.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or keyboard.is_pressed('esc'):
                        quitgame()

# 실행문
loading()
while running:
    dt = clock.tick(60)
    printer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if 200 >= pos[0] >= 100 and 555 >= pos[1] >= 455:
                playgame()
            if 580 >= pos[0] >= 480 and 555 >= pos[1] >= 455:
                quitgame()
    while play:
        dt = clock.tick(60)
        print("fps : " + str(clock.get_fps()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    is_right = True
                    is_left = False
                elif event.key == pygame.K_LEFT:
                    is_right = False
                    is_left = True
                elif event.key == pygame.K_UP:
                    to_y -= character_speed
                elif event.key == pygame.K_DOWN:
                    to_y += character_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    is_right = False
                    is_left = False
                    to_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    to_y = 0

        # 캐릭터 이동
        character_Move()
        character_x_pos += to_x * dt
        character_y_pos += to_y * dt

        score_cal()  # 점수계산
        boundary()  # 캐릭터이동범위제한

        # 장애물 생성
        # 두바퀴 마다 장애물 한 씩 추가
        total_level = (int)(total_score / 14 + 10)
        if total_level >= len(object_list):
            object_list.append(object_class())

        # 배경 및 캐릭터 출력
        printer()
        # 충돌처리
        crash()
        # 게임화면 리프레쉬
        pygame.display.update()
    # 게임화면 리프레쉬
    pygame.display.update()

# pygame 종료
pygame.quit()
