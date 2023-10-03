#!/usr/bin/env python3
import pygame as pg
import sys
import random


class Dino(pg.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.image = pg.Surface((50, 70))
        self.image.fill((0, 255, 125))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0
        self.w, self.h = self.rect.size
        self.clicked = False
        self.screen_width, self.screen_height = screen
        self.dino_strength = -15
        self.gravity = 0.5

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.clicked:
            self.clicked = True
            self.jump()
        
        self.apply_gravity()
        
        if self.rect.bottom >= self.screen_height:
            self.clicked = False
            self.rect.bottom = self.screen_height
            self.velocity = 0
        
    def jump(self):
        self.velocity = self.dino_strength

    def apply_gravity(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
    

class Cact(pg.sprite.Sprite):
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
        
class GameEngine:
    def __init__(self, width, height, fps, title: str = "Dino Game"):
        self.title = title
        self.width = width
        self.height = height
        self.screen_size = (self.width, self.height)
        self.fps = fps
        self.dino_group = pg.sprite.Group()
        self.cact_group = pg.sprite.Group()
        self.running = False
        self.game_over = False
        self.last_cact = 0 
        self.cact_frequency = 1000
        self.score = 0
        self.pass_cact = False
    def init(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
            self.create_cacts()
            self.collision()

    def quit(self):
        pg.quit()
        sys.exit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def update(self):
        if not self.game_over:
            self.dino_group.update()
            self.cact_group.update()
            self.check_score()

    def render(self):
        self.screen.fill((255, 255, 255))
        self.dino_group.draw(self.screen)
        self.cact_group.draw(self.screen)
        self.draw_text()
        pg.display.update()

    def create_cacts(self):
          
        current_time = pg.time.get_ticks()
        if current_time - self.last_cact > self.cact_frequency:
            cact1 = Cact(1000, random.randint(210, 300))
            cact2 = Cact(1000 + 35, random.randint(210, 300))
            cact3 = Cact(1000 + 70, random.randint(210, 300))
            
            self.cact_group.add(cact1, cact2, cact3)
            self.last_cact = current_time


    def collision(self):
        if pg.sprite.groupcollide(self.dino_group, self.cact_group, False, False):
            self.game_over = True

    def check_score(self):
        if len(self.cact_group) > 0:
            # Check if the dino passes the cact
            if (
                self.dino_group.sprites()[0].rect.left > self.cact_group.sprites()[0].rect.left
                and not self.pass_cact
                and self.cact_group.sprites()[0].rect.left >= 68
            ):
                self.pass_cact = True

            if self.pass_cact and self.dino_group.sprites()[0].rect.left > self.cact_group.sprites()[0].rect.right:
                self.score += 1
                self.pass_cact = False

    def draw_text(self):
        font = pg.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.width // 2, 20))
        self.screen.blit(text, text_rect)


if __name__ == "__main__":
    game = GameEngine(900, 400, 60)
    game.init()
    dino = Dino(100, 322, game.screen_size)
    game.dino_group.add(dino)
    game.run()
