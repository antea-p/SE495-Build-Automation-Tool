from typing import List

from custom_types import Box, Position

MAX_WIDTH = 123
MAX_LENGTH = 198


# https://observablehq.com/@mourner/simple-rectangle-packing
def bin_packing(boxes: List[Box]) -> dict | None:
    boxes.sort(key=lambda x: x.w * x.l, reverse=True)

    unfit_boxes = boxes.copy()
    empty_slots = [Position(x=0, y=0, w=MAX_WIDTH, l=MAX_LENGTH)]
    occupied = []

    for box in boxes:
        # https://docs.python.org/3.14/library/stdtypes.html#ranges
        for i in range(len(empty_slots) - 1, -1, -1):
            slot = empty_slots[i]

            if (box.w > MAX_WIDTH) or (box.l > MAX_LENGTH):
                print("Box can't fit the print bed!")
                break

            if (box.w > slot.w) or (box.l > slot.l):
                continue

            occupied.append(Position(x=slot.x, y=slot.y, w=box.w, l=box.l, filename=box.filename))
            unfit_boxes.remove(box)

            if (box.w == slot.w) and (box.l == slot.l):
                last = empty_slots.pop()
                if i < len(empty_slots):
                    empty_slots[i] = last

            elif box.l == slot.l:
                slot.x += box.w
                slot.w -= box.w

            elif box.w == slot.w:
                slot.y += box.l
                slot.l -= box.l

            else:
                empty_slots.append(Position(
                    x=slot.x + box.w,
                    y=slot.y,
                    w=slot.w - box.w,
                    l=box.l
                ))
                slot.y += box.l
                slot.l -= box.l
            break

    return {"occupied": occupied, "empty_slots": empty_slots, "unfit_boxes": unfit_boxes}
