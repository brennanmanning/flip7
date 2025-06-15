from typing import Tuple


def pop_tuple(data: Tuple, idx: int) -> Tuple:
    return data[:idx] + data[idx + 1 :]


def bounded_add(val: int, bound: int, adder: int = 1):
    val = val + adder
    if val >= bound:
        return 0
    else:
        return val
