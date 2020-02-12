import pygame
import datetime
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def quard(x, y, im, r):
    glBindTexture(GL_TEXTURE_2D, im)
    glBegin(GL_QUADS)
    glTexCoord2d(0, 0)
    glVertex2d(x, y)
    glTexCoord2d(0, 1)
    glVertex2d(x, y + r)
    glTexCoord2d(1, 1)
    glVertex2d(x + r, y + r)
    glTexCoord2d(1, 0)
    glVertex2d(x + r, y)
    glEnd()


def texture(s):
    img = pygame.image.load(s)
    textureData = pygame.image.tostring(img, "RGBA", 1)
    width = img.get_width()
    height = img.get_height()
    im = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, im)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.8)
    return im


def disptext(x, y, d, s, r):
    w = r
    h = r
    w1 = 0
    for i in range(str(s).__len__()):
        quard(x + w1, y, d[str(s[i])], r)
        w1 += w


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)


def menu(disp, tex):
    ackey = 1
    for i in range(15):
        for j in range(10):
            quard(disp[0] / 2 + i, disp[1] / 2 + j, tex, 1)


def take_screen_shot(display):
    time_take = time.asctime(time.localtime(time.time()))
    time_take = time_take.replace(" ", "_")
    time_take = time_take.replace(":", ".")
    file = "screenshots/" + time_take + ".png"
    pygame.image.save(display, file)



def main():
    pygame.init()
    display = (1920, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
    pygame.display.set_caption("PixelAdventures", "img/TEXTURE_HERO.png")
    gluPerspective(50, (display[0] / display[1]), 10, 1000.0)
    glTranslatef(-7.5, -7.5, -30)
    pygame.mixer.init()

    glRotatef(0, 0, 0, 0)
    x = 1
    y = 1
    z = -30
    ewt = ""
    w = 20
    h = 20
    x1 = 0
    y1 = 0
    um = 6

    texts = dict()
    for i in range(10):
        texts[str(i)] = texture("img/" + str(i) + ".png")
    for i in char_range("A", "Z"):
        texts[str(i)] = texture("img/" + str(i) + ".png")

    texts[' '] = texture("img/PROB.png")
    texts['.'] = texture("img/DOT.png")
    texts['-'] = texture("img/MIN.png")
    texts['@'] = texture("img/@.png")
    texts['!'] = texture("img/VOSKL.png")
    texts['/'] = texture("img/PROB.png")

    f = open("config/CONFIG.txt")
    f.readline()
    level = "config/" + f.readline()

    f = open(level, 'r')
    w = int(f.readline())
    h = int(f.readline())

    textures = dict()
    textures["GROUND"] = texture("img/TEXTURE_GROUND.png")
    textures["WALL"] = texture("img/WALL_TEXTURE.png")
    textures["WATER"] = texture("img/WATER_TEXTURE.png")
    textures["GRASS"] = texture("img/GRASS_TEXTURE.png")
    textures["COIN"] = texture("img/COIN_TEXTURE.png")
    textures["FINISH"] = texture("img/FINISH_TEXTURE.png")
    textures["MENU"] = texture("img/MENU.png")

    imhero = texture("img/TEXTURE_HERO.png")

    smw = 0
    smh = 0
    aa = [0] * w
    for i in range(w):
        aa[i] = [' '] * h
    i = 0
    j = 0
    for i in range(h):
        nn = f.read(1)
        for j in range(w):
            c = f.read(1)
            aa[j][w - i - 1] = c
    f.close()
    f = open("config/LEV01.txt", 'r')
    ab = [0] * w
    for i in range(w):
        ab[i] = [' '] * h
    i = 0
    j = 0
    for i in range(h):
        nn = f.read(1)
        for j in range(w):
            c = f.read(1)
            if c == '1':
                ab[j][w - i - 1] = c
    totalcoins = 0

    ac = (1, 2)
    choice = 3
    prov = False

    while True:
        for event1 in pygame.event.get():
            if event1.type == KEYDOWN:
                if event1.key == K_DOWN:
                    if choice != 1: choice -= 1
                elif event1.key == K_UP:
                    if choice != 3: choice += 1
                elif event1.key == K_y:
                    prov = True
                    if choice == 3:
                        break
                    elif choice == 1:
                        pygame.quit()
                        quit()
                elif event1.key == K_p:
                    take_screen_shot(pygame.display.get_surface())
                else:
                    prov = False
        if prov and (choice == 3):
            break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        menu(ac, textures["MENU"])
        disptext(ac[0] + 1, ac[1] + 5, texts, "WELCOME TO", 1)
        disptext(ac[0] + 2, ac[1] + 4, texts, "PIXEL ADV.", 1)
        quard(ac[0], ac[1] + choice, imhero, 0.5)
        disptext(ac[0] + 1, ac[1] + 3, texts, "START  Y  N", 0.5)
        disptext(ac[0] + 1, ac[1] + 1, texts, "EXIT GAME", 0.5)
        disptext(ac[0] + 1, ac[1] + 2, texts, "INFO", 0.5)
        disptext(ac[0] - 2, ac[1] - 2, texts, "CURRENT MAP " + level.upper(), 0.5)
        quard(4, 14, imhero, 1)
        p = 0
        for j in textures:
            p += 1
            quard(4 + p, 14, textures[j], 1)
        if prov and choice == 2:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            menu(ac, textures["MENU"])
            disptext(ac[0] - 4, ac[1] + 12, texts, "THIS GAME WAS CREATED", 1)
            disptext(ac[0] - 4, ac[1] + 11, texts, "BY MIKHAIL USHAKOV", 1)
            disptext(ac[0] - 4, ac[1] + 10, texts, "MIKHAIL.A.USHAKOV@GMAIL.COM", 0.5)
            disptext(ac[0] - 4, ac[1] + 9, texts, "IN GAME YOU CAN COLLECT SOME COINS", 0.5)
            disptext(ac[0] - 4, ac[1] + 8, texts, "AND FIND A FINISH", 0.5)
            disptext(ac[0] - 4, ac[1] + 7, texts, "SEE YOU BACK SOON AT", 0.5)
            disptext(ac[0] - 4, ac[1] + 6, texts, "PIXELSTUDIOS.ESY.ES", 0.5)
            disptext(ac[0] - 4, ac[1] + 5, texts, "WRITE ME SOMETHING GOOD!", 0.6)
            disptext(ac[0] - 4, ac[1] + 4, texts, "PS IF YOU WANT TO EXIT GAME", 0.5)
            disptext(ac[0] - 4, ac[1] + 3, texts, "TYPE ESC BUTTON", 0.5)
            disptext(ac[0] - 4, ac[1] + 2, texts, "YOU CAN  CHANGE LEVEL IN CONFIG.TXT", 0.5)
            disptext(ac[0] - 4, ac[1] + 1, texts, "ALSO DONT MISS README.TXT FILE", 0.5)
            pygame.display.flip()
            pygame.time.delay(10000)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            choice = 3
            prov = False
        pygame.time.wait(10)
        pygame.display.flip()

    ox = 1
    oy = 1
    time = 0
    while True:
        for event in pygame.event.get():
            ox = x
            oy = y
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYUP:
                ewt = ""
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    ewt = "keydown"
                elif event.key == K_UP:
                    ewt = "keyup"
                elif event.key == K_RIGHT:
                    ewt = "keyright"
                elif event.key == K_LEFT:
                    ewt = "keyleft"
                elif event.key == K_w:
                    ewt = "w"
                elif event.key == K_x:
                    ewt = "x"
                elif event.key == K_s:
                    ewt = "s"
                elif event.key == K_d:
                    ewt = "d"
                elif event.key == K_a:
                    ewt = "a"
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == K_p:
                    take_screen_shot(pygame.display.get_surface())

                if ewt == "keydown":
                    rx = 1
                    ry = 0
                    a = -1
                    if y >= 0 and aa[x][y - 1] != '0':
                        y -= 1
                elif ewt == "keyup":
                    rx = 1
                    ry = 0
                    a = 1
                    if y <= h and aa[x][y + 1] != '0':
                        y += 1
                elif ewt == "keyright":
                    rx = 0
                    ry = 1
                    a = -1
                    if x <= w and aa[x + 1][y] != '0':
                        x += 1
                elif ewt == "keyleft":
                    rx = 0
                    ry = 1
                    a = 1
                    if x >= 0 and aa[x - 1][y] != '0':
                        x -= 1
                elif ewt == "x":
                    if aa[x][y] == '!':
                        pygame.quit()
                        quit(x)
                    ewt = ""
        if aa[x][y] == "1":
            totalcoins += 1
            pygame.mixer.music.load("sound/Coin.mp3")
            pygame.mixer.music.play()
            aa[x][y] = " "
        if aa[x][y] == '~':
            if ox != x or oy != y:
                if not (pygame.mixer.music.get_busy()):
                    pygame.mixer.music.load("sound/WATER_SOUND.mp3")
                    pygame.mixer.music.play()
        if aa[x][y] == '.':
            if ox != x or oy != y:
                if not (pygame.mixer.music.get_busy()):
                    pygame.mixer.music.load("sound/GRASS_SOUND.mp3")
                    pygame.mixer.music.play()

        if aa[x][y] == ' ':
            if ox != x or oy != y:
                if not (pygame.mixer.music.get_busy()):
                    pygame.mixer.music.load("sound/SAND_SOUND.mp3")
                    pygame.mixer.music.play()
        if aa[x][y] == 'F':
            if ox != x or oy != y:
                pygame.mixer.music.load("sound/FINISH_SOUND.mp3")
                pygame.mixer.music.play()
                pygame.time.delay(8000)
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for i in range(w):
            for j in range(h):
                quard(i + um, j + um, textures["GROUND"], 1)
                if (i >= 0) & (j >= 0):
                    if aa[i][j] == '~':
                        quard(i + um, j + um, textures["GROUND"], 1)
                    if aa[i][j] == '0':
                        quard(i + um, j + um, textures["WALL"], 1)
                    if aa[i][j] == '~':
                        quard(i + um, j + um, textures["WATER"], 1)
                    if aa[i][j] == '.':
                        quard(i + um, j + um, textures["GRASS"], 1)
                    if aa[i][j] == '1':
                        quard(i + um, j + um, textures["COIN"], 1)
                    if aa[i][j] == "F":
                        quard(i + um, j + um, textures["FINISH"], 1)
                if (i == x) & (j == y):
                    quard(i + um, j + um, imhero, 1)
        if pygame.mouse.get_pos()[0] + 200 - smw / z >= display[0]:
            glTranslatef(-0.5, 0, 0)
            smw += 0.5
        if pygame.mouse.get_pos()[0] - 200 - smw / z <= 0:
            glTranslatef(0.5, 0, 0)
            smw -= 0.5
        if pygame.mouse.get_pos()[1] + 200 - smh / z >= display[1]:
            glTranslatef(0, 0.5, 0)
            smh -= 0.5
        if pygame.mouse.get_pos()[1] - 200 - smh / z <= 0:
            glTranslatef(0, -0.5, 0)
            smh += 0.5

        disptext(0 + smw, 0 + smh, texts, "COINS " + str(totalcoins), 0.5)
        disptext(0 + smw, 0 + 2 + smh, texts, "TIME " + str(time / 100), 0.5)
        pygame.display.flip()
        pygame.time.wait(10)
        time += 10


main()
