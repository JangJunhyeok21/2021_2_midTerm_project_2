import pygame
import random
########################################
#기본 초기화
pygame.init()

#화면 크기 설정
screen_width=700
screen_height=700
screen=pygame.display.set_mode((screen_width,screen_height))

#FPS
clock=pygame.time.Clock()

# 창 제목
pygame.display.set_caption("test")

#####################################
#사용자 게임 초기와 (배경, 이미지, 좌표, 속도 등)

total_score=0
level_control=10
total_level=0
total_level_list=[10,30,50,70]

#배경 이미지 불러오기
background=pygame.image.load("background.png")
character=pygame.image.load("character.png")

#캐릭터 정보
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=0
character_y_pos=screen_height/2 - character_height/2

#캐릭터 이동 관련
to_x=0
to_y=0
character_speed = 0.6

#장애물 클래스
object_list = list()
class object_class:
    object_image=pygame.image.load("object.png")

    object_size=object_image.get_rect().size
    object_width=object_size[0]
    object_height=object_size[1]
    object_x_pos=0
    object_y_pos=0
    object_speed=0
    object_rad=0
    object_spawnpoint = None

    object_rect = object_image.get_rect()
    object_rect.left = object_x_pos
    object_rect.top = object_y_pos

    def __init__(self):
        self.object_speed = random.choice([3.0, 6.0, 9.0])
        a=random.randint(1,100)
        if (a%10==0):
            self.object_spawnPoint = random.choice(['UP', 'DOWN'])
        else:
            self.object_spawnPoint = 'NONE'

        # 스폰 지점 설정
        if self.object_spawnPoint == 'UP':
            self.object_x_pos = random.choice([130, 200, 270, 340, 410, 480, 550])
            self.object_y_pos = - self.object_height
            self.object_rad = 1
        elif self.object_spawnPoint == 'DOWN':
            self.object_x_pos = random.choice([200, 270, 340, 410, 480, 550])
            self.object_y_pos = screen_height
            self.object_rad = -1
        elif self.object_spawnPoint == 'NONE':
            self.object_x_pos = screen_width
            self.object_y_pos = screen_height

    def object_move(self):
        self.object_x_pos += 0
        self.object_y_pos += self.object_speed * self.object_rad
        global total_score

        def boundary_UP():
            if self.object_y_pos < -self.object_height:
                return True

        def boundary_DOWN():
            if self.object_y_pos > screen_height:
                return True

        if self.object_spawnPoint == 'UP':
            if boundary_DOWN():
                object_list.remove(self)

        if self.object_spawnPoint == 'DOWN':
            if boundary_UP():
                object_list.remove(self)

        if self.object_spawnPoint == 'NONE':
            object_list.remove(self)

    def object_collide(self):
        self.object_rect = self.object_image.get_rect()
        self.object_rect.left = self.object_x_pos
        self.object_rect.top = self.object_y_pos


###############################33
#실행문
running=True #게임이 진행중인가 확인하는 변수
while running:
    dt=clock.tick(60)
    print("fps : "+str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                to_x+=character_speed
            elif event.key == pygame.K_LEFT:
                to_x-=character_speed
            elif event.key == pygame.K_UP:
                to_y-=character_speed
            elif event.key == pygame.K_DOWN:
                to_y+=character_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x=0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y=0
#캐릭터 이동
    character_x_pos+=to_x * dt
    character_y_pos+=to_y * dt

#범위 제한
    if character_y_pos<0:
        character_y_pos=0
    elif character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos = screen_width - character_width
    elif character_y_pos>screen_height-character_height:
        character_y_pos = screen_height - character_height

    #장애물 생성
    if total_score >= total_level_list[total_level]:
        total_level += 1

    if total_level + level_control >= len(object_list):
        object_list.append(object_class())

    #충돌처리
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    #충돌체크
    for i in object_list:
        i.object_collide()
        if character_rect.colliderect(i.object_rect):
            print("충돌")
            print("점수 : ", total_score)
            running = False

        # 배경 및 캐릭터 출력
    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    for i in object_list:
        i.object_move()
        screen.blit(i.object_image, (i.object_x_pos, i.object_y_pos))

    pygame.display.update() #게임화면 리프레쉬(c++콘솔게임에서 지우고 새로 그리는 고런 너낌)

#pygame 종료
pygame.quit()