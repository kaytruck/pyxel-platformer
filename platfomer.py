from math import trunc
import pyxel

WIDTH: int = 128
HEIGHT: int = 128
TILE_SIZE: int = 8
TILE_BG_NUM: int = 96  # 96以下のタイル番号は背景とみなし、当たり判定を行わない
TILE_MAP: int = 0

PLYAER_STEP = 1
GRAVITY = 0.7
GRAVITY_MAX = 4
JUMP = -6


class Main:
    def __init__(self) -> None:
        self.player = Player(4 * TILE_SIZE, 4 * TILE_SIZE)
        self.init()

    def init(self):
        pyxel.init(WIDTH, HEIGHT)
        pyxel.load("assets/oldempire.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.draw_map()
        self.draw_player()

    def draw_map(self):
        tm = 0
        w = int(WIDTH / TILE_SIZE)
        h = int(HEIGHT / TILE_SIZE)
        pyxel.bltm(0, 0, tm, 0, 0, w, h, 0)

    def draw_player(self):
        self.player.draw()


class Player:
    def __init__(self, start_x, start_y) -> None:
        self.px: int = start_x
        self.py: int = start_y
        self.acc_x: int = 0
        self.acc_y: float = GRAVITY
        self.jump_count: int = 0

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.acc_x = -PLYAER_STEP
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.acc_x = PLYAER_STEP
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.jump_count < 2:
                # ダブルジャンプまでは許容する
                self.acc_y = JUMP
                self.jump_count += 1
        if pyxel.btnr(pyxel.KEY_LEFT) or pyxel.btnr(pyxel.KEY_RIGHT):
            self.acc_x = 0

        # X軸方向の移動
        self.move_x()
        # Y軸方向の移動
        self.move_y()

    def move_x(self):
        # 左側の壁判定(上端)
        top_left_tx = int((self.px + self.acc_x) / TILE_SIZE)
        top_left_ty = int(self.py / TILE_SIZE)
        top_left_tile = pyxel.tilemap(TILE_MAP).get(top_left_tx, top_left_ty)
        # 左側の壁判定(下端)
        bottom_left_tx = top_left_tx
        bottom_left_ty = int((self.py + TILE_SIZE - 1) / TILE_SIZE)
        bottom_left_tile = pyxel.tilemap(TILE_MAP).get(bottom_left_tx, bottom_left_ty)
        # 右側の壁判定(上端)
        top_right_tx = int((self.px + TILE_SIZE + self.acc_x - 1) / TILE_SIZE)
        top_right_ty = top_left_ty
        top_right_tile = pyxel.tilemap(TILE_MAP).get(top_right_tx, top_right_ty)
        # 右側の壁判定(下端)
        bottom_right_tx = top_right_tx
        bottom_right_ty = bottom_left_ty
        bottom_right_tile = pyxel.tilemap(TILE_MAP).get(
            bottom_right_tx, bottom_right_ty
        )

        if top_left_tile >= TILE_BG_NUM or bottom_left_tile >= TILE_BG_NUM:
            # 左側の位置補正
            self.px = (top_left_tx + 1) * TILE_SIZE
        elif top_right_tile >= TILE_BG_NUM or bottom_right_tile >= TILE_BG_NUM:
            # 右側の位置補正
            self.px = (top_right_tx - 1) * TILE_SIZE
        else:
            # 補正不要時の移動
            self.px += self.acc_x

    def move_y(self):
        # 重力加速度
        self.acc_y += GRAVITY
        if self.acc_y > GRAVITY_MAX:
            self.acc_y = GRAVITY_MAX

        # 上側の壁判定(左端)
        top_left_tx = int(self.px / TILE_SIZE)
        top_left_ty = int((self.py + self.acc_y) / TILE_SIZE)
        top_left_tile = pyxel.tilemap(TILE_MAP).get(top_left_tx, top_left_ty)
        # 上側の壁判定(右端)
        top_right_tx = int((self.px + TILE_SIZE - 1) / TILE_SIZE)
        top_right_ty = top_left_ty
        top_right_tile = pyxel.tilemap(TILE_MAP).get(top_right_tx, top_right_ty)
        # 下側の壁判定(左端)
        bottom_left_tx = top_left_tx
        bottom_left_ty = int((self.py + TILE_SIZE + self.acc_y - 1) / TILE_SIZE)
        bottom_left_tile = pyxel.tilemap(TILE_MAP).get(bottom_left_tx, bottom_left_ty)
        # 下側の壁判定(右端)
        bottom_right_tx = top_right_tx
        bottom_right_ty = bottom_left_ty
        bottom_right_tile = pyxel.tilemap(TILE_MAP).get(
            bottom_right_tx, bottom_right_ty
        )

        if top_left_tile >= TILE_BG_NUM or top_right_tile >= TILE_BG_NUM:
            # 上側の位置補正
            self.py = (top_left_ty + 1) * TILE_SIZE
            # 上側の壁に当たった場合は縦方向の加速度をゼロにする
            self.acc_y = 0
        if bottom_left_tile >= TILE_BG_NUM or bottom_right_tile >= TILE_BG_NUM:
            # 下側の位置補正
            self.py = (bottom_left_ty - 1) * TILE_SIZE
            # ジャンプ中カウンタのクリア
            self.jump_count = 0
        else:
            # 補正不要時の移動
            self.py += self.acc_y

    # def get_tile_xy(self, x, y):
    #     tx = int(x / TILE_SIZE)
    #     ty = int(y / TILE_SIZE)
    #     return tx, ty

    def draw(self):
        img = 0
        pyxel.blt(self.px, self.py, img, 0, 0, TILE_SIZE, TILE_SIZE, 0)


Main()
