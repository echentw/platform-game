import os
import sys
import pygame as pg

import player
import archer as arc
import saber as sab
import caster as cast
import block

class Control(object):
  CAPTION = "My Game"
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, level_size):
    # winner is set when one player's health hits 0
    self.winner = None

    # the entire map
    self.level = pg.Surface((level_size[0], level_size[1])).convert()
    self.level_rect = self.level.get_rect()

    # handles the display
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock  = pg.time.Clock()
    self.fps = 60.0
    self.done = False
    self.keys = pg.key.get_pressed()

    # sound when an attack hits
    self.sound_impact = pg.mixer.Sound("assets/soundfx/sword_impact.wav")

    # controls for the players
    player1_keys = (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)
    player2_keys = (pg.K_w, pg.K_s, pg.K_a, pg.K_d)

    # initialize characters
    saber_location = (500, 500)
    archer_location = (800, 200)
    caster_location = (200, 200)
    saber = sab.Saber(player1_keys, saber_location)
    archer = arc.Archer(player2_keys, archer_location)
    caster = cast.Caster(player2_keys, caster_location)

    # initialize the players
    self.player1 = saber
    self.player2 = caster

    # initialize the obstacles of the game
    self.obstacles = self.make_obstacles()
    self.player1_obstacles = pg.sprite.Group(self.player2)
    self.player1_obstacles.add(self.obstacles)
    self.player2_obstacles = pg.sprite.Group(self.player1)
    self.player2_obstacles.add(self.obstacles)

    # initialize the face images of the characters
    self.player1_face_rect = self.player1.face_im.get_rect()
    self.player2_face_rect = self.player2.face_im.get_rect()
    self.player2_face_rect.right = self.screen_rect.width


  # helper method to create the platforms in the game
  def make_obstacles(self):
    size = 20

    walls = [block.Block((0 * size, 48 * size, 50 * size, 2 * size)),
             block.Block((0 * size, 0 * size, 50 * size, 1 * size)),
             block.Block((0 * size, 0 * size, 1 * size, 50 * size)),
             block.Block((49 * size, 0 * size, 1 * size, 50 * size))]

    ground = [block.Block((1 * size, 42 * size, 32 * size, 6 * size)),
              block.Block((1 * size, 36 * size, 17 * size, 6 * size))]

    big = [block.Block((5 * size, 18 * size, 9 * size, 13 * size)),
           block.Block((4 * size, 23 * size, 1 * size, 1 * size)),
           block.Block((4 * size, 30 * size, 1 * size, 1 * size)),
           block.Block((14 * size, 23 * size, 1 * size, 1 * size)),
           block.Block((14 * size, 30 * size, 1 * size, 1 * size))]

    floating = [block.Block((20 * size, 21 * size, 9 * size, 2 * size)),
                block.Block((23 * size, 31 * size, 15 * size, 1 * size)),
                block.Block((33 * size, 19 * size, 1 * size, 1 * size)),
                block.Block((37 * size, 16 * size, 7 * size, 2 * size))]

    high = [block.Block((6 * size, 9 * size, 3 * size, 2 * size)),
            block.Block((15 * size, 9 * size, 3 * size, 2 * size)),
            block.Block((24 * size, 9 * size, 3 * size, 2 * size)),
            block.Block((33 * size, 9 * size, 3 * size, 2 * size))]

    return pg.sprite.Group(walls, ground, big, floating, high)

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()

      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True

      # someone is attacking
      elif event.type == pg.KEYDOWN:
        if event.key == self.player1.DOWN_KEY:
          if not self.player1.fall and \
             not self.player1.attacking and \
             not self.player1.hurt:
            if self.player1.direction == self.player1.LEFT_KEY:
              if self.player2.receive_attack(self.player2.RIGHT_KEY,
                                             self.player1.attack_left_rect):
                self.sound_impact.play()
            else:
              if self.player2.receive_attack(self.player2.LEFT_KEY,
                                             self.player1.attack_right_rect):
                self.sound_impact.play()
        elif event.key == self.player2.DOWN_KEY:
          if not self.player2.fall and \
             not self.player2.attacking and \
             not self.player2.hurt:
            if self.player2.direction == self.player2.LEFT_KEY:
              if self.player1.receive_attack(self.player1.RIGHT_KEY,
                                             self.player2.attack_left_rect):
                self.sound_impact.play()
            else:
              if self.player1.receive_attack(self.player1.LEFT_KEY,
                                             self.player2.attack_right_rect):
                self.sound_impact.play()
        self.player1.handle_keydown(event.key, self.player1_obstacles)
        self.player2.handle_keydown(event.key, self.player2_obstacles)

      elif event.type == pg.KEYUP:
        self.player1.handle_keyup(event.key)
        self.player2.handle_keyup(event.key)

  # check for winner, update player position
  def update(self):
    if self.player1.health == 0:
      self.winner = self.player2
      self.done = True
    elif self.player2.health == 0:
      self.winner = self.player1
      self.done = True
    self.player1.update(self.screen_rect, self.player1_obstacles)
    self.player2.update(self.screen_rect, self.player2_obstacles)
    self.screen_rect.center = \
        ((self.player1.rect.center[0] + self.player2.rect.center[0]) / 2.0,
         (self.player1.rect.center[1] + self.player2.rect.center[1]) / 2.0)

  # draw things onto the screen
  def draw(self):
    self.level.fill(Control.BACKGROUND_COLOR)
    self.screen_rect.clamp_ip(self.level_rect)
    self.obstacles.draw(self.level)
    self.player1.draw(self.level)
    self.player2.draw(self.level)
    self.screen.blit(self.level, (0, 0), self.screen_rect)

    self.screen.blit(self.player1.face_im, (0, 0))
    self.screen.blit(self.player2.face_im, self.player2_face_rect)

    font = pg.font.Font(None, 28)
    name1 = font.render(self.player1.name, 1, (200, 200, 200))
    health1 = font.render(get_health_bar(self.player1), 1, (200, 200, 200))
    textpos1 = name1.get_rect()
    textpos1.topleft = self.player1.face_im.get_rect().topleft
    self.screen.blit(name1, textpos1)
    textpos1.y = textpos1.y + 12
    self.screen.blit(health1, textpos1)

    name2 = font.render(self.player2.name, 2, (200, 200, 200))
    health2 = font.render(get_health_bar(self.player2), 1, (200, 200, 200))
    textpos2 = name2.get_rect()
    textpos2.topleft = self.player2_face_rect.topleft
    self.screen.blit(name2, textpos2)
    textpos2.y = textpos2.y + 12
    self.screen.blit(health2, textpos2)


  # main loop of the game
  def main_loop(self):
    pg.display.set_caption(Control.CAPTION)
    pg.mixer.music.load("assets/music/oath-sign-orchestra.wav")
    pg.mixer.music.play()
    while not self.done:
      if not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)
    self.game_over_loop()

  # game over screen
  def game_over_loop(self):
    self.done = False

    font = pg.font.Font(None, 48)
    text1 = font.render(self.winner.name + " wins!", 1, (230, 230, 230))
    textpos1 = text1.get_rect()
    textpos1.centerx = self.screen.get_rect().centerx
    textpos1.centery = self.screen.get_rect().centery

    font = pg.font.Font(None, 24)
    text2 = font.render("Press esc to quit", 1, (230, 230, 230))
    textpos2 = text2.get_rect()
    textpos2.centerx = self.screen.get_rect().centerx
    textpos2.centery = self.screen.get_rect().centery + 40

    self.screen.fill(Control.BACKGROUND_COLOR)
    self.screen.blit(text1, textpos1)
    self.screen.blit(text2, textpos2)

    pg.display.update()

    while not self.done:
      for event in pg.event.get():
        self.keys = pg.key.get_pressed()
        if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
          self.done = True


# Hacky way to show the health bar
def get_health_bar(player):
  output = ''
  for i in xrange(player.health):
    output += '--'
  return output

