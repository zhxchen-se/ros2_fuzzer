"""
ROS Fuzzer basic datatype strategies module.

:authors: Alias Robotics S.L. Borja Erice, Odei Olalde, Xabi Perez, Gorka Olalde
"""
import hypothesis.strategies as st
from hypothesis.errors import InvalidArgument
from collections import namedtuple

STRING_MIN_SIZE = 0
"""int: Minimal string size."""
STRING_MAX_SIZE = 1000
"""int: Maximal string size."""


def string(min_size=STRING_MIN_SIZE, max_size=STRING_MAX_SIZE):
    """
    Generate value for ROS builtin message type "string".

    :param min_size: int
        Minimal size to generate
    :param max_size: int
        Maximal size to generate
    :return: :func:`hypothesis.strategies.binary()`
        Strategy with preconfigured default values.
    """
    if not STRING_MIN_SIZE <= min_size <= max_size <= STRING_MAX_SIZE:
        raise InvalidArgument
    # average_size parameter is deprecated
    return st.text(min_size=min_size, max_size=max_size)


@st.composite
def time(draw, secs=st.integers(), nsecs=st.integers()):
    """
    Generate value for ROS builtin message type "time".

    :param secs: hypothesis_ros.message_fields.uint32()
        Seconds
    :param nsecs: hypothesis_ros.message_fields.uint32()
        Nano seconds
    :return: :class:`hypothesis_ros.message_fields.Time()`
        Strategy with preconfigured default values.
    """
    _Time = namedtuple('Time', 'secs nsecs')
    secs_value, nsecs_value = draw(secs), draw(nsecs)
    assert isinstance(secs_value, int), 'drew invalid sec={secs_value} from {secs} for integer field'.\
        format(secs_value, secs)
    assert isinstance(nsecs_value, int), 'drew invalid nsec={nsecs_value} from {nsecs} for integer field'.\
        format(nsecs_value, nsecs)
    return _Time(secs_value, nsecs_value)


@st.composite
def duration(draw, secs=st.integers(), nsecs=st.integers()):
    """
    Generate value for ROS builtin message type "duration".

    :param secs: hypothesis_ros.message_fields.int32()
        Seconds
    :param nsecs: hypothesis_ros.message_fields.int32()
        Nano seconds
    :return: :class:`hypothesis_ros.message_fields.Duration()`
        Namedtuple with drawn values for secs and nsecs.
    """
    _Duration = namedtuple('Duration', 'secs nsecs')
    secs_value, nsecs_value = draw(secs), draw(nsecs)
    assert isinstance(secs_value, int), 'drew invalid sec={secs_value} from {secs} for integer field'.\
        format(secs_value, secs)
    assert isinstance(nsecs_value, int), 'drew invalid nsec={nsecs_value} from {nsecs} for integer field'.\
        format(nsecs_value, nsecs)
    return _Duration(secs_value, nsecs_value)


def array(elements=None, min_size=None, max_size=None, unique_by=None, unique=None):
    """
    Generate variable length array with ROS builtin message types as elements.
    To generate a fixed length array define `min_size == max_size`.

    :param elements: hypothesis_ros.message_fields
        Strategies for pritive types from hypothesis_ros.message_fields.
    :param min_size: integer
        Minimal size of the array.
    :param max_size: integer
        Maximal size of the array.
    :param unique_by: callable
        Function returning a hashable type when given a value from elements.
        The resulting array (list) will satisfy `unique_by(result[i]) != unique_by(result[j])`.
    :param unique: boolean
        Function returning a hashable type. For comparison of directy object equality.
    :return: :func:`hypothesis.strategies.lists()`
        A variable or fixed length array containing values drawn from elements with
        length in the interval [min_size, max_size] (no bounds in that direction
        if these are None).
    """
    # Build kwargs dict, only include parameters that are not None
    # This is required for hypothesis >= 6.0 which doesn't accept None for size parameters
    kwargs = {'elements': elements}
    if min_size is not None:
        kwargs['min_size'] = min_size
    if max_size is not None:
        kwargs['max_size'] = max_size
    if unique_by is not None:
        kwargs['unique_by'] = unique_by
    if unique is not None:
        kwargs['unique'] = unique
    
    return st.lists(**kwargs)