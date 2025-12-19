import pytest


# @pytest.mark.parametrize(
#     "input,expected",
#     [
#         (2, 4),
#         (3, 6),
#         (0, 0)
#     ]
# )
# def test_double(input, expected):
#     assert double(input) == expected


def multiply(x, multiplier):
    return x * multiplier

import pytest

@pytest.fixture
def multiplier():
    return 3

@pytest.mark.parametrize("num,expected", [(1,3),(2,6),(0,0)])
def test_multiply(num, expected, multiplier):
    assert multiply(num, multiplier) == expected

def test_try():
    from collections import Counter
    s = "aaccccnb"
    counts = Counter(s)
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for char, count in sorted_counts[:3]:
        print(char, count)