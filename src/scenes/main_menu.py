import pygame as pg

from src.servants import archer as arc
from src.servants import saber as sab
from src.servants import caster as cast
from src.servants import assassin as ass

class State:
  SINGLEPLAYER = 0
  MULTIPLAYER = 1
  EXIT = 2


class Menu(object):
  CAPTION = "My Game"
  BACKGROUND_COLOR = (100, 100, 100)

  def __init__(self, screen_size):
    self.screen = pg.display.get_surface()
    self.screen_rect = self.screen.get_rect()
    self.clock = pg.time.Clock()
    self.fps = 60.0

    self.done = False
    self.quit = False
    self.keys = pg.key.get_pressed()

    # control main menu screen navigation
    self.state = State.SINGLEPLAYER
    self.default_color = (200, 200, 200)
    self.select_color  = (200, 0, 200)

    # decoration
    self.background = pg.image.load("assets/sprites/night.png").convert()
    self.excalibur_im = pg.image.load("assets/sprites/excalibur.png").convert()
    self.excalibur_im.set_colorkey((255, 0, 255))


  def reset(self):
    self.__init__((self.screen_rect.width, self.screen_rect.height))

  # check for key presses and releases
  def event_loop(self):
    for event in pg.event.get():
      self.keys = pg.key.get_pressed()
      if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
        self.done = True
        self.quit = True

      elif self.keys[pg.K_UP]:
        if self.state != State.SINGLEPLAYER:
          self.state -= 1
      elif self.keys[pg.K_DOWN]:
        if self.state != State.EXIT:
          self.state += 1
      elif self.keys[pg.K_RETURN]:
        if self.state == State.SINGLEPLAYER or self.state == State.MULTIPLAYER:
          self.done = True
          self.quit = False
        elif self.state == State.EXIT:
          self.done = True
          self.quit = True


  def update(self):
    pass

  # draw things onto the screen
  def draw(self):
    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.excalibur_im, (0, 0))

    font = pg.font.Font('assets/fonts/outline_pixel-7.ttf', 50)
    text = font.render('Fate/Stay Night Game', 1, (150, 150, 250))
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery - 30
    self.screen.blit(text, textpos)

    singleplayer_text_color = self.default_color
    multiplayer_text_color  = self.default_color
    exit_text_color         = self.default_color
    if self.state == State.SINGLEPLAYER:
      singleplayer_text_color = self.select_color
    elif self.state == State.MULTIPLAYER:
      multiplayer_text_color = self.select_color
    elif self.state == State.EXIT:
      exit_text_color = self.select_color

    font = pg.font.Font('assets/fonts/outline_pixel-7_solid.ttf', 24)
    text = font.render('Single Player', 1, singleplayer_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 30
    self.screen.blit(text, textpos)

    text = font.render('Multi Player', 1, multiplayer_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 60
    self.screen.blit(text, textpos)

    text = font.render('Exit', 1, exit_text_color)
    textpos = text.get_rect()
    textpos.centerx = self.screen_rect.centerx
    textpos.centery = self.screen_rect.centery + 90
    self.screen.blit(text, textpos)

    font = pg.font.Font(None, 24)
    text = font.render('UP and DOWN to navigate, ENTER to toggle', 1, (200, 200, 200))
    textpos = text.get_rect()
    textpos.bottomright = self.screen_rect.bottomright
    self.screen.blit(text, textpos)


  # main loop of the game
  def main_loop(self):
    pg.display.set_caption(Menu.CAPTION)
    pg.mixer.music.load("assets/music/kodoku-na-junrei.wav")
    pg.mixer.music.play()
    while not self.done:
      if not pg.mixer.music.get_busy():
        pg.mixer.music.play()
      self.event_loop()
      self.update()
      self.draw()
      pg.display.update()
      self.clock.tick(self.fps)
    return self.quit

