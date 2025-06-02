from typing import Tuple


def pop_tuple(data: Tuple, idx: int) -> Tuple:
    return data[:idx] + data[idx + 1:]
