import matplotlib.pyplot as plt

from custom_types import Position
from layout import MAX_WIDTH, MAX_LENGTH

cmap = plt.cm.get_cmap('gist_rainbow')


# https://sqlpey.com/python/top-6-ways-to-retrieve-colors-from-matplotlib-colormap/
def _next_color(i: int, max_colors):
    return cmap(((5 * i) % max_colors) / max_colors)


def _area(packed: list[Position]) -> float:
    area = 0
    for box in packed:
        area += box.w * box.l
    return area


def visualise(packed: list[Position], filename: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 12))  # https://stackoverflow.com/a/34162641

    for i, box in enumerate(packed):
        color = _next_color(i, 32)

        # https://pythonguides.com/matplotlib-plot-multiple-rectangles/
        ax.add_patch(
            plt.Rectangle((box.x, box.y), box.w, box.l, linewidth=2, edgecolor='black', facecolor=color, alpha=0.9,
                          zorder=2))
        ax.text(box.x + box.w / 2, box.y + box.l / 2, f"{box.w} x {box.l}", ha='center', va='center', weight='bold')

    plt.xlim(0, MAX_WIDTH)
    plt.ylim(0, MAX_LENGTH)

    plt.xlabel('Širina')
    plt.ylabel('Duljina')

    packed_area = _area(packed)
    plt.title(f'Iskorištenost: {packed_area / (MAX_WIDTH * MAX_LENGTH) * 100:.2f}%')
    plt.grid(linestyle='--', alpha=0.5)
    plt.tight_layout()

    plt.savefig(filename)
    plt.close()
