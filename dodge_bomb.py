from encodings.punycode import T
import os
import random
import sys
from tkinter import RIGHT
from turtle import screensize
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, 5), pg.K_RIGHT: (5, 0), pg.K_LEFT: (-5, 0)}

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    wid, hgt = True, True
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        wid = False
    elif obj_rct.top > HEIGHT or obj_rct.bottom < 0:
        hgt = False
    return wid, hgt

def gameover(screen: pg.Surface) -> None:
    """
    こうかとんに爆弾が着弾した際に、
    1. 画面をブラックアウトし、
    2. 泣いているこうかとん画像と
    3. 「Game Over」の文字列を
    4. 5秒間表示させ、
    5. display.update()する
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    go_img.set_alpha(180)
    go_img.fill((0, 0, 0))
    pg.draw.rect(go_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    screen.blit(go_img, (0, 0))

    gokk_img = pg.image.load("fig/8.png")
    gokk1_rct = gokk_img.get_rect(center=(WIDTH/2-300, HEIGHT/2))
    gokk2_rct = gokk_img.get_rect(center=(WIDTH/2+300, HEIGHT/2))
    screen.blit(gokk_img, gokk1_rct)
    screen.blit(gokk_img, gokk2_rct)

    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rct)

    pg.display.update()
    time.sleep(5)



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    vx = 5
    vy = -5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        screen.blit(bb_img, bb_rct)

        bb_rct.move_ip([vx, vy])
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        bx, by = check_bound(bb_rct)
        if not bx:
            vx *= -1
        elif not by:
            vy *= -1
        
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
