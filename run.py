# pylint: disable-all
from typing import Any

import streamlit as st

import SessionState
from laconcha import Image
from laconcha.filters import (ColorChannel, ColorMode, autocontrast,
                              bilateral_filter, brightness, channel,
                              color_quantization, contrast, convert_color,
                              equalize, gaussian_blur, hflip, integral, invert,
                              max_filter, mean_filter, median_filter,
                              min_filter, mode_filter, posterize, rotate,
                              saturation, scale, sharpness, shear, solarize,
                              spread, swirl, translate, unsharpen, vflip)
from laconcha.generators import gaussian_noise, white_noise

# SETUP

img_path = 'test_images/stained-glass-1181864_1920.jpg'

session_state: Any = SessionState.get(filters=[])

generator_dict = {
    'File': (lambda size: crop(size)(Image.open(st.file_uploader('Choose an Image', ['.png', '.jpg']) or img_path)), lambda: []),
    'Gaussian Noise': (gaussian_noise, lambda: [
        st.number_input('Seed', 0, 100, 0)
    ]),
    'White Noise': (white_noise, lambda: [
        st.number_input('Seed', 0, 100, 0)
    ])
}

filter_dict = {
    'As OpenCV': (lambda: lambda i: Image.from_opencv(i.as_opencv()), lambda i: []),
    'As PIL': (lambda: lambda i: Image.from_pil(i.as_pil()), lambda i: []),
    'As Scikit': (lambda: lambda i: Image.from_scikit(i.as_scikit()), lambda i: []),
    'Autocontrast': (autocontrast, lambda i: [
        st.slider('Cutoff', 0, 49, 0, key=f'C{i}')
    ]),
    'Bilateral Filter': (bilateral_filter, lambda i: [
        st.slider('Diameter', 1, 15, 9, key=f'D{i}'),
        st.slider('Std. Deviation (Color)', 0, 100, 75, key=f'C{i}'),
        st.slider('Std. Deviation (Space)', 0, 100, 75, key=f'S{i}')
    ]),
    'Brightness': (brightness, lambda i: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Channel': (channel, lambda i: [
        st.selectbox('Channel', list(ColorChannel),
                     format_func=lambda x: x.name, key=f'C{i}')
    ]),
    'Color Quantization': (color_quantization, lambda i: [
        st.slider('# of Clusters', 1, 128, 16, key=f'#{i}')
    ]),
    'Contrast': (contrast, lambda i: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Convert Color Mode': (convert_color, lambda i: [
        st.selectbox('From', list(ColorMode),
                     format_func=lambda x: x.name, key=f'F{i}'),
        st.selectbox('To', list(ColorMode),
                     format_func=lambda x: x.name, key=f'T{i}')
    ]),
    'Equalize': (equalize, lambda i: []),
    'Gaussian Blur': (gaussian_blur, lambda i: [
        (st.slider('Kernel Width', 1, 7, 5, 2, key=f'W{i}'),
         st.slider('Kernel Height', 1, 7, 5, 2, key=f'H{i}')),
        st.slider('Standard Deviation', 0.0, 10.0, 0.0, key=f'S{i}')
    ]),
    'Horizontal Flip': (hflip, lambda i: []),
    'Integral': (integral, lambda i: []),
    'Invert': (invert, lambda i: []),
    'Max Filter': (max_filter, lambda i: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Mean Filter': (mean_filter, lambda i: [
        (st.slider('Kernel Width', 1, 7, 5, key=f'W{i}'),
         st.slider('Kernel Height', 1, 7, 5, key=f'H{i}'))
    ]),
    'Median Filter': (median_filter, lambda i: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Min Filter': (min_filter, lambda i: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Mode Filter': (mode_filter, lambda i: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Posterize': (posterize, lambda i: [
        st.slider('Bits', 1, 8, 8, key=f'B{i}')
    ]),
    'Rotate': (rotate, lambda i: [
        st.slider('Angle', 0.0, 360.0, 0.0, key=f'A{i}')
    ]),
    'Saturation': (saturation, lambda i: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Scale': (scale, lambda i: [
        (st.slider('Scale X', .1, 10.0, 1.0, key=f'X{i}'),
         st.slider('Scale Y', .1, 10.0, 1.0, key=f'Y{i}'))
    ]),
    'Sharpness': (sharpness, lambda i: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Shear': (shear, lambda i: [
        st.slider('Angle', 0.0, 90.0, 0.0, key=f'A{i}')
    ]),
    'Solarize': (solarize, lambda i: [
        st.slider('Threshold', 0, 255, 128, key=f'B{i}')
    ]),
    'Spread': (spread, lambda i: [
        st.slider('Distance', 0, 15, 3, key=f'D{i}')
    ]),
    'Swirl': (swirl, lambda i: [
        (st.number_input('Center X', key=f'X{i}'),
         st.number_input('Center Y', key=f'Y{i}')),
        st.slider('Strength', -100.0, 100.0, 0.0, key=f'S{i}'),
        st.slider('Radius', 1.0, 2000.0, 100.0, key=f'R{i}')
    ]),
    'Translate': (translate, lambda i: [
        (st.slider('Offset X', -400, 400, 0, key=f'X{i}'),
         st.slider('Offset Y', -400, 400, 0, key=f'Y{i}'))
    ]),
    'Unsharpen': (unsharpen, lambda i: [
        st.slider('Radius', 0, 7, 2, key=f'R{i}'),
        st.slider('Percent', 0, 200, 150, key=f'P{i}'),
        st.slider('Threshold', 0, 10, 3, key=f'T{i}')
    ]),
    'Vertical Flip': (vflip, lambda i: [])
}

# PAGE

st.header('Laconcha')

num_filters = len(session_state.filters)
if st.button('Add Filter'):
    session_state.filters.append(num_filters)
if st.button('Remove Filter') and num_filters > 0:
    session_state.filters.pop()


h = st.slider('Height', 0, 2000, 1000, 2)
w = st.slider('Width', 0, 2000, 1000, 2)
g, g_args = generator_dict[st.selectbox('Image', list(generator_dict.keys()))]
img = g((h, w), *g_args())  # type: ignore

st.image(img.as_pil(), use_column_width=True)

for i in session_state.filters:
    st.markdown('---')

    f = st.selectbox('Type', list(
        filter_dict.keys()), key=f'FilterType{i}')
    f, args = filter_dict[f]
    with st.spinner('Applying Filter...'):
        img = img.apply_filter(f(*args(i)))

    st.image(img.as_pil(), use_column_width=True)

