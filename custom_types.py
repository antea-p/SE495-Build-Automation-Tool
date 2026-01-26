from dataclasses import dataclass
from enum import Enum

import pyautogui

w, h = pyautogui.size()


class Status(Enum):
    NEW = 1
    BUILT = 2
    PRODUCING = 3
    FINISHED = 4


@dataclass
class Box:
    w: int
    l: int
    h: int = None
    filename: str = None


@dataclass
class Position:
    # FOR EMPTY SLOT -> (x, y) = top left corner of empty slot, (w, l) = slot size
    # FOR PACKED SLOT -> (x, y) = top left corner of the box, (w, l) = box size, filename = original model name
    x: int
    y: int
    w: int
    l: int
    filename: str = None


@dataclass
class Region:
    top_left: int
    top_right: int
    bottom_left: int
    bottom_right: int

    def __init__(self, top_left, top_right, bottom_left, bottom_right):
        self.top_left = int(top_left)
        self.top_right = int(top_right)
        self.bottom_left = int(bottom_left)
        self.bottom_right = int(bottom_right)


HOTKEYS = {
    'NEW_PROJECT': ['ctrl', 'n'],
    'OPEN': ['ctrl', 'o'],
    'SLICE': ['s', 'l'],
    'SAVE': ['ctrl', 'shift', 's'],
    'CANCEL_PROMPT': ['alt', 'f4'],
    'ENTER': 'enter'
}

REGION_BOX = {
    "SLICE": Region(w * 0.8, h * 0.91, w * 0.98, h * 0.98),
    "SAVING_SLICE": Region(w * 0.4, h * 0.74, w * 0.58, h * 0.82),
    "BACK_TO_MODEL_PREPARE": Region(w * 0.45, 0, w * 0.5, h * 0.05),
    "NO": Region(w * 0.5, h * 0.5, w * 0.6, h * 0.55),
    "BUG_FEEDBACK": Region(w * 0.3, h * 0.1, w * 0.4, h * 0.2)
}
