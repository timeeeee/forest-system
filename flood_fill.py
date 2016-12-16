from itertools import product


def neighbors(pos):
    """
    Return Moore neighborhood neighbors for given position in any dimension.
    """
    offsets = product(*[[0, -1, 1] for _ in range(len(pos))])
    # skip (0, 0... 0)
    offsets.next()

    for offset in offsets:
        yield tuple(a + b for a, b in zip(pos, offset))


assert set(neighbors((0,))) == set([(-1,), (1,)])
assert set(neighbors((0, 0))) == set([
             ( 0, -1), ( 0, 1),
    (-1, 0), (-1, -1), (-1, 1),
    ( 1, 0), ( 1, -1), ( 1, 1)])
s = set(neighbors((1, 2, 3)))
for a in [-1, 0, 1]:
    for b in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            if a != 0 or b != 0 or c != 0:
                assert (1 + a, 2 + b, 3 + c) in s


def get_value(array, pos):
    """Get the value of an n-dimensional array with the given coordinates."""
    result = array
    for index in pos:
        if index < 0:
            raise IndexError("negative index")
        result = result[index]
    return result


assert get_value([0, 1, 2, 3], (1,)) == 1
assert get_value([[1, 2, 3], [2, 3, 4], [3, 4, 5]], (2, 2)) == 5
assert get_value([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], (0, 0, 0)) == 1
assert get_value([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], (0, 1, 1)) == 4
assert get_value([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], (1, 0, 0)) == 5


def set_value(array, pos, new_value):
    """Set the value of an n-dimensional array with the given coordinates."""
    container = array
    # Get the list that immediately contains the value to change
    for index in pos[:-1]:
        if index < 0:
            raise IndexError("negative index")
        container = container[index]
    container[pos[-1]] = new_value


def flood_select(array, start_pos):
    """
    Generate a list of the starting point and all contiguous cells with the
    same value.
    """
    selected = set()
    queue = [start_pos]
    select_value = get_value(array, start_pos)
    while queue:
        pos = queue.pop()
        if pos not in selected:
            try:
                if get_value(array, pos) == select_value:
                    selected.add(pos)
                    queue.extend(neighbors(pos))
            # If we can't get the value, assume out of bounds of the grid
            except IndexError:
                pass
    return list(selected)


def flood_fill(array, start_pos, new_value):
    """
    Paint the contiguous region that start_pos is part of with new_value.
    """
    for pos in flood_select(array, start_pos):
        set_value(array, pos, new_value)


# Test one dimension
line = [0, 1, 1, 0, 0, 0, 1]
assert set(flood_select(line, (0,))) == set([(0,)])
assert set(flood_select(line, (1,))) == set([(1,), (2,)])
assert set(flood_select(line, (2,))) == set([(1,), (2,)])
assert set(flood_select(line, (3,))) == set([(3,), (4,), (5,)])
assert set(flood_select(line, (4,))) == set([(3,), (4,), (5,)])
assert set(flood_select(line, (5,))) == set([(3,), (4,), (5,)])
assert set(flood_select(line, (6,))) == set([(6,)])



# Test two dimensions
grid = [
    [0, 0, 1],
    [1, 0, 0],
    [1, 1, 1]]
zeros = set([(0, 0), (0, 1), (1, 1), (1, 2)])
ones = set([(1, 0), (2, 0), (2, 1), (2, 2)])
one_island = set([(0, 2)])
# make sure I did those positions right
assert len(zeros.union(ones).union(one_island)) == 9

assert set(flood_select(grid, (0, 0))) == zeros
assert set(flood_select(grid, (0, 1))) == zeros
assert set(flood_select(grid, (1, 1))) == zeros
assert set(flood_select(grid, (1, 2))) == zeros
assert set(flood_select(grid, (1, 0))) == ones
assert set(flood_select(grid, (2, 0))) == ones
assert set(flood_select(grid, (2, 1))) == ones
assert set(flood_select(grid, (2, 2))) == ones
assert set(flood_select(grid, (0, 2))) == one_island


# Test three dimensions
cube = [
    [
        [1, 0, 1],
        [0, 0, 1],
        [1, 1, 1]
        ],
    [
        [0, 0, 2],
        [0, 0, 2],
        [1, 1, 2]
        ],
    [
        [3, 3, 3],
        [3, 3, 3],
        [3, 3, 1]
        ]
    ]
assert get_value(cube, (0, 0, 0)) == 1  # This 1 is surrounded by 0s
# This 1 is connected diagonally with the big group of 1s
assert get_value(cube, (2, 2, 2)) == 1
zeros = set([(0, 0, 1), (0, 1, 0), (0, 1, 1),
             (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)])
ones = set([(0, 0, 2), (0, 1, 2), (0, 2, 0), (0, 2, 1), (0, 2, 2),
            (1, 2, 0), (1, 2, 1),
            (2, 2, 2)])
one_island = set([(0, 0, 0)])
twos = set([(1, 0, 2), (1, 1, 2), (1, 2, 2)])
threes = set([(2, 0, 0), (2, 0, 1), (2, 0, 2),
              (2, 1, 0), (2, 1, 1), (2, 1, 2),
              (2, 2, 0), (2, 2, 1)])
# Did I get everything?
assert len(zeros.union(ones).union(one_island).union(twos).union(threes)) == 27

assert set(flood_select(cube, (0, 0, 0))) == one_island
assert set(flood_select(cube, (0, 0, 1))) == zeros
assert set(flood_select(cube, (0, 0, 2))) == ones
assert set(flood_select(cube, (0, 1, 0))) == zeros
assert set(flood_select(cube, (0, 1, 1))) == zeros
assert set(flood_select(cube, (0, 1, 2))) == ones
assert set(flood_select(cube, (0, 2, 0))) == ones
assert set(flood_select(cube, (0, 2, 1))) == ones
assert set(flood_select(cube, (0, 2, 2))) == ones
assert set(flood_select(cube, (1, 0, 0))) == zeros
assert set(flood_select(cube, (1, 0, 1))) == zeros
assert set(flood_select(cube, (1, 0, 2))) == twos
assert set(flood_select(cube, (1, 1, 0))) == zeros
assert set(flood_select(cube, (1, 1, 1))) == zeros
assert set(flood_select(cube, (1, 1, 2))) == twos
assert set(flood_select(cube, (1, 2, 0))) == ones
assert set(flood_select(cube, (1, 2, 1))) == ones
assert set(flood_select(cube, (1, 2, 2))) == twos
assert set(flood_select(cube, (2, 0, 0))) == threes
assert set(flood_select(cube, (2, 0, 1))) == threes
assert set(flood_select(cube, (2, 0, 2))) == threes
assert set(flood_select(cube, (2, 1, 0))) == threes
assert set(flood_select(cube, (2, 1, 1))) == threes
assert set(flood_select(cube, (2, 1, 2))) == threes
assert set(flood_select(cube, (2, 2, 0))) == threes
assert set(flood_select(cube, (2, 2, 1))) == threes
assert set(flood_select(cube, (2, 2, 2))) == ones


# Test flood fill
grid = [
    [0, 0, 1],
    [1, 1, 0],
    [0, 1, 1]]
flood_fill(grid, (0, 1), 2)
assert grid == [
    [2, 2, 1],
    [1, 1, 2],
    [0, 1, 1]]
    
