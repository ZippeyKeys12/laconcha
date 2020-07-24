# pylint: disable-all

import inspect
import random
from typing import Any, Callable, TypeVar, cast

import streamlit as st

from .ranges import Range
from .util import format_name

T = TypeVar('T')


def _generate_args(o):
    if isinstance(o, list):
        return random.choice(o)

    if isinstance(o, tuple):
        return tuple(_generate_args(a) for a in o)

    if isinstance(o, Range):
        return o.random()

    raise TypeError(f'Unrecognized type: {o}')


def _streamlit_args(label: str, o, i: int):
    key = f'{label}{i}'
    label = format_name(label)

    if isinstance(o, list):
        return st.selectbox(label, o, key=key)

    if isinstance(o, tuple):
        return tuple(_streamlit_args(f'{label}[{j}]', a, i) for j, a in enumerate(o))

    if isinstance(o, Range):
        return st.slider(label, o.start, o.stop - 1, o.default, o.step, key=key)

    raise TypeError(f'Unrecognized type: {o}')


def gen_meta(*args) -> Callable[[T], T]:
    def f(g: Any) -> T:
        g = cast(Any, g)
        g.generate = lambda: g(*[_generate_args(a) for a in args])
        g.streamlit = lambda i=0: g(*[_streamlit_args(*a, i) for a in zip(
            inspect.getfullargspec(f).args, args)])

        return g

    return f
