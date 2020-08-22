import math
import pygame
from pygame.locals import *
import sys
import random
from time import sleep

BLACK = (0, 0, 0)

padWidth = 480  # 게임 화면의 가로 크기
padHeight = 640 # 게임 화면의 세로 크기
rockImage = ['images/rock01.png', 'images/rock02.png', 'images/rock03.png', 'images/rock04.png', 'images/rock05.png',
             'images/rock06.png', 'images/rock07.png', 'images/rock08.png', 'images/rock09.png', 'images/rock10.png',
             'images/rock11.png', 'images/rock12.png', 'images/rock13.png', 'images/rock14.png', 'images/rock15.png',
             'images/rock16.png', 'images/rock17.png', 'images/rock18.png', 'images/rock19.png', 'images/rock20.png',
             'images/rock21.png', 'images/rock22.png', 'images/rock23.png', 'images/rock24.png', 'images/rock25.png',
             'images/rock26.png', 'images/rock27.png', 'images/rock28.png', 'images/rock29.png', 'images/rock30.png']
# explosionSound = ['sounds/explosion01.wav', 'sounds/explosion02.wav', 'sounds/explosion03.wav', 'sounds/explosion04.wav']
explosionSound = ['sounds/explosion_YJ.wav', 'sounds/explosion2_YJ.wav', 'sounds/explosion03.wav', 'sounds/explosion04.wav']
shotCount = 0
rockPassed = 0
level = 1

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

# 텍스트 메세지 생성
def draw_text(text, font, surface, x, y ,main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

# 운석을 맞춘 개수 계산
def writeScore(count):
    global gamePad

    font = pygame.font.Font('font/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석수: ' + str(count), True, (220, 220, 220))
    gamePad.blit(text, (10, 0))

# 운석이 화면 아래로 통과한 개수
def writePassed(count):
    global gamePad

    font = pygame.font.Font("font/NanumGothic.ttf", 20)
    text = font.render('놓친 운석 수: ' + str(count) + ' / 5', True, (250, 20, 20))
    gamePad.blit(text, (316, 0))

# 게임 메시지 출력
def writeMessage(text):
    global gamePad, level

    game_image = pygame.image.load('images/game_screen_YJ.png')
    gamePad.blit(game_image, [0, 0])

    textfont = pygame.font.Font('font/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (250, 20, 20))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    textfont = pygame.font.Font('font/NanumGothic.ttf', 50)
    text = textfont.render('Level: {}'.format(level), True, (250, 20, 20))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/1.6)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()   # 배경 음악 정지

# 전투기가 운석과 충돌했을 때 메시지 출력
def crash():
    global gamePad, gameOverSound

    writeMessage('전투기 파괴!')
    gameOverSound.play()    # 게임 오버 사운드 재생
    sleep(2)
    pygame.mixer.music.play(-1) # 배경 음악 재생
    return 'game_screen'

# 게임 오버 메시지 보이기
def gameOver():
    global gamePad, gameOverSound

    writeMessage('게임 오버!')
    gameOverSound.play()    # 게임 오버 사운드 재생
    sleep(2)
    pygame.mixer.music.play(-1) # 배경 음악 재생
    return 'game_screen'

def levelup(level):
    global gamePad, levelupSound

    game_image = pygame.image.load('images/game_screen_YJ.png')
    gamePad.blit(game_image, [0, 0])

    textfont = pygame.font.Font('font/NanumGothic.ttf', 80)
    text = textfont.render('LEVEL UP!!!', True, (250, 20, 20))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)

    textfont = pygame.font.Font('font/NanumGothic.ttf', 50)
    text = textfont.render('Level: {}'.format(level), True, (250, 20, 20))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/1.6)
    gamePad.blit(text, textpos)

    pygame.display.update()
    pygame.mixer.music.stop()   # 배경 음악 정지

    levelupSound.play()
    sleep(3)
    pygame.mixer.music.play(-1)

def draw_repeating_background(background_img):
    global gamePad
    background_rect = background_img.get_rect()
    for i in range(int(math.ceil(padWidth / background_rect.width))):
        for j in range(int(math.ceil(padHeight / background_rect.height))):
            gamePad.blit(background_img, Rect(i * background_rect.width,
                                             j * background_rect.height,
                                             background_rect.width,
                                             background_rect.height))

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameOverSound, levelupSound

    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting(ft.바둥이♥)')                        # 게임 이름
    pygame.display.set_icon(pygame.image.load('images/missile.png'))# 아이콘 설정
    background = pygame.image.load('images/background.png')         # 배경 그림
    fighter = pygame.image.load('images/fighter.png')               # 전투기 그림
    missile = pygame.image.load('images/missile.png')               # 미사일 그림
    explosion = pygame.image.load('images/explosion.png')           # 폭발 그림
    pygame.mixer.music.load('sounds/music.wav')                     # 배경 음악
    pygame.mixer.music.play(-1)                                     # 배경 음악 재생
    # missileSound = pygame.mixer.Sound('sounds/missile.wav')    # 미사일 사운드
    missileSound = pygame.mixer.Sound('sounds/missile_YJ.wav')    # 미사일 사운드
    gameOverSound = pygame.mixer.Sound('sounds/gameover_YJ.wav')  # 게임 오버 사운드
    levelupSound = pygame.mixer.Sound('sounds/levelup2_YJ.wav')     # 레벨 업 사운드
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, background, fighter, missile, explosion,\
        missileSound, shotCount, rockPassed, level

    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []      # 미사일 좌표 리스트

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size     # 운석 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    # 전투기 미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    paused = False
    while not onGame:
        pygame.display.update()  # 게임 화면을 다시 그림
        clock.tick(60)  # 게임 화면의 초당 프레임수(FPS)를 60으로 설정

        if paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        pygame.mouse.set_visible(False)
                if event.type in [pygame.QUIT]:
                    return 'quit'
        else:
            draw_repeating_background(background)       # 배경 화면 그리기

            for event in pygame.event.get():
                if event.type in [pygame.KEYDOWN]:
                    if event.key == pygame.K_LEFT:      # 전투기를 왼쪽으로 이동
                        fighterX -= 5

                    elif event.key == pygame.K_RIGHT:   # 전투기를 오른쪽으로 이동
                        fighterX += 5

                    elif event.key == pygame.K_SPACE:   # 미사일 발사
                        missileSound.play()             # 미사일 사운드 재생
                        missileX = x + fighterWidth / 2
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])

                    elif event.key == pygame.K_p:
                        paused = not paused
                        if paused:
                            transp_surf = pygame.Surface((padWidth, padHeight))
                            transp_surf.set_alpha(150)
                            gamePad.blit(transp_surf, transp_surf.get_rect())
                            pygame.mouse.set_visible(True)
                            draw_text('일시 정지',
                                      pygame.font.Font('font/NanumGothic.ttf', 60),
                                                       gamePad, padWidth / 2, padHeight / 2, (250, 250, 20))
                            pygame.display.update()

                if event.type in [pygame.KEYUP]:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        fighterX = 0
                if event.type in [pygame.QUIT]:
                    return 'quit'

            # drawObject(background, 0, 0)

            # 전투기 위치 재조정
            x += fighterX
            if x < 0:
                x = 0
            elif x > padWidth - fighterWidth:
                x = padWidth - fighterWidth

            # 전투기가 운석과 충돌했는지 체크
            if y < rockY + rockHeight:
                # if (rockX > x and rockX < x + fighterWidth) or \
                #         (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                if rockX + rockWidth > x and rockX < x + fighterWidth:
                    return crash()

            drawObject(fighter, x, y)   # 전투기를 게임 화면의 (x, y)좌표에 그림

            if rockPassed == 5:     # 운석 5개 놓치면 게임 오버
                return gameOver()

            # 미사일 발사 화면에 그리기
            if len(missileXY) != 0:
                for i, bxy in enumerate(missileXY):     # 미사일 요소에 대해 반복함
                    bxy[1] -= 10        # 미사일의 y좌표 -10 (위로 이동)
                    missileXY[i][1] = bxy[1]

                    # 미사일이 운석을 맞췄을 경우
                    if bxy[1] < rockY:
                        if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                            missileXY.remove(bxy)
                            isShot = True
                            shotCount += 1

                    if bxy[1] <= 0:     # 미사일이 화면 밖을 벗어나면
                        try:
                            missileXY.remove(bxy)   # 미사일 제거
                        except:
                            pass

            if len(missileXY) != 0:
                for bx, by in missileXY:
                    drawObject(missile, bx, by)

            writeScore(shotCount)   # 운석을 맞춘 점수 표시

            rockY += rockSpeed      # 운석이 아래로 움직임

            # 운석이 지구로 떨어진 경우
            if rockY > padHeight:
                # 새로운 운석(랜덤)
                rock = pygame.image.load(random.choice(rockImage))
                rockSize = rock.get_rect().size
                rockWidth = rockSize[0]
                rockHeight = rockSize[1]
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = 0
                rockPassed += 1

            writePassed(rockPassed)     # 놓친 운석 수 표시

            # 운석을 맞춘 경우
            if isShot:
                # 운석 폭발
                drawObject(explosion, rockX, rockY)     # 운석 폭발 그리기
                destroySound.play()

                # 새로운 운석 (랜덤)
                rock = pygame.image.load(random.choice(rockImage))
                rockSize = rock.get_rect().size
                rockWidth = rockSize[0]
                rockHeight = rockSize[1]
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = 0
                destroySound = pygame.mixer.Sound(random.choice(explosionSound))
                isShot = False

                # 운석을 맞추면 운석 속도 증가
                rockSpeed_up = 0.05
                rockSpeed += rockSpeed_up
                if rockSpeed >= 9:
                    rockSpeed = 9

                print(rockSpeed)

                if abs(rockSpeed - round(rockSpeed)) < rockSpeed_up / 2:
                    level = int(rockSpeed)
                    if level == 9:
                        levelup('만렙 달성!!')
                        return 'game_screen'
                    levelup(level)

            drawObject(rock, rockX, rockY)      # 운석 그리기

            # gamePad.fill(BLACK)
            # pygame.display.update()


    return 'game_screen'       # pygame 종료

def game_screen():
    global gamePad, shotCount, rockPassed
    pygame.mouse.set_visible(True)

    start_image = pygame.image.load('images/game_screen_YJ.png')
    gamePad.blit(start_image, [0, 0])

    draw_text('파괴한 운석수: {}'.format(shotCount),
              pygame.font.Font('font/NanumGothic.ttf', 20), gamePad, 80, 20, (20, 20, 250))
    draw_text('놓친 운석수: {} / 5'.format(rockPassed),
              pygame.font.Font('font/NanumGothic.ttf', 20), gamePad, 390, 20, (250, 20, 20))
    draw_text('지구를 지켜라!',
              pygame.font.Font('font/NanumGothic.ttf', 70), gamePad,
              padWidth / 2, padHeight / 3.4, (220, 220, 220))
    draw_text('바둥이 사랑해♥',
              pygame.font.Font('font/NanumGothic.ttf', 40), gamePad,
              padWidth / 2, padHeight / 2.5, (240, 240, 240))
    draw_text("SPACEBAR 버튼이나 'S'키를 누르면 게임이 시작됩니다.",
              pygame.font.Font('font/NanumGothic.ttf', 20), gamePad,
              padWidth / 2, padHeight / 2.0, (240, 240, 240))
    draw_text("게임을 종료하려면 'Q'키를 누르세요.",
              pygame.font.Font('font/NanumGothic.ttf', 20), gamePad,
              padWidth / 2, padHeight / 1.8, (240, 240, 240))
    draw_text("게임 중 일시 정지는 'P'키를 누르세요.",
              pygame.font.Font('font/NanumGothic.ttf', 20), gamePad,
              padWidth / 2, padHeight / 1.6, (240, 240, 240))
    draw_text("※ 우주선은 키보드 좌우로 조작이 가능하며,",
              pygame.font.Font('font/NanumGothic.ttf', 20), gamePad,
              padWidth / 2, padHeight - 80, (250, 20, 20))
    draw_text("미사일은 SPACEBAR로 발사가 가능합니다.",
              pygame.font.Font('font/NanumGothic.ttf', 20), gamePad,
              padWidth / 2, padHeight - 50, (250, 20, 20))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return 'quit'
            elif event.key == pygame.K_s or event.key == pygame.K_SPACE:
                return 'play'
        if event.type in [pygame.QUIT]:
            return 'quit'

    return 'game_screen'

def main_loop():
    initGame()
    action = 'game_screen'
    while action != 'quit':
        if action == 'game_screen':
            action = game_screen()
        elif action == 'play':
            action = runGame()

    pygame.quit()
    sys.exit()

main_loop()