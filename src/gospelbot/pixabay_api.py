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

import requests
import os
import dotenv
import random
import time
import sys

from misc import print

dotenv.load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

def pixabay_video(path, q, min_duration=0):
    """
    Downloads a video from Pixabay based on a given query, with a specified minimum duration.
    
    :param path: Path to save the video.
    :param q: Search theme/query.
    :param min_duration: Minimum duration in seconds for videos. Defaults to 0 (no limit).
    :return: Full path of the downloaded video file.
    """
    BASE_URL = 'https://pixabay.com/api/videos/'
    
    params = {
        'key': PIXABAY_API_KEY,
        'q': q,  # Search theme
        'per_page': 50  # Number of results
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:

        data = response.json()
        videos = data['hits']
        
        # Filter videos based on the minimum duration
        filtered_videos = [video for video in videos if video['duration'] >= min_duration]
        
        if filtered_videos:

            # Select a random video
            random_video = random.choice(filtered_videos)
            video_url = random_video['videos']['medium']['url']

            print(f"GospelBot - Downloading the video: {video_url}.")
            
            # Download the video
            video_response = requests.get(video_url)

            if video_response.status_code == 200:

                filename = f"{q}-{int(time.time())}.mp4"
                file = path + filename
                
                with open(file, 'wb') as f:

                    f.write(video_response.content)
                
                print(f"GospelBot - Video successfully downloaded: {filename}.")

                return file

            else:

                raise ValueError(f"GospelBot - An error occurred while downloading the video: {video_response.status_code}.")
        else:

            raise ValueError("GospelBot - No videos found matching the minimum duration requirement.")
    else:

        raise ValueError(f"GospelBot - An error occurred {response.status_code}: {response.text}.")