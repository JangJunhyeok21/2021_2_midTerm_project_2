import pygame

pygame.init()

#화면 크기 설정
screen_width=480
screen_height=640
screen=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("test")

#배경 이미지 불러오기
background=pygame.image.load("background.png")

running=True #게임이 진행중인가 확인하는 변수
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.blit(background,(0,0))
    #screen.fill(0,0,255)

    pygame.display.update() #게임화면 리프레쉬(c++콘솔게임에서 지우고 새로 그리는 고런 너낌)

#pygame 종료
pygame.quit()