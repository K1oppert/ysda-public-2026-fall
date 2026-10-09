from collections import namedtuple
from time import perf_counter, sleep

from profiler import profiler


@profiler
def ackermann(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    if m > 0 and n == 0:
        return ackermann(m - 1, 1)
    if m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    assert False, 'unreachable'


@profiler
def strange_function(a, b, c=1, d=2):  # type: ignore
    return a.foo + b.bar + c + d


def test_example() -> None:
    start = perf_counter()
    result = ackermann(3, 2)
    delta = perf_counter() - start

    assert ackermann.calls == 541
    assert 0 <= ackermann.last_time_taken <= delta, 'Wrong last time taken'
    assert result == 29


def test_profiler_one_call() -> None:
    start = perf_counter()
    result = ackermann(3, 2)
    delta = perf_counter() - start

    assert ackermann.calls == 541
    assert 0 <= ackermann.last_time_taken <= delta, 'Wrong last time taken'
    assert result == 29


def test_profiler_many_call() -> None:
    _ = ackermann(0, 1)
    _ = ackermann(3, 2)
    assert ackermann.calls == 541


def test_profiler_strange_akkerman() -> None:
    foo = namedtuple('foo', ['foo', 'bar'])
    expected_result = 10
    result = strange_function(foo(1, 2), foo(1, 2), 3, 4)
    assert result == expected_result


def test_profiler_not_changes_func() -> None:
    @profiler
    def f() -> None:
        """test"""
        pass

    assert f.__name__ == 'f'
    assert f.__doc__ == 'test'
    assert f.__module__ == __name__


def test_timer_covers_outer_call() -> None:
    @profiler
    def countdown(depth: int) -> None:
        if depth:
            sleep(0.01)
            countdown(depth - 1)

    start = perf_counter()
    countdown(2)
    elapsed = perf_counter() - start
    assert countdown.calls == 3
    assert 0.02 <= countdown.last_time_taken <= elapsed
    countdown(0)
    assert countdown.calls == 1
    assert countdown.last_time_taken >= 0



def test_uses_performance_counter(monkeypatch) -> None:  # type: ignore
    import runpy
    import time
    import profiler as profiler_module

    # Управляем показаниями таймера: реальная скорость компьютера не важна.
    counter = [100.0]
    monkeypatch.setattr(time, 'perf_counter', lambda: counter[0])
    monkeypatch.setattr(time, 'perf_counter_ns', lambda: int(counter[0] * 1_000_000_000))

    # Загружаем решение после подмены: работает и с import time,
    # и с from time import perf_counter.
    decorate = runpy.run_path(profiler_module.__file__)['profiler']

    @decorate
    def work() -> int:
        counter[0] += 0.25
        return 42

    assert work() == 42
    assert work.calls == 1
    assert work.last_time_taken == 0.25
