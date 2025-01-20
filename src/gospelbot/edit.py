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

import random
import json
import time

from misc import *
from bible_api import *
from settings import *
from moviepy import *
import moviepy.video.fx as vfx
from video import *


def generate_edit_short(title: str, references: list,  transition_duration=0.5):

    filename = f"edit-{int(time.time())}.mp4"
    width, height = 1080, 1920

    print("GospelBot - Creating edit short video...")

    # Set the music
    random_music = random_file(settings["edit_musics_folder"])
    music = AudioFileClip(random_music)

    print("GospelBot - Music chosen : " + random_music)

    clip_duration = music.duration / (len(references) + 2)
    intro_duration = clip_duration * 2

    print("GospelBot - Clip duration : " + str(clip_duration))

    # Set the video size
    base = (
        ColorClip(
            size=(width, height), 
            color=(0, 0, 0)
        )
        .with_duration(clip_duration)
    )
    
    # Create Vignette mask
    vignette_path = f"{settings['images_folder']}vignette.png"
    vignette = (
        ImageClip(vignette_path)
        .resized((width, height))
        .with_duration(intro_duration)
    )
    # Set the intro
    intro = (
        ImageClip(random_file(settings["edit_introductions_folder"]))
        .resized(height=height*1.75)
        .with_position(idle_movement)
        .rotated(idle_rotation_movement)
        .with_duration(intro_duration)
        .with_effects([vfx.FadeIn(transition_duration), vfx.FadeOut(transition_duration)])
    )

    clips = [base, intro, vignette]
    old_clips = []

    titles = divide_string(title, 3)
    print(titles)

    # Set the titles
    for index, key in enumerate(titles):

        content = key
        text_font = settings["title_font_family"]
        text_color = 'red'
        position = 800
        
        for _, k in enumerate(old_clips):
            position += k.h

        if index == 0:

            text_font = settings["subtitle_font_family"]
            text_color = 'red'
            content = str.upper(content)

        elif index == 1:

            text_font = settings["paragraph_font_family"]
            text_color = 'white'
            content = str.lower(content)
        else:

            text_font = settings["subtitle_font_family"]
            text_color = 'cyan'
            content = str.upper(content)

        text = (
            TextClip(
                text=content, 
                font_size=settings["medium_font_size"], 
                color=text_color, 
                method="caption",  
                font=text_font,
                stroke_width=3,
                stroke_color="black",
                size=(1000, None)
            )
            .with_duration(intro_duration)
            .with_position(('center', position))
            .with_effects([vfx.FadeIn(transition_duration), vfx.FadeOut(transition_duration)])
            .transform(blur_frame)
        )

        clips.extend([text])
        old_clips.append(text)

    # Choose random images
    random_images = sample_files(settings["edit_backgrounds_folder"], len(references))

    # Set the clips
    for index, key in enumerate(references) :

        print("GospelBot - Clip " + str(index) + " - Text chosen : " + key)
        print("GospelBot - Clip " + str(index) + " - Biblical reference : " + references[key])

        # Set the start
        start = index * clip_duration + intro_duration

        # Set the image
        clip = (
            ImageClip(random_images[index])
            .resized(height=height * 1.75)
            .with_position(idle_movement)
            .rotated(idle_rotation_movement)
            .with_start(start)
            .with_duration(clip_duration)
            .with_effects([vfx.FadeIn(transition_duration), vfx.FadeOut(transition_duration)])
        )

        # Create the Vignette mask
        vignette = (
            ImageClip(vignette_path)
            .resized((width, height))
            .with_start(start)
            .with_duration(clip_duration)
        )
        
        # Set the text
        text = (
            TextClip(
                text=key, 
                font_size=settings["medium_font_size"], 
                color="white", 
                method="caption", 
                stroke_width=3, 
                stroke_color='black', 
                font=settings["paragraph_font_family"],
                size=(1000, None)
            )
            .with_duration(clip.duration).with_start(start)
            .with_position(('center', 800))
            .with_effects([vfx.FadeIn(transition_duration), vfx.FadeOut(transition_duration)])
            .transform(blur_frame)
        )

        # Set the reference
        reference = (
            TextClip(
                text=references[key], 
                font_size=settings["medium_font_size"], 
                color="cyan", 
                method="label", 
                stroke_width=3, 
                stroke_color="black", 
                font=settings["subtitle_font_family"]
            )
            .with_duration(clip.duration)
            .transform(blur_frame)
            .with_start(start)
            .with_position(('center', 800 + text.h))
            .with_effects([vfx.FadeIn(transition_duration), vfx.FadeOut(transition_duration)])
        )
        
        # Add to clips 
        clips.extend([clip, vignette, text, reference])

    # Set credits
    credits = (
        TextClip(
            text=settings["username"], 
            font_size=settings["medium_font_size"], 
            color="white", 
            method="label", 
            font=settings["subtitle_font_family"], 
            stroke_width=3, 
            stroke_color="black"
        )
        .with_duration(music.duration)
        .with_position(('center', 1500))
        .with_opacity(0.5)
        .transform(blur_frame)
    )

    clips.append(credits)
    video_path = f"{settings['output_folder']}{filename}"

    # Final video
    video = CompositeVideoClip(clips)
    video = video.with_audio(music)

    os.makedirs(settings["output_folder"], exist_ok=True)

    video.write_videofile(video_path, fps=24, preset='ultrafast', threads=4, codec="libx264")

    return video_path

def edit_short(is_publishing: bool) -> str :

    print("GospelBot - Creating and publishing a edit short video started...")

    random_reference = random.choice(
        json.load(
            open(
                get_first_file(settings["verses_folder"]),
                "r"
            )
        )
    )

    title, references = get_random_edit_content(5, get_first_file(settings["edit_content_folder"]), settings["bible_id"])

    video = generate_edit_short(title, references)

    hashtags = random.sample(settings["hashtags"], 4)

    title = f"{settings['edit_video_title']} {time.strftime('%d/%m/%Y')} {' '.join(hashtags)}"
    description = f"Amen !"

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
            "public",
            key
        )

    print("GospelBot - Success !")

    return video

if __name__ == "__main__":
    edit_short(False)