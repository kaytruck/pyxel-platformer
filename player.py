import pyxel
import common
from map import Map
from common import Direction


class Player:
    def __init__(self, initial_x, initial_y, current_map) -> None:
        self.px: int = initial_x
        self.py: int = initial_y
        # TODO PlayerからMapへ直接参照するのはやめたい
        self.current_map: Map = current_map

        self.direction: Direction = Direction.RIGHT
        self.acc_x: int = 0
        self.acc_y: int = common.GRAVITY
        self.jump_count: int = 0
        self.gravity_tick: int = 0
        self.gravity_interval: int = common.GRAVITY_INTERVAL

        self.img: int = 0
        self.pu: int = 0
        self.pv: int = 0

        self.attack: bool = False
        self.attack_offset: int = common.TILE_SIZE
        self.attack_direction: int = 1

        self.ani_move_idx: int = -1
        self.ani_move_idx_max: int = 2
        self.ani_move_tick: int = 0
        self.ani_move_interval: int = 3

        self.ani_atk_idx: int = -1
        self.ani_atk_idx_max: int = 4
        self.ani_atk_tick: int = 0
        self.ani_atk_interval: int = 1

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction = Direction.LEFT
            self.acc_x = -common.PLYAER_STEP
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = Direction.RIGHT
            self.acc_x = common.PLYAER_STEP
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.jump_count < 2:
                # ダブルジャンプまでは許容する
                self.acc_y = common.JUMP
                self.jump_count += 1
        if pyxel.btnp(pyxel.KEY_X):
            # 攻撃
            self.attack = True
        if pyxel.btnr(pyxel.KEY_LEFT) or pyxel.btnr(pyxel.KEY_RIGHT):
            self.acc_x = 0

        # X軸方向の移動
        self.move_x()
        # Y軸方向の移動
        self.move_y()

        # 描画の準備
        self.prepare_draw()

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
        self.gravity_tick = (self.gravity_tick + 1) % self.gravity_interval
        if self.gravity_tick == 0:
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

    def prepare_draw(self):
        # 自機のアニメーション
        self.img = 0
        if self.acc_x != 0:
            self.ani_move_tick = (self.ani_move_tick + 1) % self.ani_move_interval
            if self.ani_move_tick == 0:
                self.ani_move_idx += 1
                if self.ani_move_idx >= self.ani_move_idx_max:
                    self.ani_move_idx = 0
        else:
            self.ani_move_idx = 0

        # 自機画像の取得元位置
        if self.jump_count != 0:
            # ジャンプ中画像を表示
            self.pu = 0
            if self.acc_x > 0:
                # 右移動ジャンプ
                self.pv = common.TILE_SIZE * 3
            elif self.acc_x == 0:
                # その場でジャンプ
                if self.direction == Direction.RIGHT:
                    self.pv = common.TILE_SIZE * 2
                elif self.direction == Direction.LEFT:
                    self.pv = common.TILE_SIZE * 5
            elif self.acc_x < 0:
                # 左移動ジャンプ
                self.pv = common.TILE_SIZE * 6
        # TODO 立ち止まり、上下方向を向く
        # TODO 斜め上方向
        # TODO 斜め下方向
        else:
            # 左右水平移動の画像を表示
            self.pu = 0 + common.TILE_SIZE * self.ani_move_idx
            self.pv = 0 + common.TILE_SIZE * self.direction.value

        # 攻撃のアニメーション
        if self.attack:
            self.ani_atk_tick = (self.ani_atk_tick + 1) % self.ani_atk_interval
            if self.ani_atk_tick == 0:
                self.ani_atk_idx += 1
                if self.ani_atk_idx >= self.ani_atk_idx_max:
                    self.ani_atk_idx = 0
                    self.attack = False
            # プレイヤーの左右向きに応じて攻撃描画位置を変更
            self.attack_offset = common.TILE_SIZE
            self.attack_direction = 1
            if self.direction == Direction.LEFT:
                self.attack_offset = -common.TILE_SIZE * 2
                self.attack_direction = -1

    def draw(self):
        # 自機の描画
        pyxel.blt(
            self.px,
            self.py,
            self.img,
            self.pu,
            self.pv,
            common.TILE_SIZE,
            common.TILE_SIZE,
            0,
        )
        if self.attack:
            # 攻撃の描画
            pyxel.blt(
                self.px + self.attack_offset,
                self.py,
                self.img,
                (0 + common.TILE_SIZE * 2),
                (0 + common.TILE_SIZE * self.ani_atk_idx),
                common.TILE_SIZE * 2 * self.attack_direction,
                common.TILE_SIZE,
                0,
            )
