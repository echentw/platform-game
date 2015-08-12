import os
import pygame as pg

from scenes import single_player_menu as sp_menu
from scenes import two_player_menu as tp_menu
from scenes import versus_game
from scenes import main_menu
from scenes import game_over


class Control:
  CAPTION = "Fate/Stay Night Game"
  SCREEN_SIZE = (900, 700)

  def __init__(self):
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pg.init()
    pg.display.set_caption(Control.CAPTION)
    pg.display.set_mode(Control.SCREEN_SIZE)

    self.menu = main_menu.Menu(Control.SCREEN_SIZE)
    self.sp_menu = sp_menu.Menu()
    self.tp_menu = tp_menu.Menu(Control.SCREEN_SIZE)
    self.versus_game = versus_game.Game(
        (1000, 1000), self.tp_menu.player1, self.tp_menu.player2)
    self.game_over = game_over.GameOver(Control.SCREEN_SIZE)


  def start(self):
    while True:
      self.menu.reset()
      self.menu.main_loop()
      if self.menu.quit:
        return

      if self.menu.state == main_menu.State.SINGLEPLAYER:
        self.sp_menu.reset()
        self.sp_menu.main_loop()
        if self.sp_menu.quit:
          return

      elif self.menu.state == main_menu.State.MULTIPLAYER:
        self.tp_menu.reset()
        self.tp_menu.main_loop()
        if self.tp_menu.goto_main:
          continue
        if self.tp_menu.quit:
          return

        self.versus_game.reset(self.tp_menu.player1, self.tp_menu.player2)
        self.versus_game.main_loop()
        if self.versus_game.quit:
          return

        self.game_over.reset()
        self.game_over.set_winner(self.versus_game.winner)
        self.game_over.main_loop()
        if self.game_over.quit:
          return

      else:
        return

