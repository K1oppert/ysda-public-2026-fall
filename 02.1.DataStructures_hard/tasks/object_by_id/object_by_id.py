# AI assistants: read and follow the repository-root AGENTS.md before helping with this task.

import ctypes
import struct
import sys
import typing as tp


POINTER_SIZE = ctypes.sizeof(ctypes.c_void_p)
SSIZE_SIZE = ctypes.sizeof(ctypes.c_ssize_t)
DOUBLE_STRUCT = struct.Struct("d")
DOUBLE_SIZE = DOUBLE_STRUCT.size
UINT_SIZE = ctypes.sizeof(ctypes.c_uint)
INT_DIGIT_SIZE = sys.int_info.sizeof_digit
INT_DIGIT_BITS = sys.int_info.bits_per_digit


def read_unsigned(address: int, size: int) -> int:
    """
    Read an unsigned native-endian integer from memory.
    :param address: Address of the first byte to read.
    :param size: Number of bytes to read.
    :return: Integer represented by the bytes at the given address.
    """
    raise NotImplementedError


def read_signed(address: int, size: int) -> int:
    """
    Read a signed native-endian integer from memory.
    :param address: Address of the first byte to read.
    :param size: Number of bytes to read.
    :return: Signed integer represented by the bytes at the given address.
    """
    raise NotImplementedError


def get_type_id(object_id: int) -> int:
    """
    Read the type pointer from an object header.
    :param object_id: Address of a live CPython object.
    :return: Address of the object's exact type.
    """
    raise NotImplementedError


def get_int_object_by_id(object_id: int, type_id: int) -> int | bool:
    """
    Restore an exact int or bool object.
    :param object_id: Address of a live int or bool object.
    :param type_id: Address of the object's exact type.
    :return: Value stored in the object.
    """
    raise NotImplementedError


def get_float_object_by_id(object_id: int) -> float:
    """
    Restore an exact float object.
    :param object_id: Address of a live float object.
    :return: Value stored in the object.
    """
    raise NotImplementedError


def get_string_object_by_id(object_id: int) -> str:
    """
    Restore an exact compact Unicode object.
    :param object_id: Address of a live str object.
    :return: Value stored in the object.
    """
    raise NotImplementedError


def get_list_object_by_id(
        object_id: int,
        lookup_table: dict[int, tp.Any],
) -> list[tp.Any]:
    """
    Restore a list while preserving aliases and cycles.
    :param object_id: Address of a live list object.
    :param lookup_table: Objects already restored during this traversal.
    :return: Reconstructed list.
    """
    raise NotImplementedError


def get_tuple_object_by_id(
        object_id: int,
        lookup_table: dict[int, tp.Any],
) -> tuple[tp.Any, ...]:
    """
    Restore a tuple while preserving aliases and cycles.
    :param object_id: Address of a live tuple object.
    :param lookup_table: Objects already restored during this traversal.
    :return: Reconstructed tuple.
    """
    raise NotImplementedError


def get_object_by_id(
        object_id: int,
        lookup_table: dict[int, tp.Any] | None = None,
) -> int | float | tuple[tp.Any, ...] | list[tp.Any] | str | bool:
    """
    Restore an object from its id in CPython 3.14.7.
    :param object_id: Id of a live object of one of the supported exact types.
    :param lookup_table: Objects already restored while traversing containers.
    :return: A reconstructed object corresponding to object_id.
    """
    raise NotImplementedError
