import pygame

pygame.init()

#화면 크기 설정
screen_width=480
screen_height=640
screen=pygame.display.set_mode((screen_width,screen_height))

#FPS
clock=pygame.time.Clock()

pygame.display.set_caption("test") #창 제목

#배경 이미지 불러오기
background=pygame.image.load("background.png")
character=pygame.image.load("character.png")

character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=(screen_width/2)-(character_width/2)
character_y_pos=screen_height-character_height

to_x=0
to_y=0

character_speed = 0.6

#오브젝트
object=pygame.image.load("object.png")

object_size=object.get_rect().size
object_width=object_size[0]
object_height=object_size[1]
object_x_pos=(screen_width/2)-(object_width/2)
object_y_pos=(screen_height/2)-(object_height / 2)

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
#배경 및 캐릭터 출력
    screen.blit(background,(0,0))
    screen.blit(object, (object_x_pos, object_y_pos))
    screen.blit(character,(character_x_pos,character_y_pos))

    #충돌처리
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    object_rect=object.get_rect()
    object_rect.left=object_x_pos
    object_rect.top=object_y_pos

    #충돌체크
    if character_rect.colliderect(object_rect):
        print("충돌했어요.")
        running=False

    pygame.display.update() #게임화면 리프레쉬(c++콘솔게임에서 지우고 새로 그리는 고런 너낌)

#pygame 종료
pygame.quit()