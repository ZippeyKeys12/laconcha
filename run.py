# pylint: disable-all
from typing import Any

import streamlit as st

import SessionState
from laconcha import Image
from laconcha.filters import (ColorChannel, bilateral_filter, channel,
                              color_quantization, gaussian_blur, mean_filter,
                              median_filter, spread, swirl)

# SETUP

session_state: Any = SessionState.get(filters=[])

filter_dict = {
    'Bilateral Filter': (bilateral_filter, lambda i: [
        st.sidebar.slider('Diameter', 1, 15, 9, key=f'D{i}'),
        st.sidebar.slider('Std. Deviation (Color)', 0, 100, 75, key=f'C{i}'),
        st.sidebar.slider('Std. Deviation (Space)', 0, 100, 75, key=f'S{i}')
    ]),
    'Channel': (channel, lambda i: [
        st.sidebar.selectbox('Channel', list(ColorChannel),
                             format_func=lambda x: x.name, key=f'C{i}')
    ]),
    'Color Quantization': (color_quantization, lambda i: [
        st.sidebar.slider('# of Clusters', 1, 128, 16, key=f'#{i}')
    ]),
    'Gaussian Blur': (gaussian_blur, lambda i: [
        (st.sidebar.slider('Kernel Width', 0, 7, 5, key=f'W{i}'),
         st.sidebar.slider('Kernel Height', 0, 7, 5, key=f'H{i}')),
        st.sidebar.slider('Standard Deviation', 0, 10, 0, key=f'S{i}')
    ]),
    'Mean Filter': (mean_filter, lambda i: [
        (st.sidebar.slider('Kernel Width', 0, 7, 5, key=f'W{i}'),
         st.sidebar.slider('Kernel Height', 0, 7, 5, key=f'H{i}'))
    ]),
    'Median Filter': (median_filter, lambda i: [
        (st.sidebar.slider('Kernel Width', 0, 7, 5, key=f'W{i}'),
         st.sidebar.slider('Kernel Height', 0, 7, 5, key=f'H{i}'))
    ]),
    'Spread': (spread, lambda i: [
        st.sidebar.slider('Distance', 0, 15, 3, key=f'D{i}')
    ]),
    'Swirl': (swirl, lambda i: [
        st.sidebar.slider('Strength', 1, 100, 1, key=f'S{i}'),
        st.sidebar.slider('Radius', 1, 1000, 100, key=f'R{i}'),
        st.sidebar.slider('Rotation', 0, 360, 0, key=f'Ro{i}')
    ]),
}

# PAGE

st.header('Laconcha')

num_filters = len(session_state.filters)
if st.button('Add Filter'):
    session_state.filters.append(num_filters)
if st.button('Remove Filter') and num_filters > 0:
    session_state.filters.pop()


img = Image.open('test_images/netherlands-5039354_1280.jpg')
for i in session_state.filters:
    f = st.sidebar.selectbox('Type', list(
        filter_dict.keys()), key=f'FilterType{i}')
    f, args = filter_dict[f]
    img.apply_filter(f(*args(i)))


st.image(img.as_pil(), use_column_width=True)
