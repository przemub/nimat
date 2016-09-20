#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1366, 768))
clock = pygame.time.Clock()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

CasinoBackground = Background('tlo.png', [0, 0])
stone = pygame.image.load('kam1.png')

tips = [ u"Wybierz stertę, z której będziesz brał kamienie.",
         u"Weź więcej kamieni z tej sterty lub zakończ ruch.",
         u"Wygrasz, jeżeli jako ostatni wykonasz ruch!",
         u"Myślę…",
         u"Już wiem!",
         u"Wygrałem! Xoruj sprawniej!",
         u"Pokonałeś mnie! Teraz zmierz się z mistrzem.",
         u"Pokonałeś mnie! Gdybym ja zaczynał, nie byłoby tak łatwo…",
         ""
       ]

class Game:
    heaps = [6, 6, 6]
    active = -1
    curtip = 0
    end = False

    def __init__(self, mistrz):
        self.heaps = [6, 6, 6]
        self.active = -1
        self.curtip = 0
        self.end = False
        self.mistrz = mistrz

        if mistrz:
            pygame.display.set_caption("Gra z mistrzem - NiMat 0.1 kappa")
        else:
            pygame.display.set_caption("Gra z RNG - NiMat 0.1 kappa")

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if not event.button == 1:
                        continue

                    x, y = event.pos

                    if (x > 470 and x < 900 and
                        y > 530 and y < 650):
                        if (self.end):
                            return

                        if (self.active == -1):
                            continue

                        self.move()
                        if (self.end):
                            continue

                        self.active = -1
                        self.curtip = 2

                    if (y < 200 or y > 200 + 75*3 + 20 or x < 60):
                        continue

                    curheap = x // (120*3 + 2*10)
                    if curheap > 3:
                        continue

                    if self.active == -1 and self.heaps[curheap] > 0:
                        self.active = curheap
                    if self.active != curheap:
                        continue

                    if self.heaps[curheap] > 0:
                        self.heaps[curheap] -= 1

                    if self.curtip == 0:
                        self.curtip = 1

                    if sum(self.heaps) == 0:
                        self.end = True
                        if self.mistrz:
                            self.curtip = 7
                        else:
                            self.curtip = 6

            self.draw_game()

    def move(self):
        self.curtip = 3
        self.draw_game()

        pygame.time.delay(random.randint(200, 2200))

        self.curtip = 4
        self.draw_game()

        neheaps = []
        for i in range(3):
            if self.heaps[i] > 0:
                neheaps.append(i)

        randomly = True

        move = 0
        moveheap = 0
        if self.mistrz:
            for i in neheaps:
                for j in range(1, self.heaps[i]+1):
                    self.heaps[i] -= j
                    if (self.heaps[0] ^ self.heaps[1] ^ self.heaps[2] == 0):
                        move = j
                        moveheap = i
                        self.heaps[i] += j
                        randomly = False
                        break
                    self.heaps[i] += j

                if move != 0:
                    break

        if randomly:
            moveheap = random.choice(neheaps)
            move = random.randint(1, self.heaps[moveheap])

        pygame.time.delay(random.randint(400, 600))
        for i in range(move):
            self.heaps[moveheap] -= 1
            pygame.time.delay(random.randint(400, 600))
            self.draw_game()
        pygame.time.delay(random.randint(400, 600))

        if sum(self.heaps) == 0:
            self.end = True
            self.curtip = 5

    def draw_game(self):
            deltat = clock.tick(30)

            screen.fill([255, 255, 255])
            screen.blit(CasinoBackground.image, CasinoBackground.rect)

            font = pygame.font.SysFont("monospace", 35)
            ftip = font.render(tips[self.curtip], 1, (255,255,0))
            screen.blit(ftip, (1366/2 - ftip.get_rect().width/2, 60))

            Game.heap(1, self.heaps[0])
            Game.heap(2, self.heaps[1])
            Game.heap(3, self.heaps[2])

            pygame.draw.rect(screen, (0, 0, 0),
                            (1366/2 - 420/2, 768 - 130 - 110, 420, 120))
            pygame.draw.rect(screen, (255, 255, 0),
                            (1366/2 - 400/2, 768 - 120 - 110, 400, 100))

            if self.end:
                btn1 = font.render("Jeszcze raz", 1, (0,0,0))
            else:
                btn1 = font.render(u"Zakończ ruch", 1, (0,0,0))
            screen.blit(btn1, (1366/2 - btn1.get_rect().width/2,
                                768 - 130 - 110 + 60 - btn1.get_rect().height/2))

            pygame.display.flip()

    @staticmethod
    def heap(size, number):
        xs = 120
        ys = 75

        x1 = 30*size + 380*(size-1) + 60
        y1 = 200

        x2 = x1 + xs*3 + 2*10
        y2 = y1 + ys*3 + 2*10

        xc = (x1 + x2)/2
        yc = (y1 + y2)/2

        mx = 10
        my = 10

        def one(y):
            screen.blit(stone, (xc - xs/2, y))

        def two(y):
            screen.blit(stone, (xc - xs/2 - (xs/2 + 10), y))
            screen.blit(stone, (xc - xs/2 + (xs/2 + 10), y))

        def three(y):
            screen.blit(stone, (xc - xs/2, y))
            screen.blit(stone, (xc - xs/2 - (xs + 10), y))
            screen.blit(stone, (xc + xs/2 + 10, y))

        if (number == 1):
            one(yc + ys/2 + my)
        elif (number == 2):
            two(yc + ys/2 + my)
        elif (number == 3):
            three(yc + ys/2 + my)
        elif (number == 4):
            one(yc - ys/2)
            three(yc + (ys/2 + my))
        elif (number == 5):
            two(yc - ys/2)
            three(yc + (ys/2 + my))
        elif (number == 6):
            one(yc - ys/2 - (ys + my))
            two(yc - ys/2)
            three(yc + ys/2 + my)


def main():
    pygame.display.set_caption("NiMat 0.1 kappa")

    while True:
        # Ograniczenie liczby klatek
        deltat = clock.tick(30)

        # Wejście
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if not event.button == 1:
                    continue

                x, y = event.pos
                
                if (x < 470 or x > 810):
                    continue

                if (y > 290 and y < 410):
                    gra = Game(True)
                    gra.loop()
                elif (y > 450 and y < 570):
                    gra = Game(False)
                    gra.loop()

        screen.fill([255, 255, 255])
        screen.blit(CasinoBackground.image, CasinoBackground.rect)

        font = pygame.font.SysFont("monospace", 90)
        gamma = font.render("NiMat 0.1 kappa", 1, (255,255,0))
        screen.blit(gamma, (1366/2 - gamma.get_rect().width/2, 100))

        font = pygame.font.SysFont("monospace", 35)

        pygame.draw.rect(screen, (0, 0, 0),
                        (1366/2 - 420/2, 768/2 - 120/2 - 80 + 50, 420, 120))
        pygame.draw.rect(screen, (255, 255, 0),
                        (1366/2 - 400/2, 768/2 - 100/2 - 80 + 50, 400, 100))

        btn1 = font.render("Zagraj z mistrzem", 1, (0,0,0))
        screen.blit(btn1, (1366/2 - btn1.get_rect().width/2, 768/2 - btn1.get_rect().height/2 - 80 + 50))

        pygame.draw.rect(screen, (0, 0, 0),
                        (1366/2 - 420/2, 768/2 - 120/2 + 80 + 50, 420, 120))
        pygame.draw.rect(screen, (255, 255, 0),
                        (1366/2 - 400/2, 768/2 - 100/2 + 80 + 50, 400, 100))

        btn2 = font.render("Zagraj z RNG", 1, (0,0,0))
        screen.blit(btn2, (1366/2 - btn2.get_rect().width/2, 768/2 - btn2.get_rect().height/2 + 80 + 50))

        font = pygame.font.SysFont("monospace", 18)
        left = font.render(u"Copyright (c) 2016 Przemysław Buczkowski. All rights reversed.",
                            1, (255,255,0))
        gith = font.render("https://github.com/przemub/nimat", 1, (255,255,0))
        screen.blit(left, (1366-700, 768-60))
        screen.blit(gith, (1366-370, 768-40))

        pygame.display.flip()

if __name__ == "__main__":
    main()

