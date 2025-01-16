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
import dotenv
import argparse

dotenv.load_dotenv()

settings_file = "json/settings.json"

with open(settings_file, "r") as file:
    settings = json.load(file)

def main():
    parser = argparse.ArgumentParser(description="Spread the Gospel")
    
    parser.add_argument("--type", type=str, choices=["edit", "dailyverse"], help="Set the type of video")
    parser.add_argument("--test", type=bool, choices=[True, False], default=False, help="If True the video will not be publish")


    args = parser.parse_args()

    if args.type == "edit":
        print("edit")
    elif args.type == "dailyverse":
        do_until_success(publish_daily_verse_short, args.test)
        


if __name__ == "__main__":
    main()


