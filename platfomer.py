import pyxel
import common
from map import Map
from player import Player

WIDTH: int = 128
HEIGHT: int = 128
TILE_MAP: int = 0
ASSETS = "assets/pypla.pyxres"


class Main:
    def __init__(self) -> None:
        self.map: Map = Map(TILE_MAP, WIDTH, HEIGHT, common.TILE_SIZE)
        init_px = 4
        init_py = 4
        self.player: Player = Player(
            init_px * common.TILE_SIZE, init_py * common.TILE_SIZE, self.map
        )

        pyxel.init(WIDTH, HEIGHT, fps=common.FPS)
        pyxel.load(ASSETS)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.map.update()
        self.player.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.draw_map()
        self.draw_player()

    def draw_map(self):
        self.map.draw()

    def draw_player(self):
        self.player.draw()


Main()
