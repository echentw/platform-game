import os
import sys
import pygame as pg

import archer as arc
import saber as sab
import caster as cast
import block

class Control(object):
  CAPTION = "My Game"
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, level_size):
    self.level = pg.Surface((level_size[0], level_size[1])).convert()
    self.level_rect = self.level.get_rect()

    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0
    self.done = False
    self.keys = pg.key.get_pressed()

    x = self.screen_rect.center[0] - 40
    y = self.screen_rect.center[1] + 40
    self.player1 = sab.Saber(4, (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT),
                             "assets/sprites/saber_walk.png", (x,y,38,54),
                             "assets/sprites/saber_slash.png", (x,y,74,54),
                             "assets/sprites/saber_jump1.png", (x,y,38,58),
                             "assets/sprites/saber_jump2.png", (x,y,41,63))
#    self.player1 = arc.Archer(5, (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT),
#                              "assets/sprites/archer_walk.png", (x,y,33,60),
#                              "assets/sprites/archer_slash.png", (x,y,90,70),
#                              "assets/sprites/archer_jump1.png", (x,y,52,59),
#                              "assets/sprites/archer_jump2.png", (x,y,52,59))
    y -= 100
    self.player2 = cast.Caster(5, (pg.K_w, pg.K_s, pg.K_a, pg.K_d),
                               "assets/sprites/caster_walk.png", (x,y,32,62),
                               "assets/sprites/caster_attack.png", (x,y,95,61),
                               "assets/sprites/caster_jump1.png", (x,y,62,65),
                               "assets/sprites/caster_jump2.png", (x,y,62,65))
    self.obstacles = self.make_obstacles()
    self.player1_obstacles = pg.sprite.Group(self.player2)
    self.player1_obstacles.add(self.obstacles)
    self.player2_obstacles = pg.sprite.Group(self.player1)
    self.player2_obstacles.add(self.obstacles)

  def make_obstacles(self):
    walls = [block.Block(pg.Color("chocolate"), (0,980,1000,20)),
             block.Block(pg.Color("chocolate"), (0,0,20,1000)),
             block.Block(pg.Color("chocolate"), (980,0,20,1000))]
    static = [block.Block(pg.Color("darkgreen"), (250,780,200,100)),
              block.Block(pg.Color("darkgreen"), (600,880,200,100)),
              block.Block(pg.Color("darkgreen"), (20,360,880,40)),
              block.Block(pg.Color("darkgreen"), (950,400,30,20)),
              block.Block(pg.Color("darkgreen"), (20,630,50,20)),
              block.Block(pg.Color("darkgreen"), (80,530,50,20)),
              block.Block(pg.Color("darkgreen"), (130,470,200,210)),
              block.Block(pg.Color("darkgreen"), (20,760,30,20)),
              block.Block(pg.Color("darkgreen"), (400,740,30,40))]

    return pg.sprite.Group(walls, static)

  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
      elif event.type == pg.KEYDOWN:
        self.player1.handle_keydown(event.key, self.player1_obstacles)
        self.player2.handle_keydown(event.key, self.player2_obstacles)

        if event.key == self.player1.DOWN_KEY:
          if not self.player1.fall:
            if self.player1.direction == self.player1.LEFT_KEY:
              self.player2.receive_attack(self.player1.attack_left_rect)
            else:
              self.player2.receive_attack(self.player1.attack_right_rect)
        elif event.key == self.player2.DOWN_KEY:
          if not self.player2.fall:
            if self.player2.direction == self.player2.LEFT_KEY:
              self.player1.receive_attack(self.player2.attack_left_rect)
            else:
              self.player1.receive_attack(self.player2.attack_right_rect)

      elif event.type == pg.KEYUP:
        self.player1.handle_keyup(event.key)
        self.player2.handle_keyup(event.key)

  def update(self):
    if self.player1.health == 0:
      print self.player2.name + " wins!"
      self.done = True
    elif self.player2.health == 0:
      print self.player1.name + " wins!"
      self.done = True
    self.player1.update(self.screen_rect, self.player1_obstacles)
    self.player2.update(self.screen_rect, self.player2_obstacles)
    self.screen_rect.center = \
        ((self.player1.rect.center[0] + self.player2.rect.center[0]) / 2.0,
         (self.player1.rect.center[1] + self.player2.rect.center[1]) / 2.0)

  def draw(self):
    self.level.fill(Control.BACKGROUND_COLOR)
    self.screen_rect.clamp_ip(self.level_rect)
    self.obstacles.draw(self.level)
    self.player1.draw(self.level)
    self.player2.draw(self.level)
    self.screen.blit(self.level, (0, 0), self.screen_rect)

    font = pg.font.Font(None, 28)
    text1 = font.render(self.player1.name + " health: " + self.get_health_bar(self.player1), 1, (10, 10, 10))
    textpos1 = text1.get_rect()
    textpos1.topleft = self.screen.get_rect().topleft
    self.screen.blit(text1, textpos1)

    text2 = font.render(self.player2.name + " health: " + self.get_health_bar(self.player2), 2, (10, 10, 10))
    textpos2 = text2.get_rect()
    textpos2.top = self.screen.get_rect().top
    textpos2.left = self.screen.get_rect().centerx
    self.screen.blit(text2, textpos2)

  def get_health_bar(self, player):
    output = ''
    for i in xrange(player.health):
      output += '-'
    return output

  def main_loop(self):
    pg.display.set_caption(Control.CAPTION)
#    pg.display.toggle_fullscreen()
    pg.mixer.music.load("assets/music/oath-sign-orchestra.mp3")
    pg.mixer.music.play()

    while not self.done:
      if not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)

