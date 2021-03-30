from enum import Enum

TILE_SIZE: int = 8
TILE_BG_NUM: int = 96  # 96以下のタイル番号は背景とみなし、当たり判定を行わない

PLYAER_STEP = 1
JUMP = -6
GRAVITY = 0.7
GRAVITY_MAX = 4


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    DOWN = 2
    UP = 3
