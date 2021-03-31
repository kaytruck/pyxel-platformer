from enum import Enum

FPS: int = 40

TILE_SIZE: int = 8
TILE_BG_NUM: int = 96  # 96以下のタイル番号は背景とみなし、当たり判定を行わない

PLYAER_STEP = 1
JUMP = -7
GRAVITY = 1
GRAVITY_MAX = 3


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    DOWN = 2
    UP = 3
