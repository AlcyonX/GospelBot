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

import os
import random

def do_until_success(func, *args, **kwargs):
    """
    Tries to execute a function until it succeeds.

    Arguments:
    func -- The function to execute.
    *args -- Positional arguments to pass to the function.
    **kwargs -- Keyword arguments to pass to the function.

    Prints an error message if an exception occurs and retries.
    """
    while True:
        try:
            func(*args, **kwargs)
            break
        except Exception as e:
            print(f"GospelBot - An error occured : {e}")

def random_file(folder):

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    if not files:
        raise "GospelBot - No files found in the folder."
    
    selected_file = random.choice(files)
    return folder + selected_file

def sample_files(folder, count):

    files = os.listdir(folder)

    selected_files = random.sample(files, min(count, len(files)))
    return [os.path.join(folder, file) for file in selected_files]

def divide_string(s, n):
    
    # Split the string into words
    words = s.split()

    # Calculate the length of each part
    part_length = len(words) // n
    remainder = len(words) % n

    # Initialize a list to store the parts
    parts = []
    start_index = 0

    # Create the parts, accounting for the remainder
    for i in range(n):
        end_index = start_index + part_length + (1 if i < remainder else 0)
        part = ' '.join(words[start_index:end_index])
        parts.append(part)
        start_index = end_index

    return parts
