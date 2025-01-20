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
import time
import logging

from logging.handlers import RotatingFileHandler
from settings import *

# Logs
os.makedirs(settings["logs_folder"], exist_ok=True)
handler = RotatingFileHandler(f"{settings['logs_folder']}.log", maxBytes=50000, backupCount=10)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[handler]
) 

# ANSI for text customization
RED = '\033[31m'
YELLOW = '\033[33m'
RESET = '\033[0m'
BOLD = '\033[1m'
CYAN = '\033[36m'

timeout = 2

def do_until_success(func, *args, **kwargs) -> None:
    """
    Tries to execute a function until it succeeds.

    Arguments:
    func -- The function to execute.
    *args -- Positional arguments to pass to the function.
    **kwargs -- Keyword arguments to pass to the function.

    Prints an error message if an exception occurs and retries.
    """
    global timeout
    while True:
        try:
            func(*args, **kwargs)
            timeout = 2
            break
        except Exception as e:
            minutes, seconds = divmod(timeout, 60)
            print(f"GospelBot - {RED} An error occured : {e} {RESET}")
            print(f"GospelBot - {CYAN} Retry in {minutes} minutes and {seconds} seconds {RESET}")
            time.sleep(timeout)
            timeout *= 2

def random_file(folder: str) -> str:

    # Get a list of files in the specified folder (only files, not directories)
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    # Check if there are no files in the folder, raise an error with a message
    if not files:
        raise Exception("GospelBot - No files found in the folder.")
    
    # Randomly choose a file from the list of files
    selected_file = random.choice(files)
    
    # Return the full path to the randomly selected file by combining the folder and file name
    return os.path.join(folder, selected_file)

def sample_files(folder: str, count: int) -> list:
    
    # Get a list of all files and directories in the specified folder
    files = os.listdir(folder)

    # Randomly select the 'count' number of files from the folder, ensuring it doesn't exceed the available files
    selected_files = random.sample(files, min(count, len(files)))
    
    # Return a list of full file paths by combining the folder and each selected file
    return [os.path.join(folder, file) for file in selected_files]

def divide_string(s: str, n: int) -> list:
    
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

def get_first_file(directory: str) -> str:

    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Return the first file if any exists, otherwise return None
    if files:
        return f"{directory}{files[0]}"
    else:
        raise "GospelBot - No files found in the folder."


# Custom print
original_print = print

def custom_print(*args, **kwargs):

    new_args = []
    for arg in args:

        new_args.append(str(arg).replace("GospelBot - ", f"{BOLD}{YELLOW}GospelBot - {RESET}"))
    
    original_print(*new_args, **kwargs)
    logging.info(*new_args, **kwargs)

print = custom_print