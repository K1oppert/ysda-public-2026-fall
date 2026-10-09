from typing import Any, TypeVar

from _pytest.capture import CaptureFixture  # typing

from lru_cache import cache


@cache(20)
def binomial(n: int, k: int) -> int:
    if k > n:
        return 0
    if k == 0:
        return 1
    return binomial(n - 1, k) + binomial(n - 1, k - 1)


@cache(2048)
def ackermann(m: int, n: int) -> int:
    print(f'Calculating for {m} and {n}...')
    if m == 0:
        return n + 1
    if m > 0 and n == 0:
        return ackermann(m - 1, 1)
    if m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    assert False, 'unreachable'


@cache(1)
def join(args: tuple[Any, ...] | Any) -> tuple[Any, ...]:
    result: tuple[Any, ...] = tuple()
    for arg in args:
        if isinstance(arg, tuple):
            result += join(arg)
        else:
            result += (arg,)
    return result


def test_cache_not_changes_func() -> None:
    T = TypeVar('T')

    @cache(1)
    def func(a: T) -> T:
        """test doc"""
        return a

    assert func.__name__ == 'func'
    assert func.__doc__ == 'test doc'
    assert func.__module__ == __name__


def test_binomial() -> None:
    result = sum(binomial(30, i) for i in range(31))
    assert result == 2 ** 30


def test_ackermann(capsys: CaptureFixture[str]) -> None:
    result = ackermann(3, 7)
    assert result == 1021
    assert capsys.readouterr().out.count('\n') == 2558


def test_join_lists() -> None:
    result = join(((1, 2, 3), 1, (1, 2, 3, 4, ((1, 2), 2, 3))))
    assert result == (1, 2, 3, 1, 1, 2, 3, 4, 1, 2, 2, 3)


def test_max_cache_size() -> None:
    calls_count = 0
    cache_size = 8

    @cache(cache_size)
    def simple_id(i: int) -> int:
        nonlocal calls_count
        calls_count += 1
        return i

    args = tuple(range(cache_size))
    result = tuple(map(simple_id, args))
    assert result == args
    assert calls_count == cache_size

    args = tuple(range(cache_size, cache_size * 2))
    result = tuple(map(simple_id, args))
    assert result == args
    assert calls_count == cache_size * 2

    args = tuple(range(cache_size))
    result = tuple(map(simple_id, args))
    assert result == args
    assert calls_count == cache_size * 3


def test_cache_hit_updates_recency() -> None:
    calls: list[int] = []

    @cache(2)
    def identity(value: int) -> int:
        calls.append(value)
        return value

    for value in (1, 2, 1, 3, 1, 2):
        assert identity(value) == value
    assert calls == [1, 2, 3, 2]


def test_none_result_is_cached() -> None:
    calls = 0

    @cache(2)
    def no_result(*, left: int, right: int) -> None:
        nonlocal calls
        calls += 1

    assert no_result(left=1, right=2) is None
    assert no_result(left=1, right=2) is None
    assert calls == 1


def test_zero_size_does_not_cache() -> None:
    calls = 0

    @cache(0)
    def identity(value: int) -> int:
        nonlocal calls
        calls += 1
        return value

    assert identity(1) == identity(1) == 1
    assert calls == 2


def test_keyword_order_is_preserved() -> None:
    calls = 0

    @cache(2)
    def keys(**kwargs: int) -> tuple[str, ...]:
        nonlocal calls
        calls += 1
        return tuple(kwargs)

    assert keys(left=1, right=2) == ('left', 'right')
    assert keys(right=2, left=1) == ('right', 'left')
    assert keys(left=1, right=2) == ('left', 'right')
    assert keys(right=2, left=1) == ('right', 'left')
    assert calls == 2
