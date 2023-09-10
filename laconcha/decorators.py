import inspect
import random
from enum import Enum
from typing import Any, Callable, TypeVar, cast

import streamlit as st

from .ranges import Range
from .seed import Seed
from .util import RGBColor, format_name

T = TypeVar('T')


def _generate_args(o):
    if isinstance(o, list):
        return random.choice(o)

    if isinstance(o, tuple):
        return tuple(_generate_args(a) for a in o)

    if issubclass(o, Enum):
        return random.choice(list(o))

    if isinstance(o, Range):
        return o.random()

    if o is Seed or isinstance(o, Seed):
        return random.randint(0, int(16 * '1', base=2))

    if o is RGBColor:
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    if o is None:
        return None

    raise TypeError(f'Unrecognized type: {o}')


def _streamlit_args(label: str, o, i: int):
    key = f'{label}{i}'
    label = format_name(label)

    if isinstance(o, list):
        return st.selectbox(label, o, key=key)

    if isinstance(o, tuple):
        return tuple(_streamlit_args(f'{label}[{j}]', a, i) for j, a in enumerate(o))

    if issubclass(o, Enum):
        return st.selectbox(label, list(o), key=key)

    if isinstance(o, Range):
        return st.slider(label, o.start, o.stop - 1, o.default, o.step, key=key)

    if o is Seed or isinstance(o, Seed):
        return st.number_input(label, 0, int(16 * '1', base=2), key=key)

    if o is RGBColor:
        return (
            st.slider(f'{label}[R]', 0, 255, key=f'{key}R'),
            st.slider(f'{label}[G]', 0, 255, key=f'{key}G'),
            st.slider(f'{label}[B]', 0, 255, key=f'{key}B')
        )

    if o is None:
        return None

    raise TypeError(f'Unrecognized type: {o}')


def gen_meta(*args) -> Callable[[T], T]:
    def f(g: Any) -> T:
        g = cast(Any, g)
        fargs = inspect.getfullargspec(g).args

        if len(args) == 0:
            if len(fargs) == 0:
                g.generate = lambda: g()
                g.streamlit = lambda: g()

            else:
                g.generate = lambda: g
                g.streamlit = lambda: g

        else:
            g.generate = lambda: g(*[_generate_args(a) for a in args])
            g.streamlit = lambda i=0: g(
                *[_streamlit_args(*a, i) for a in zip(fargs, args)])

        return g

    return f
