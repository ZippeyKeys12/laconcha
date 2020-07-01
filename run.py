# pylint: disable-all
from typing import Any

import streamlit as st

import SessionState
from laconcha import Image
from laconcha.filters import (ColorChannel, ColorMode, bilateral_filter,
                              brightness, channel, color_quantization,
                              contrast, convert_color, gaussian_blur, integral,
                              max_filter, mean_filter, median_filter,
                              min_filter, mode_filter, rotate, saturation,
                              scale, sharpness, shear, spread, swirl,
                              translate, unsharpen)

# SETUP

session_state: Any = SessionState.get(filters=[])

filter_dict = {
    'As OpenCV': (lambda: lambda i: Image.from_opencv(i.as_opencv()), lambda i: []),
    'As PIL': (lambda: lambda i: Image.from_pil(i.as_pil()), lambda i: []),
    'As Scikit': (lambda: lambda i: Image.from_scikit(i.as_scikit()), lambda i: []),
    'Bilateral Filter': (bilateral_filter, lambda i: [
        st.sidebar.slider('Diameter', 1, 15, 9, key=f'D{i}'),
        st.sidebar.slider('Std. Deviation (Color)', 0, 100, 75, key=f'C{i}'),
        st.sidebar.slider('Std. Deviation (Space)', 0, 100, 75, key=f'S{i}')
    ]),
    'Brightness': (brightness, lambda i: [
        st.sidebar.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Channel': (channel, lambda i: [
        st.sidebar.selectbox('Channel', list(ColorChannel),
                             format_func=lambda x: x.name, key=f'C{i}')
    ]),
    'Color Quantization': (color_quantization, lambda i: [
        st.sidebar.slider('# of Clusters', 1, 128, 16, key=f'#{i}')
    ]),
    'Contrast': (contrast, lambda i: [
        st.sidebar.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Convert Color Mode': (convert_color, lambda i: [
        st.sidebar.selectbox('From', list(ColorMode),
                             format_func=lambda x: x.name, key=f'F{i}'),
        st.sidebar.selectbox('To', list(ColorMode),
                             format_func=lambda x: x.name, key=f'T{i}')
    ]),
    'Gaussian Blur': (gaussian_blur, lambda i: [
        (st.sidebar.slider('Kernel Width', 1, 7, 5, 2, key=f'W{i}'),
         st.sidebar.slider('Kernel Height', 1, 7, 5, 2, key=f'H{i}')),
        st.sidebar.slider('Standard Deviation', 0.0, 10.0, 0.0, key=f'S{i}')
    ]),
    'Integral': (integral, lambda i: []),
    'Max Filter': (max_filter, lambda i: [
        st.sidebar.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Mean Filter': (mean_filter, lambda i: [
        (st.sidebar.slider('Kernel Width', 1, 7, 5, key=f'W{i}'),
         st.sidebar.slider('Kernel Height', 1, 7, 5, key=f'H{i}'))
    ]),
    'Median Filter': (median_filter, lambda i: [
        st.sidebar.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Min Filter': (min_filter, lambda i: [
        st.sidebar.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Mode Filter': (mode_filter, lambda i: [
        st.sidebar.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Rotate': (rotate, lambda i: [
        st.sidebar.slider('Angle', 0.0, 360.0, 0.0, key=f'A{i}')
    ]),
    'Saturation': (saturation, lambda i: [
        st.sidebar.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Scale': (scale, lambda i: [
        (st.sidebar.slider('Scale X', .1, 10.0, 1.0, key=f'X{i}'),
         st.sidebar.slider('Scale Y', .1, 10.0, 1.0, key=f'Y{i}'))
    ]),
    'Sharpness': (sharpness, lambda i: [
        st.sidebar.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Shear': (shear, lambda i: [
        st.sidebar.slider('Angle', 0.0, 90.0, 0.0, key=f'A{i}')
    ]),
    'Spread': (spread, lambda i: [
        st.sidebar.slider('Distance', 0, 15, 3, key=f'D{i}')
    ]),
    'Swirl': (swirl, lambda i: [
        (st.sidebar.number_input('Center X', key=f'X{i}'),
         st.sidebar.number_input('Center Y', key=f'Y{i}')),
        st.sidebar.slider('Strength', 1.0, 100.0, 1.0, key=f'S{i}'),
        st.sidebar.slider('Radius', 1.0, 1000.0, 100.0, key=f'R{i}')
    ]),
    'Translate': (translate, lambda i: [
        (st.sidebar.slider('Offset X', -400, 400, 0, key=f'X{i}'),
         st.sidebar.slider('Offset Y', -400, 400, 0, key=f'Y{i}'))
    ]),
    'Unsharpen': (unsharpen, lambda i: [
        st.sidebar.slider('Radius', 0, 7, 2, key=f'R{i}'),
        st.sidebar.slider('Percent', 0, 200, 150, key=f'P{i}'),
        st.sidebar.slider('Threshold', 0, 10, 3, key=f'T{i}')
    ])
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
