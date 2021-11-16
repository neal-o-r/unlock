import matplotlib.pyplot as plt
from typing import List, Generator

Position = int
Pattern = List[Position]
PatternGenerator = Generator[Pattern, None, None]

blocks = {
    # number : blocked : blocked by
    1: {3: 2, 7: 4, 9: 5},
    2: {8: 5},
    3: {1: 2, 7: 5, 9: 6},
    4: {6: 5},
    5: {},
    6: {4: 5},
    7: {1: 4, 3: 5, 9: 8},
    8: {2: 5},
    9: {1: 5, 3: 6, 7: 8},
}

locs = {
    1: (0, 2),
    2: (1, 2),
    3: (2, 2),
    4: (0, 1),
    5: (1, 1),
    6: (2, 1),
    7: (0, 0),
    8: (1, 0),
    9: (2, 0)
}

def transpose(lst: list) -> list: return list(zip(*lst))


def show_pattern(pattern: Pattern):
    plt.scatter(*transpose(locs.values()), c="k")

    pts = [locs[p] for p in pattern]
    for i, p in enumerate(zip(pts, pts[1:])):
        plt.plot(*transpose(p), "k", alpha=0.4 + 0.05 * i)

    plt.axis("off")
    plt.title("→".join(map(str, pattern)))
    plt.show()


def line_types(pattern: Pattern) -> int:
    # how many different kinds of lines are there,
    # ignoring lines that are reflections on one another
    abs_sub = lambda x, y: abs(x - y)
    lines = set()
    for i in range(0, len(pattern) - 2):
        l1, l2 = locs[pattern[i]], locs[pattern[i + 1]]
        lines.add(tuple(map(abs_sub, l1, l2)))

    return len(lines)


def available(pattern: Pattern, n: Position) -> bool:
    *_, end = pattern
    is_blocked = n in blocks[end]
    is_freed = blocks[end].get(n, None) in pattern
    return (not is_blocked) or is_freed


def next_pattern(pattern: Pattern) -> PatternGenerator:
    yield from (
        pattern + [n]
        for n in range(1, 10)
        if not pattern or (n not in pattern and available(pattern, n))
    )


def all_patterns(length: int, pattern: Pattern = []) -> PatternGenerator:
    if length == 0:
        yield pattern
    else:
        for p in next_pattern(pattern):
            yield from all_patterns(length - 1, pattern=p)


if __name__ == "__main__":
    patterns9 = all_patterns(9)
    most_complex = max(patterns9, key=line_types)
    show_pattern(most_complex)
