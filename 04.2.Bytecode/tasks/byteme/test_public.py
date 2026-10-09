import dataclasses
import dis
import io
from typing import Any, Callable
import sys

import pytest

import byteme


@dataclasses.dataclass
class Case:
    func: Callable[..., Any]
    expected_dis_out: str

    def __str__(self) -> str:
        return self.func.__name__


TEST_CASES = [
    Case(
        func=byteme.f0,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_CONST               0 (None)
  4       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f1,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_SMALL_INT           0
  4       STORE_FAST               0 (a)
  6       LOAD_FAST_BORROW         0 (a)
  8       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f2,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_SMALL_INT           0
  4       STORE_FAST               0 (a)
  6       LOAD_GLOBAL              1 (print + NULL)
 16       LOAD_FAST_BORROW         0 (a)
 18       CALL                     1
 26       POP_TOP
 28       LOAD_CONST               1 (None)
 30       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f3,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_SMALL_INT           0
  4       STORE_FAST               0 (a)
  6       LOAD_FAST_BORROW         0 (a)
  8       LOAD_SMALL_INT           1
 10       BINARY_OP               13 (+=)
 22       STORE_FAST               0 (a)
 24       LOAD_GLOBAL              1 (print + NULL)
 34       LOAD_FAST_BORROW         0 (a)
 36       CALL                     1
 44       POP_TOP
 46       LOAD_CONST               1 (None)
 48       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f4,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_GLOBAL              1 (range + NULL)
 12       LOAD_SMALL_INT          10
 14       CALL                     1
 22       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f5,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_GLOBAL              1 (range + NULL)
 12       LOAD_SMALL_INT          10
 14       CALL                     1
 22       GET_ITER
 24       FOR_ITER                14 (to L2)
 28       STORE_FAST               0 (i)
 30       LOAD_GLOBAL              3 (print + NULL)
 40       LOAD_FAST_BORROW         0 (i)
 42       CALL                     1
 50       POP_TOP
 52       JUMP_BACKWARD           16 (to L1)
 56       END_FOR
 58       POP_ITER
 60       LOAD_CONST               1 (None)
 62       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f6,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_SMALL_INT           0
  4       STORE_FAST               0 (a)
  6       LOAD_GLOBAL              1 (range + NULL)
 16       LOAD_SMALL_INT          10
 18       CALL                     1
 26       GET_ITER
 28       FOR_ITER                12 (to L2)
 32       STORE_FAST               1 (i)
 34       LOAD_FAST_BORROW         0 (a)
 36       LOAD_SMALL_INT           1
 38       BINARY_OP               13 (+=)
 50       STORE_FAST               0 (a)
 52       JUMP_BACKWARD           14 (to L1)
 56       END_FOR
 58       POP_ITER
 60       LOAD_GLOBAL              3 (print + NULL)
 70       LOAD_FAST_BORROW         0 (a)
 72       CALL                     1
 80       POP_TOP
 82       LOAD_CONST               1 (None)
 84       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f8,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_SMALL_INT           1
  4       LOAD_SMALL_INT           2
  6       STORE_FAST_STORE_FAST   16 (y, x)
  8       LOAD_CONST               1 (None)
 10       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f9,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_SMALL_INT           1
  4       LOAD_SMALL_INT           1
  6       COMPARE_OP              88 (bool(==))
 10       POP_JUMP_IF_FALSE        3 (to L1)
 14       NOT_TAKEN
 16       LOAD_SMALL_INT           1
 18       RETURN_VALUE
 20       LOAD_SMALL_INT           2
 22       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f10,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_GLOBAL              1 (range + NULL)
 12       LOAD_SMALL_INT          10
 14       CALL                     1
 22       GET_ITER
 24       FOR_ITER                13 (to L3)
 28       STORE_FAST               0 (i)
 30       LOAD_FAST_BORROW         0 (i)
 32       LOAD_SMALL_INT           3
 34       COMPARE_OP              88 (bool(==))
 38       POP_JUMP_IF_TRUE         3 (to L2)
 42       NOT_TAKEN
 44       JUMP_BACKWARD           12 (to L1)
 48       POP_TOP
 50       LOAD_CONST               1 (None)
 52       RETURN_VALUE
 54       END_FOR
 56       POP_ITER
 58       LOAD_CONST               1 (None)
 60       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f11,
        expected_dis_out='''\
  0       RESUME                   0
  2       BUILD_LIST               0
  4       LOAD_CONST               3 ((1, 2, 3))
  6       LIST_EXTEND              1
  8       STORE_FAST               0 (list_)
 10       LOAD_CONST               1 ('a')
 12       LOAD_SMALL_INT           1
 14       LOAD_CONST               2 ('b')
 16       LOAD_SMALL_INT           2
 18       BUILD_MAP                2
 20       STORE_FAST               1 (dict_)
 22       LOAD_FAST_BORROW_LOAD_FAST_BORROW 1 (list_, dict_)
 24       BUILD_TUPLE              2
 26       RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f12,
        expected_dis_out='''\
  0       RESUME                   0
  2       LOAD_SMALL_INT           1
  4       STORE_FAST               0 (a)
  6       LOAD_SMALL_INT           2
  8       STORE_FAST               1 (b)
 10       LOAD_SMALL_INT           3
 12       STORE_FAST               2 (c)
 14       LOAD_SMALL_INT           4
 16       STORE_FAST               3 (d)
 18       LOAD_SMALL_INT           5
 20       STORE_FAST               4 (e)
 22       LOAD_FAST_BORROW_LOAD_FAST_BORROW 1 (a, b)
 24       LOAD_FAST_BORROW         2 (c)
 26       BINARY_OP                5 (*)
 38       LOAD_FAST_BORROW_LOAD_FAST_BORROW 52 (d, e)
 40       BINARY_OP                8 (**)
 52       BINARY_OP               11 (/)
 64       BINARY_OP                0 (+)
 76       RETURN_VALUE
'''
    ),
]


def test_version() -> None:
    """
    To do this task you need python=3.14.7
    """
    assert '3.14.7' == sys.version.split(' ', maxsplit=1)[0]


def strip_dis_out(dis_out: str) -> str:
    """Strip first 11 chars from dis_out and remove empty lines"""
    return '\n'.join(line[11:] for line in dis_out.split('\n') if line) + '\n'


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_byteme(t: Case) -> None:
    out = io.StringIO()
    dis.dis(t.func, file=out, show_offsets=True)
    actual_dis_out = out.getvalue()
    print(actual_dis_out)
    assert strip_dis_out(actual_dis_out) == t.expected_dis_out
