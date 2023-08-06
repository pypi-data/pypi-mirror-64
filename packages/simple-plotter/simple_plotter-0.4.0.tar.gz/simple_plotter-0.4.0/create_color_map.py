"""
create_color_map.py  - script to create equally spaced HSV colors

Copyright (C) 2020 Thies Hecker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import numpy as np
import matplotlib.pyplot as plt


def interpolate_color(color_values, angle):
    """Interpolates a single color profile"""

    for i, color_val in enumerate(color_values):
        if color_val[0] > angle:
            angle0 = color_values[i-1][0]
            color0 = color_values[i-1][1]
            angle1 = color_val[0]
            color1 = color_val[1]
            break

    int_val = (angle - angle0) * (color1 - color0) / (angle1 - angle0) + color0

    return int_val


def calculate_colors(S, V, no_colors):
    """Calculates the color values"""

    ubound = V
    lbound = V * (1 - S)

    red_values = [
        (0., ubound),
        (60., ubound),
        (120., lbound),
        (180., lbound),
        (240., lbound),
        (300., ubound),
        (360., ubound)
    ]

    green_values = [
        (0., lbound),
        (60., ubound),
        (120., ubound),
        (180., ubound),
        (240., lbound),
        (300., lbound),
        (360., lbound)
    ]

    blue_values = [
        (0., lbound),
        (60., lbound),
        (120., lbound),
        (180., ubound),
        (240., ubound),
        (300., ubound),
        (360., lbound)
    ]

    # calculate color anlges
    rgb_values = []
    angle = 0
    offset = 360
    counter = 0
    angles = []
    while len(rgb_values) < no_colors:
        print('Color {}: Hue angle {}°'.format(counter, angle))
        red = interpolate_color(red_values, angle)
        green = interpolate_color(green_values, angle)
        blue = interpolate_color(blue_values, angle)
        rgb_values.append((red, green, blue))
        angles.append(angle)

        last_angle = angle
        while True:
            angle = last_angle + offset + 180
            if angle >= 360.:
                angle -= 360

            if angle in angles:
                offset = offset / 2
            else:
                counter += 1
                offset = 180.
                break

    return rgb_values, angles


def create_test_plot(rgb_values):
    """Creates a simple test plot"""

    x = np.linspace(-1, 1., 10)

    def y(x, m, b):
        return m * x + b

    for i, rgb_value in enumerate(rgb_values):
        plt.plot(x, y(x, i, 0), color=rgb_value, label='Color {}'.format(i))

    plt.legend()
    plt.show()


if __name__ == '__main__':

    S = 1.0     # saturation
    V = 0.8     # value
    no_colors = 16  # number of colors to create

    rgb_values, angles = calculate_colors(S, V, no_colors)

    print('\nrgba_values = (')
    for i, rgb_value in enumerate(rgb_values):
        print('    ({:4.3f}, {:4.3f}, {:4.3f}, 1.0),  # H={}°, S={}, V={}'.format(*rgb_value, angles[i], S, V))
    print(')')

    create_test_plot(rgb_values)
