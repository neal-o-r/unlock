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


def available(pattern, n):
    *_, end = pattern
    is_blocked = n in blocks[end]
    is_freed = blocks[end].get(n, None) in pattern
    return (not is_blocked) or is_freed


def next_pattern(pattern):
    yield from (
        pattern + [n]
        for n in range(1, 10)
        if not pattern or (n not in pattern and available(pattern, n))
    )


def all_patterns(pattern, n, verbose=False):
    if n == 0:
        if verbose:
            print("->".join(map(str, pattern)))
        yield pattern
    else:
        for p in next_pattern(pattern):
            yield from all_patterns(p, n - 1, verbose)
