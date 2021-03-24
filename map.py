import pyxel


class Map:
    def __init__(self, tm, w, h, tilesize) -> None:
        self.tm = tm
        self.w = w
        self.h = h
        self.tilesize = tilesize

    def get_tile(self, tx, ty):
        return pyxel.tilemap(self.tm).get(tx, ty)

    def update(self):
        pass

    def draw(self):
        w = int(self.w / self.tilesize)
        h = int(self.h / self.tilesize)
        pyxel.bltm(0, 0, self.tm, 0, 0, w, h, 0)
