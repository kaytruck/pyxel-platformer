import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 128
ACC = 0.3
DEC = 0.1
MAX = 3


class AccDec:
    """加減速サンプルプログラム"""

    def __init__(self):
        self.ax = 0
        self.vx = 0
        self.px = 64
        self.d = 1

        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.ax = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.ax = ACC
        if pyxel.btn(pyxel.KEY_LEFT):
            self.ax = -ACC

        if self.ax == 0:
            # 加速されなかった場合は徐々に減速する
            if self.vx > 0:
                self.vx -= 0.1
            if self.vx < 0:
                self.vx += 0.1
        else:
            # 加速
            self.vx += self.ax
        if abs(self.vx) < 0.1:
            # 絶対値が十分に小さくなった場合、速度は0にする
            self.vx = 0

        # 速度の上限
        if self.vx > MAX:
            self.vx = MAX
        if self.vx < -MAX:
            self.vx = -MAX

        # 位置の更新
        self.px += self.vx
        if self.px <= 0:
            self.px = 0
        elif self.px >= WINDOW_WIDTH:
            self.px = WINDOW_WIDTH

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.px, 64, 4, 6)


AccDec()
