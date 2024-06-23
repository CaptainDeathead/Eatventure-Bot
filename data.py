from typing import Tuple, Dict
from json import loads

CONFIG: Dict[str, any] = {}

with open("config.json", "r") as file:
    CONFIG: Dict[str, any] = loads(file.read())

# VNC Settings
PHONE_IP_ADDRESS: str = CONFIG["PHONE_IP_ADDRESS"]

# Confordence values
STATION_UPGRADES_CONFORDENCE: float = 0.8
CRATES_CONFORDENCE: float = 0.8
EXPLINATION_CONFORDENCE: float = 0.85
POPUP_CONFORDENCE: float = 0.8
RENOVATE_UPGRADE_CONFORDENCE: float = 0.8

# Values to tinker with
Y_OFFSET_UPGRADE_MENU: int = 40
MIDDLE_X: int = 206
TOP_SCROLL_Y: int = 216
HALF_SCROLL: int = 516
BOTTOM_SCROLL_Y: int = 816
MAX_SCROLLS: int = 10
MAX_CHECK_X: int = 30
UPGRADE: Tuple[int, int] = (387, 898)
TOP_UPGRADE: Tuple[int, int] = (330, 385)
RENOVATION_UPGRADE_MIDPOINT: Tuple[int, int] = (100, 1200)
RENOVATION_UPGRADE: Tuple[int, int] = (50, 1240)
RENOVATE_BUTTON: Tuple[int, int] = (300, 673)
OPEN_BUTTON: Tuple[int, int] = (200, 565)
EXPLINATION_MARK_OFFSET: int = 30
NORMAL_GEOMETRY: Tuple[int, int, int, int] = (1094, 84, 442, 957)
NO_GO_BOTTOM_Y: int = 840
NO_GO_TOP_Y: int = 136

# MISC
SPRITES: Tuple[str] = ("big_cross.png", "crate.png", "crate1.png", "crate4.png", "explination_mark.png", "upgrade.png", "renovate_upgrade.png")
ZOOM: float = 1