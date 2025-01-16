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

def edit_short(title, references, credits_translation,  transition_duration=0.5):

    filename = title + "-" + credits_translation + "-" + str(int(time.time())) + ".mp4"
    credits_text = credits_translation

    print("GospelBot - Creating edit short video...")

    # Set the music
    random_music = random_file(AUDIO_FOLDER + "edit/")
    music = AudioFileClip(random_music)

    print("GospelBot - Music chosen : " + random_music)

    clip_duration = music.duration / (len(references) + 2)
    intro_duration = clip_duration * 2

    print("GospelBot - Clip duration : " + str(clip_duration))

    # Set the video size
    base = (
        ColorClip(
            size=(1080, 1920), 
            color=(0, 0, 0)
        )
        .with_duration(clip_duration)
    )
    
    # Create Vignette mask
    vignette = (
        ImageClip(IMAGE_FOLDER + "vignette.png")
        .resized((1080, 1920))
        .with_duration(intro_duration)
    )
    # Set the intro
    intro = (
        ImageClip(random_file("media/image/intro/"))
        .resized(height=3000)
        .with_position(idle_movement)
        .rotate(idle_rotation_movement)
        .with_duration(clip_duration*2)
        .fadein(transition_duration)
        .fadeout(transition_duration)
    )

    clips = [base, intro, vignette]
    old_clips = []

    titles = divide_string(title, 3)
    print(titles)

    # Set the titles
    for index, key in enumerate(titles):

        content = key
        text_font = FONT
        text_color = 'red'
        position = 800
        
        for _, k in enumerate(old_clips):
            position += k.h

        if index == 0:
            text_font = BOLD
            text_color = 'red'
            content = str.upper(content)
        elif index == 1:
            text_font = ITALIC
            text_color = 'white'
            content = str.lower(content)
        else:
            text_font = BOLD
            text_color = 'cyan'
            content = str.upper(content)

        text = (
            TextClip(
                content, 
                fontsize=MEDIUM, 
                color=text_color, 
                method="caption",  
                font=text_font,
                stroke_width=3,
                stroke_color='black',
                size=(1000, None)
            )
            .with_duration(intro_duration)
            .with_position(('center', position))

            .fadein(transition_duration)
            .fadeout(transition_duration)
        )

        clips.extend([text])
        old_clips.append(text)

    # Choose random images
    random_images = unique_random_files("media/image/background/", len(references))

    # Set the clips
    for index, key in enumerate(references) :

        print("GospelBot - Clip " + str(index) + " - Text chosen : " + key)
        print("GospelBot - Clip " + str(index) + " - Biblical reference : " + references[key])

        # Set the start
        start = index * clip_duration + intro_duration

        # Set the image
        clip = (
            ImageClip(random_images[index])
            .resized(height=3000)
            .with_position(idle_movement)
            .rotate(idle_rotation_movement)
            .with_start(start)
            .with_duration(clip_duration)
            .fadein(transition_duration)
            .fadeout(transition_duration)
        )

        # Create the Vignette mask
        vignette = (
            ImageClip(IMAGE_FOLDER + "vignette.png")
            .resized((1080, 1920))
            .with_start(start)
            .with_duration(clip_duration)
        )
        
        # Set the text
        text = (
            TextClip(
                key, 
                fontsize=MEDIUM, 
                color='white', 
                method="caption", 
                stroke_width=3, 
                stroke_color='black', 
                font=ITALIC,
                size=(1000, None)
            )
            .with_duration(clip.duration).with_start(start)
            .with_position(('center', 800))

            .fadein(transition_duration)
            .fadeout(transition_duration)
        )

        # Set the reference
        reference = (
            TextClip(
                references[key], 
                fontsize=MEDIUM, 
                color='cyan', 
                method="label", 
                stroke_width=3, 
                stroke_color='black', 
                font=BOLD
            )
            .with_duration(clip.duration)

            .with_start(start)
            .with_position(('center', 800 + text.h))
            .fadein(transition_duration)
            .fadeout(transition_duration)
        )
        
        # Add to clips 
        clips.extend([clip, vignette, text, reference])

    # Set credits
    credits = (
        TextClip(
            credits_text, 
            fontsize=MEDIUM, 
            color='white', 
            method="label", 
            font=BOLD, 
            stroke_width=3, 
            stroke_color='black'
        )
        .with_duration(music.duration)
        .with_position(('center', 1500))
        .with_opacity(0.5)
        .transform(lambda frame: apply_blur())
    )

    clips.append(credits)

    # Final video
    video = CompositeVideoClip(clips)
    video = video.with_audio(music)
    video.write_videofile(OUTPUT_FOLDER+filename, fps=24, preset='ultrafast', threads=4, codec="libx264")
    video = OUTPUT_FOLDER+filename

    return video

def publish_edit_short(test):

    for _, key in enumerate(LANGUAGES):

        success = False

        while not success:

            try:
                print("GospelBot - Creating and publishing an edit short video..")

                print("GospelBot - Language : {key}")

                title, references = random_edit_content(5, LANGUAGES[key], BIBLES_ID[key])

                print("GospelBot - Title : {title}")

                video = edit_short(title, references, CREDITS_TRANSLATION[key])

                if not test:

                    random_title = random.choice(EDIT_TITLES)

                    title = f"{random_title} #god #holyspirit #jesus #faith #jesuschrist"

                    print("GospelBot - Publishing...")

                    video_id = publish(
                        video,
                        title,
                        "Amen ! ✝️",
                        KEYWORDS,
                        22,
                        "public",
                        key
                    )

                    try:
                        post_comment(video_id, random.choice(COMMENTS), LANGUAGES[key])
                    except Exception as e:
                        print("GospelBot - An small error occurred : " + str(ValueError(e)))
                    
                    success = True

                else:
                    success = True

                print("GospelBot - Success !")

            except Exception as e:
                print("GospelBot - An error occurred : " + str(ValueError(e)))

