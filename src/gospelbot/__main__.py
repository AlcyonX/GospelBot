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

from dailyverse import *
from edit import *
from settings import *
import dotenv
import argparse

def main() -> None:

    for folder in settings["folders"]:
        os.makedirs(settings[folder], exist_ok=True)

    parser = argparse.ArgumentParser(description="A program that spreads the gospel on social media.")
    
    parser.add_argument("--type", type=str, choices=["edit", "dailyverse"], help="Set the type of video")
    parser.add_argument("--publish", type=bool, choices=[True, False], default=True, help="If False the video will not be publish")

    if len(sys.argv) == 1:

        parser.parse_args(["--help"])
    else:

        args = parser.parse_args()

        if args.type == "edit":

            do_until_success(edit_short, args.publish)

        elif args.type == "dailyverse":

            do_until_success(daily_verse_short, args.publish)

if __name__ == "__main__":
    main()


