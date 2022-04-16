import config
from config import *
import pygame as pg


class Map():
    def __init__(self, screen, start_time):
        self.screen = screen
        self.start_time = start_time

    def draw(self):
        self.screen.fill((30, 30, 30))

        pg.draw.circle(self.screen, (0, 100, 0), FENCE_CENTER, FENCE_RADIUS, 0)
        pg.draw.circle(self.screen, (165, 42, 42), FENCE_CENTER, FENCE_RADIUS, 3)  # rysowanie ogrodzenia

        pg.draw.rect(self.screen, (165, 42, 42),
                     pg.Rect(TUNNEL_POINT.x + 8, TUNNEL_POINT.y, TUNNEL_SIZE.x - 10,
                             TUNNEL_SIZE.y), 6)
        pg.draw.rect(self.screen, (165, 42, 42),
                     pg.Rect(DESTINATION_POINT.x, DESTINATION_POINT.y, DESTINATION_SIZE.x,
                             DESTINATION_SIZE.y), 6)
        pg.draw.rect(self.screen, (0, 100, 0),
                     pg.Rect(TUNNEL_POINT.x, TUNNEL_POINT.y, TUNNEL_SIZE.x, TUNNEL_SIZE.y))
        pg.draw.rect(self.screen, (0, 100, 0),
                     pg.Rect(DESTINATION_POINT.x, DESTINATION_POINT.y, DESTINATION_SIZE.x,
                             DESTINATION_SIZE.y))

        font = pg.font.SysFont('comicsans', 30)
        label = font.render('SCORE: ' + str(config.SCORE), True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, 100))
        label = font.render('TIME: ' + str(int((pg.time.get_ticks() - self.start_time) / 1000)) + 's', True,
                            (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, 130))
        label = font.render('GEN_TIME: ' + str(config.GEN_TIME) + 's', True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, 160))

        label = font.render('Space - next gen', True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, HEIGHT/2+150))
        label = font.render('n - gen_time down', True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, HEIGHT / 2 + 180))
        label = font.render('m - gen_time up', True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, HEIGHT / 2 + 210))
        label = font.render('p - new scenario', True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, HEIGHT / 2 + 240))

        label = font.render('s - show', True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, HEIGHT / 2 + 270))
        label = font.render('d - dont show', True, (255, 255, 255))
        self.screen.blit(label, (WIDTH / 2, HEIGHT / 2 + 300))
