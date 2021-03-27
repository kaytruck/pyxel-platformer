import pyxel
import common
from map import Map


class Player:
    def __init__(self, initial_x, initial_y, current_map) -> None:
        self.px: int = initial_x
        self.py: int = initial_y
        self.current_map: Map = current_map
        self.acc_x: int = 0
        self.acc_y: float = common.GRAVITY
        self.jump_count: int = 0

        self.anime_idx: int = 0
        self.anime_idx_max: int = 2
        self.anime_tick: int = 0
        self.anime_interval: int = 3

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.acc_x = -common.PLYAER_STEP
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.acc_x = common.PLYAER_STEP
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.jump_count < 2:
                # ダブルジャンプまでは許容する
                self.acc_y = common.JUMP
                self.jump_count += 1
        if pyxel.btnr(pyxel.KEY_LEFT) or pyxel.btnr(pyxel.KEY_RIGHT):
            self.acc_x = 0

        # X軸方向の移動
        self.move_x()
        # Y軸方向の移動
        self.move_y()

    def move_x(self):
        # 左側の壁判定(上端)
        top_left_tx = int((self.px + self.acc_x) / common.TILE_SIZE)
        top_left_ty = int(self.py / common.TILE_SIZE)
        top_left_tile = self.current_map.get_tile(top_left_tx, top_left_ty)
        # 左側の壁判定(下端)
        bottom_left_tx = top_left_tx
        bottom_left_ty = int((self.py + common.TILE_SIZE - 1) / common.TILE_SIZE)
        bottom_left_tile = self.current_map.get_tile(bottom_left_tx, bottom_left_ty)
        # 右側の壁判定(上端)
        top_right_tx = int(
            (self.px + common.TILE_SIZE + self.acc_x - 1) / common.TILE_SIZE
        )
        top_right_ty = top_left_ty
        top_right_tile = self.current_map.get_tile(top_right_tx, top_right_ty)
        # 右側の壁判定(下端)
        bottom_right_tx = top_right_tx
        bottom_right_ty = bottom_left_ty
        bottom_right_tile = self.current_map.get_tile(bottom_right_tx, bottom_right_ty)

        # 移動
        if (
            top_left_tile >= common.TILE_BG_NUM
            or bottom_left_tile >= common.TILE_BG_NUM
        ):
            # 左側の位置補正
            self.px = (top_left_tx + 1) * common.TILE_SIZE
        elif (
            top_right_tile >= common.TILE_BG_NUM
            or bottom_right_tile >= common.TILE_BG_NUM
        ):
            # 右側の位置補正
            self.px = (top_right_tx - 1) * common.TILE_SIZE
        else:
            # 補正不要時の移動
            self.px += self.acc_x

    def move_y(self):
        # 重力加速度
        self.acc_y += common.GRAVITY
        if self.acc_y > common.GRAVITY_MAX:
            self.acc_y = common.GRAVITY_MAX

        # 上側の壁判定(左端)
        top_left_tx = int(self.px / common.TILE_SIZE)
        top_left_ty = int((self.py + self.acc_y) / common.TILE_SIZE)
        top_left_tile = self.current_map.get_tile(top_left_tx, top_left_ty)
        # 上側の壁判定(右端)
        top_right_tx = int((self.px + common.TILE_SIZE - 1) / common.TILE_SIZE)
        top_right_ty = top_left_ty
        top_right_tile = self.current_map.get_tile(top_right_tx, top_right_ty)
        # 下側の壁判定(左端)
        bottom_left_tx = top_left_tx
        bottom_left_ty = int(
            (self.py + common.TILE_SIZE + self.acc_y - 1) / common.TILE_SIZE
        )
        bottom_left_tile = self.current_map.get_tile(bottom_left_tx, bottom_left_ty)
        # 下側の壁判定(右端)
        bottom_right_tx = top_right_tx
        bottom_right_ty = bottom_left_ty
        bottom_right_tile = self.current_map.get_tile(bottom_right_tx, bottom_right_ty)

        # 移動
        if top_left_tile >= common.TILE_BG_NUM or top_right_tile >= common.TILE_BG_NUM:
            # 上側の位置補正
            self.py = (top_left_ty + 1) * common.TILE_SIZE
            # 上側の壁に当たった場合は縦方向の加速度をゼロにする
            self.acc_y = 0
        if (
            bottom_left_tile >= common.TILE_BG_NUM
            or bottom_right_tile >= common.TILE_BG_NUM
        ):
            # 下側の位置補正
            self.py = (bottom_left_ty - 1) * common.TILE_SIZE
            # ジャンプ中カウンタのクリア
            self.jump_count = 0
        else:
            # 補正不要時の移動
            self.py += self.acc_y

    def draw(self):
        img = 0
        if self.acc_x != 0:
            self.anime_tick = (self.anime_tick + 1) % self.anime_interval
            if self.anime_tick == 0:
                self.anime_idx += 1
                if self.anime_idx >= self.anime_idx_max:
                    self.anime_idx = 0
        else:
            self.anime_idx = 0
        pyxel.blt(
            self.px,
            self.py,
            img,
            (0 + self.anime_idx * common.TILE_SIZE),
            0,
            common.TILE_SIZE,
            common.TILE_SIZE,
            0,
        )
