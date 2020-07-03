# pylint: disable-all

from typing import Any

import streamlit as st

import SessionState
from laconcha import Image
from laconcha.curves import (circular, cosine, cubic, exponential, inverse,
                             logarithm, quadratic, sine, smooth_step,
                             smoother_step, smoothest_step, square_root)
from laconcha.filters import (ColorChannel, ColorMode, autocontrast,
                              bilateral_filter, bottom, brightness, channel,
                              color_quantization, contrast, convert_color,
                              crop, curve, equalize, fit, gaussian_blur, hflip,
                              hmirror, integral, invert, left, max_filter,
                              mean_filter, median_filter, min_filter,
                              mode_filter, oct_mirror, posterize, quad_mirror,
                              right, rotate, saturation, scale, sharpness,
                              shear, solarize, spread, swirl, top, translate,
                              unsharpen, vflip, vmirror)
from laconcha.generators import gaussian_noise, white_noise
from laconcha.util import format_name

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
    'As OpenCV': (lambda: lambda i: Image.from_opencv(i.as_opencv()), lambda i, h, w: []),
    'As PIL': (lambda: lambda i: Image.from_pil(i.as_pil()), lambda i, h, w: []),
    'As Scikit': (lambda: lambda i: Image.from_scikit(i.as_scikit()), lambda i, h, w: []),
    'Autocontrast': (autocontrast, lambda i, h, w: [
        st.slider('Cutoff', 0, 49, 0, key=f'C{i}')
    ]),
    'Bilateral Filter': (bilateral_filter, lambda i, h, w: [
        st.slider('Diameter', 1, 15, 9, key=f'D{i}'),
        st.slider('Std. Deviation (Color)', 0, 100, 75, key=f'C{i}'),
        st.slider('Std. Deviation (Space)', 0, 100, 75, key=f'S{i}')
    ]),
    'Bottom': (bottom, lambda i, h, w: [
        st.slider('Pixels', 0, h, h, key=f'P{i}')
    ]),
    'Brightness': (brightness, lambda i, h, w: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Channel': (channel, lambda i, h, w: [
        st.selectbox('Channel', list(ColorChannel),
                     format_func=lambda x: x.name, key=f'C{i}')
    ]),
    'Color Quantization': (color_quantization, lambda i, h, w: [
        st.slider('# of Clusters', 1, 128, 16, key=f'#{i}')
    ]),
    'Contrast': (contrast, lambda i, h, w: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Convert Color Mode': (convert_color, lambda i, h, w: [
        st.selectbox('From', list(ColorMode),
                     format_func=lambda x: x.name, key=f'F{i}'),
        st.selectbox('To', list(ColorMode),
                     format_func=lambda x: x.name, key=f'T{i}')
    ]),
    'Crop': (crop, lambda i, h, w: [
        st.slider('Height', 0, h, h, key=f'H{i}'),
        st.slider('Width', 0, w, w, key=f'W{i}')
    ]),
    'Curve': (curve, lambda i, h, w: [
        st.selectbox('Function', [
            circular, cosine, cubic, exponential, inverse, logarithm,
            sine, smooth_step, smoother_step, smoothest_step, square_root,
            quadratic],
            format_func=lambda x: format_name(x.__name__))
    ]),
    'Equalize': (equalize, lambda i, h, w: []),
    'Fit': (fit, lambda i, h, w: [
        st.slider('Height', 0, h, h, key=f'H{i}'),
        st.slider('Width', 0, w, w, key=f'W{i}')
    ]),
    'Gaussian Blur': (gaussian_blur, lambda i, h, w: [
        (st.slider('Kernel Width', 1, 7, 5, 2, key=f'W{i}'),
         st.slider('Kernel Height', 1, 7, 5, 2, key=f'H{i}')),
        st.slider('Standard Deviation', 0.0, 10.0, 0.0, key=f'S{i}')
    ]),
    'Horizontal Flip': (hflip, lambda i, h, w: []),
    'Horizontal Mirror': (hmirror, lambda i, h, w: []),
    'Integral': (integral, lambda i, h, w: []),
    'Invert': (invert, lambda i, h, w: []),
    'Left': (left, lambda i, h, w: [
        st.slider('Pixels', 0, w, w, key=f'P{i}')
    ]),
    'Max Filter': (max_filter, lambda i, h, w: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Mean Filter': (mean_filter, lambda i, h, w: [
        (st.slider('Kernel Width', 1, 7, 5, key=f'W{i}'),
         st.slider('Kernel Height', 1, 7, 5, key=f'H{i}'))
    ]),
    'Median Filter': (median_filter, lambda i, h, w: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Min Filter': (min_filter, lambda i, h, w: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Mode Filter': (mode_filter, lambda i, h, w: [
        st.slider('Diameter', 1, 15, 9, 2, key=f'D{i}')
    ]),
    'Oct-Mirror': (oct_mirror, lambda i, h, w: []),
    'Posterize': (posterize, lambda i, h, w: [
        st.slider('Bits', 1, 8, 8, key=f'B{i}')
    ]),
    'Quad-Mirror': (quad_mirror, lambda i, h, w: []),
    'Right': (right, lambda i, h, w: [
        st.slider('Pixels', 0, w, w, key=f'P{i}')
    ]),
    'Rotate': (rotate, lambda i, h, w: [
        st.slider('Angle', 0.0, 360.0, 0.0, key=f'A{i}')
    ]),
    'Saturation': (saturation, lambda i, h, w: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Scale': (scale, lambda i, h, w: [
        (st.slider('Scale X', .1, 10.0, 1.0, key=f'X{i}'),
         st.slider('Scale Y', .1, 10.0, 1.0, key=f'Y{i}'))
    ]),
    'Sharpness': (sharpness, lambda i, h, w: [
        st.slider('Factor', 0.0, 2.0, 1.0, key=f'F{i}')
    ]),
    'Shear': (shear, lambda i, h, w: [
        st.slider('Angle', 0.0, 90.0, 0.0, key=f'A{i}')
    ]),
    'Sine': (sine, lambda i, h, w: []),
    'Solarize': (solarize, lambda i, h, w: [
        st.slider('Threshold', 0, 255, 128, key=f'B{i}')
    ]),
    'Spread': (spread, lambda i, h, w: [
        st.slider('Distance', 0, 15, 3, key=f'D{i}')
    ]),
    'Swirl': (swirl, lambda i, h, w: [
        (st.slider('Center X', 0, w, w // 2, key=f'X{i}'),
         st.slider('Center Y', 0, h, h // 2, key=f'Y{i}')),
        st.slider('Strength', -100.0, 100.0, 0.0, key=f'S{i}'),
        st.slider('Radius', 1.0, float(max(h, w)), 100.0, key=f'R{i}')
    ]),
    'Top': (top, lambda i, h, w: [
        st.slider('Pixels', 0, h, h, key=f'P{i}')
    ]),
    'Translate': (translate, lambda i, h, w: [
        (st.slider('Offset X', -w, w, 0, key=f'X{i}'),
         st.slider('Offset Y', -h, h, 0, key=f'Y{i}'))
    ]),
    'Unsharpen': (unsharpen, lambda i, h, w: [
        st.slider('Radius', 0, 7, 2, key=f'R{i}'),
        st.slider('Percent', 0, 200, 150, key=f'P{i}'),
        st.slider('Threshold', 0, 10, 3, key=f'T{i}')
    ]),
    'Vertical Flip': (vflip, lambda i, h, w: []),
    'Vertical Mirror': (vmirror, lambda i, h, w: [])
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

    f, f_args = filter_dict[st.selectbox('Type', list(
        filter_dict.keys()), key=f'FilterType{i}')]
    with st.spinner('Applying Filter...'):
        img = img.apply_filter(f(*f_args(i, h, w)))  # type: ignore
        h, w = img.size

    st.image(img.as_pil(), use_column_width=True)

