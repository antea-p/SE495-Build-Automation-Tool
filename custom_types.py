from enum import Enum


class Status(Enum):
    NEW = 1
    BUILT = 2
    PRODUCING = 3
    FINISHED = 4
