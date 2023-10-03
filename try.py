import pygame as pg
import random
import sys

pg.init()

class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((30, 200))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scroll_speed = 8
    
    def update(self):
        self.rect.left -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()

screen = pg.display.set_mode((1000, 400))
clock = pg.time.Clock()
pipe_group = pg.sprite.Group()

last_pipe = 0
pipe_freq = 1000

def create_pipes():
    global last_pipe  
    current_time = pg.time.get_ticks()
    if current_time - last_pipe > pipe_freq:
        pipe1 = Pipe(1000, random.randint(250, 300))
        pipe2 = Pipe(1000 + 31, random.randint(250, 300))
        pipe3 = Pipe(1000 + 62, random.randint(250, 300))
        
        pipe_group.add(pipe1, pipe2, pipe3)
        
        last_pipe = current_time

while True:
    clock.tick(60)
    screen.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    
    create_pipes() 
    pipe_group.update()
    pipe_group.draw(screen)
    pg.display.update()

pg.quit()
