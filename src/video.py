from moviepy import *
from utilities import *

# VARIABLES

scirpt_dir = Path(__file__).parent

output_folder = f"output/"
video_folder = f"media/video/"
sticker_folder = f"media/image/sticker/"
extracts_folder = f"media/audio/extracts/"

settings = f"json/settings.json"

with open(settings, "r") as file:
    SETTINGS = json.load(file)

def adjust_text_size(text,fontsize,intensity=10):
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

"""def daily_verse_short(reference, verse, background_video, title_translation, credits_translation):

    filename= title_translation + credits_translation + "-"+str(int(time.time()))+".mp4"
    title_text = title_translation
    credits_text = credits_translation
    
    print("GospelBot - Creating daily verse short video...")

    # Set the music
    random_music = random_file(AUDIO_FOLDER)
    music = AudioFileClip(random_music)

    print("GospelBot - Short music chosen : " + random_music)

    # Set the main clip
    clip = (
        VideoFileClip(background_video)
        .subclip(0,1)
        .cropped(x1=100, y1=100, x2=720, y2=1280)
        .with_duration(music.duration)
        .resized((1080,1920))
        .transform(lambda frame: apply_blur())
    )

    # Set the title
    text1 = (
        TextClip(
            title_text, 
            fontsize=LARGE, 
            color='yellow', 
            method="label", 
            stroke_width=3, 
            stroke_color='black', 
            font=BOLD
        )
        .with_duration(clip.duration)
        .with_position(('center', 50))
        .transform(lambda frame: apply_blur())
    )

    # Set the credits
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
        .with_duration(clip.duration)
        .with_position(('center', 1700))
        .with_opacity(0.5)
        .transform(lambda frame: apply_blur())
    )

    # Set the paper clip
    paper = (
        ImageClip("media/image/paper.png")
        .with_duration(clip.duration)
        .with_position(('center', 350))
        .resized((1200, 950))
    )

    # Set the biblical reference
    text2 = (
        TextClip(
            reference, 
            fontsize=MEDIUM, 
            color='cyan', 
            method="caption", 
            stroke_width=3, 
            stroke_color='black', 
            size=(1000, 200), 
            font=BOLD
        )
        .with_duration(clip.duration)
        .with_position(('center', 200))
        .transform(lambda frame: apply_blur())
    )

    # Set the verse
    text3 = (
        TextClip(
            verse, 
            fontsize=adjust_text_size(verse, SMALL), 
            color='white', 
            method="caption", 
            stroke_width=2, 
            stroke_color='black', 
            size=(900, 900), 
            font=ITALIC
        )
        .with_duration(clip.duration)
        .with_position(('center', 400))
        .transform(lambda frame: apply_blur())
    )

    # Set the jesus image

    image = ImageClip(random_file(STICKER_FOLDER)).resized(width=1080)
    image = move_with_easing(image, (0, 1920), (0, 1200), 2, music.duration, ease_out_quart)

    # Final video
    video = CompositeVideoClip(
        [
            clip.fadein(1).fadeout(2),
            text1.fadein(1).fadeout(2),
            paper.fadein(1).fadeout(2),
            text2.fadein(1).fadeout(2),
            text3.fadein(1).fadeout(2),
            image.fadein(1).fadeout(2),
            credits
        ]
    )
      
    video = video.with_audio(music)
    video.write_videofile(OUTPUT_FOLDER+filename, codec="libx264", preset='ultrafast', threads=4)
    video = OUTPUT_FOLDER+filename

    return video"""

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

def daily_verse_short(reference, verse): 

    filename= "Daily Verse-"+str(int(time.time()))+".mp4"
    
    print("GospelBot - Creating daily verse short video...")

    clips = []
    sounds = []
    
    subtitles = [
        {"text":"Do you have one minute for god ?", "position":("center", "center"), "delay":1, "color":"yellow"},
        {"text":"Great !", "position":("center", "center"), "delay":1, "color":"lime"},
        {"text":"Here the verse of the day !", "position":("center", "center"), "delay":0, "color":"white"},
        {"text":reference.replace(":", " "), "position":("center", "center"), "delay":0, "color":"cyan"},
        {"text":f'"{verse}"', "position":("center", "center"), "delay":0, "color":"white"},
        {"text":"Subscribe for more daily verse !", "position":("center", "center"), "delay":-0.3, "color":"red"},
        {"text":"And spread the gospel with me !", "position":("center", "center"), "delay":-0.3, "color":"yellow"},
        {"text":"By sharing to all of your friend.", "position":("center", "center"), "delay":0, "color":"yellow"},
        {"text":"God bless you !", "position":("center", "center"), "delay":0, "color":"cyan"}
        ]
    
    oldstart = 0
    voice = random.choice(SETTINGS["VOICES"])
    
    for key in subtitles:

        text = key["text"]
        position = key["position"]
        delay = key["delay"]
        color = key["color"]

        speech = asyncio.run(text_to_speech(text, voice))
        speech_clip = AudioFileClip(speech).with_start(oldstart)
        background_video = pixabay_video(video_folder, "landscape", speech_clip.duration + delay)

        clip = (
            VideoFileClip(background_video)
            .with_duration(speech_clip.duration + delay)
            .cropped(x1=100, y1=100, x2=720, y2=1280)
            .resized((1080,1920))
            .with_start(oldstart)
        )

        subtitle = (
            TextClip(text=text, color=color, font_size=SETTINGS["MEDIUM"], size=(1000, None), font=SETTINGS["ITALIC"], stroke_color="black", stroke_width=3, method="caption")
            .with_duration(speech_clip.duration + delay)
            .with_start(oldstart)
            .with_position(position)
        )

        size = list(subtitle.size)
        size[0] = 1080
        h = size[1]
        size = tuple(size)

        sticker = (
            ImageClip(random_file(sticker_folder))
            .with_duration(speech_clip.duration + delay)
            .with_start(oldstart)
            .resized(height=abs(960 - h))
            .with_position(('center', "bottom"))
        )

        background = (
            
            ColorClip(size=size, color=[0, 0, 0])
            .with_duration(speech_clip.duration + delay)
            .with_position(position)
            .with_start(oldstart)
            .with_opacity(.5)
        )


        clips.extend([clip, sticker, background, subtitle])
        sounds.append(speech_clip)

        oldstart += speech_clip.duration + delay


    # Set the music
    random_music = random_file(extracts_folder)
    music = AudioFileClip(random_music).with_volume_scaled(0.1)
    sounds.append(music)
    final_sound = CompositeAudioClip(sounds)

    print("GospelBot - Short music chosen : " + random_music)

    credits = (
        TextClip(
            text=SETTINGS["USERNAME"], 
            font_size=SETTINGS["MEDIUM"], 
            color='white', 
            method="label", 
            font=SETTINGS["BOLD"], 
            stroke_width=3, 
            stroke_color='black'
        )
        .with_duration(music.duration)
        .with_position(('center', 200))
        .with_opacity(0.5)
    )

    clips.append(credits)

    # Final video
    video = CompositeVideoClip(clips)
      
    video = video.with_audio(final_sound)
    video.write_videofile(output_folder+filename, codec="libx264", preset='ultrafast', threads=4, fps=24)
    video = output_folder+filename

    return video


