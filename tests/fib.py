from __future__ import annotations


def fibonacci(n) -> int:
    if n <= 0:
        raise ValueError("The input must be a positive integer.")
    elif n == 1:
        return 0
    elif n == 2:
        return 1

    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b
