# Author: AlcyonX
#
# Author YouTube channel link: https://www.youtube.com/@AlcyonX
# Official GospelBot YouTube channel : https://www.youtube.com/@GospelBot
#
# Copyright (c) 2025 AlcyonX. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# PRAISE THE LORD JESUS CHIRST ✝

import math
import cv2
import numpy as np

def blur_frame(get_frame, t):
    """
    This function returns the current frame with a blur effect applied.
    """
    frame = get_frame(t)
    
    # Apply Gaussian blur to the entire frame
    blur_kernel_size = (15, 15)
    blurred_frame = cv2.GaussianBlur(frame, blur_kernel_size, 0)
    
    return blurred_frame

def adjust_text_size(text,fontsize,intensity=10) -> float:
    font_size = fontsize - len(text) / intensity
    return font_size

def idle_movement(t):
    return 'center', math.sin(t*2)*50 - 500

def idle_rotation_movement(t):
    return math.sin(t*2)*2

def ease_out_quad(t, start, end, duration):
    t /= duration
    return start + (end - start) * (1 - (1 - t) ** 2)

def ease_out_quart(t, start, end, duration):
    t /= duration
    return start + (end - start) * (1 - (1 - t) ** 4)

def move_with_easing(clip, start_pos, end_pos, move_duration, total_duration, easing_func):

    animated_clip = clip.with_position(lambda t: (
        (end_pos if t >= move_duration else (
            easing_func(t, start_pos[0], end_pos[0], move_duration),
            easing_func(t, start_pos[1], end_pos[1], move_duration)
        ))
    ))
    
    return animated_clip.with_duration(total_duration)

