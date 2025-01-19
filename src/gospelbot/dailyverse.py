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

import json
import time
import random
import asyncio
import cv2
import os
import sys

from video import *    
from settings import *
from bible_api import *
from edge_tts_api import *
from pixabay_api import *
from youtube_api import *
from misc import *
from moviepy import *

def generate_daily_verse_short(reference: str, verse: str) -> str: 

    filename = f"daily_verse-{int(time.time())}.mp4"
    
    print("GospelBot - Creating daily verse short video...")

    clips = []
    sounds = []
    
    subtitles = [
        {"text":"Do you have one minute for god ?", "position":("center", "center"), "delay":1, "color":"yellow"},
        {"text":"Great !", "position":("center", "center"), "delay":1, "color":"lime"},
        {"text":"Here the verse of the day !", "position":("center", "center"), "delay":0, "color":"white"},
        {"text":reference.replace(":", " "), "position":("center", "center"), "delay":0, "color":"cyan"},
        {"text":f'"{verse}"', "position":("center", "center"), "delay":0, "color":"white"},
        {"text":"Subscribe for more daily verse !", "position":("center", "center"), "delay":-0.2, "color":"red"},
        {"text":"And spread the gospel with me !", "position":("center", "center"), "delay":-0.2, "color":"yellow"},
        {"text":"By sharing to all of your friend.", "position":("center", "center"), "delay":0, "color":"yellow"},
        {"text":"God bless you !", "position":("center", "center"), "delay":0, "color":"cyan"}
    ]
    
    old_start = 0
    voice = random.choice(settings["voices"])

    for item in subtitles:

        text = item["text"]
        position = item["position"]
        delay = item["delay"]
        color = item["color"]

        speech = asyncio.run(text_to_speech(text, voice, settings["downloads_folder"]))
        speech_clip = AudioFileClip(speech).with_start(old_start)
        background_video = "downloads/landscape-1737142300.mp4" #pixabay_video(settings["downloads_folder"], "landscape", speech_clip.duration + delay)

        # Set the background video
        clip = (
            VideoFileClip(background_video)
            .with_duration(speech_clip.duration + delay)
            .cropped(x1=100, y1=100, x2=720, y2=1280)
            .resized((1080,1920))
            .with_start(old_start)
            .transform(blur_frame)
        )

        # Set the subtitle
        subtitle = (
            TextClip(
                text=text,
                color=color, 
                font_size=settings["medium_font_size"], 
                size=(1000, None), 
                font=settings["paragraph_font_family"], 
                stroke_color="black", 
                stroke_width=3, 
                method="caption"
            )
            .with_duration(speech_clip.duration + delay)
            .with_start(old_start)
            .with_position(position)
            .transform(blur_frame)
        )

        h = subtitle.size[1]
        size = (1080, h)

        sticker_image = random_file(settings["sticker_folder"])

        sticker = (
            ImageClip(sticker_image)
            .with_duration(speech_clip.duration + delay)
            .with_start(old_start)
            .resized(height=abs(960 - h))
            .with_position(('center', "bottom"))
        )

        background = (
            ColorClip(size=size, color=[0, 0, 0])
            .with_duration(speech_clip.duration + delay)
            .with_position(position)
            .with_start(old_start)
            .with_opacity(.5)
        )


        clips.extend([clip, sticker, background, subtitle])
        sounds.append(speech_clip)

        old_start += speech_clip.duration + delay


    # Set the music
    random_music = random_file(settings["extracts_folder"])
    music = AudioFileClip(random_music).with_volume_scaled(0.1)
    sounds.append(music)
    final_sound = CompositeAudioClip(sounds)

    print("GospelBot - Music extract chosen : " + random_music)

    # Set the credits
    credits = (
        TextClip(
            text=settings["username"], 
            font_size=settings["medium_font_size"], 
            color='white', 
            method="label", 
            font=settings["title_font_family"], 
            stroke_width=3, 
            stroke_color='black'
        )
        .with_duration(music.duration)
        .with_position(('center', 200))
        .with_opacity(0.5)
        .transform(blur_frame)
    )

    clips.append(credits)

    # Final video

    print(f"GospelBot - Writing video file : {filename}")

    video_path = f"{settings["output_folder"]}{filename}"

    video = CompositeVideoClip(clips)
      
    video = video.with_audio(final_sound)

    os.makedirs(settings["output_folder"], exist_ok=True)
    
    video.write_videofile(video_path, codec="libx264", preset='ultrafast', fps=24, logger=None)

    return video_path

def daily_verse_short(is_publishing: bool) -> str :

    print("GospelBot - Creating and publishing a daily verse short video started...")

    random_reference = random.choice(
        json.load(
            open(
                get_first_file(settings["verses_folder"]),
                "r"
            )
        )
    )

    reference, verse = get_verse(settings["bible_id"], random_reference)

    print("GospelBot - Bibical reference chosen : " + reference)
    print("GospelBot - Bibical verse chosen : " + verse)

    video = generate_daily_verse_short(reference, verse)

    hashtags = random.sample(settings["hashtags"], 4)

    title = f"✝️ Daily verse 💝 {time.strftime("%d/%m/%Y")} {" ".join(hashtags)}"
    description = f"{reference}-{verse}"

    print("GospelBot - Title : " + title)
    print("GospelBot - Description : " + description)

    if is_publishing:

        print("GospelBot - Publishing...")

        video_id = publish(
            video,
            title,
            description,
            settings["keywords"],
            22,
            "public"
        )

    print("GospelBot - Success !")

    return video

if __name__ == "__main__":

    daily_verse_short(True)