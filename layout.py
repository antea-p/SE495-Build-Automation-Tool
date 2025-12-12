from dataclasses import dataclass
from typing import List


@dataclass
class Box:
    w: int
    h: int


@dataclass
class Position:
    # FOR EMPTY SLOT -> (x, y) = top left corner of empty slot, (w, h) = slot size
    # FOR PACKED SLOT -> (x, y) = top left corner of the box, (w, h) = box size
    x: int
    y: int
    w: int
    h: int


MAX_WIDTH = 123
MAX_LENGTH = 198


def bin_packing(boxes: List[Box]) -> list[List[Position]] | None:
    area = 0
    # max_width = 0
    for box in boxes:
        area += box.w * box.h
        # max_width = max(max_width, box.w)

    boxes.sort(key=lambda x: x.w * x.h, reverse=True)

    empty_slots = [Position(x=0, y=0, w=MAX_WIDTH, h=MAX_LENGTH)]
    occupied = []

    for box in boxes:
        print(f"Current box: {box}")
        for (i, slot) in enumerate(reversed(empty_slots)):
            if (box.w > MAX_WIDTH) or (box.h > MAX_LENGTH):
                print("Box can't fit the print bed!")
                continue

            if (box.w > slot.w) or (box.h > slot.h):
                print("Box too big!")
                continue

            print("Placing the box...")
            occupied.append(Position(x=slot.x, y=slot.y, w=box.w, h=box.h))
            print(f"Packed! Position: {Position(x=slot.x, y=slot.y, w=box.w, h=box.h)}")

            if (box.w == slot.w) and (box.h == slot.h):
                last = empty_slots.pop()
                if i < len(empty_slots):
                    slot = last

            elif box.h == slot.h:
                slot.x += box.w
                slot.w -= box.w

            elif box.w == slot.w:
                slot.y += box.h
                slot.h -= box.h

            else:
                empty_slots.append(Position(
                    x=slot.x + box.w,
                    y=slot.y,
                    w=slot.w - box.w,
                    h=box.h
                ))
                slot.y += box.h
                slot.h -= box.h
            break
    print(f"Occupied len: {len(occupied)}, occupied: {occupied})")
    print(f"Empty len: {len(empty_slots)}, empty: {empty_slots})")

    return [occupied, empty_slots]


if __name__ == '__main__':
    boxes = [
        Box(80, 400),
        Box(100, 100),
        Box(250, 100),
        Box(400, 80),
        Box(60, 60),
        Box(60, 60),
        Box(60, 60),
        Box(20, 50),
        Box(20, 50),
        Box(20, 50),
        Box(10, 10),
        Box(10, 10),
        Box(5, 5),
    ]
    bin_packing(boxes)
