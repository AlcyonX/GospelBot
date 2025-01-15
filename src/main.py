from video import *
from utilities import * 
import argparse

load_dotenv()

__version__ = "1.0.0"

client_id = "json/api/.client_id.json"
token = "json/api/token.json"

edit_content = "json/data/edit_content"
verses = "json/data/edit_content"

settings_file = "json/settings.json"

with open(settings_file, "r") as file:
    settings = json.load(file)

def publish_daily_verse_short(publish):

    print("GospelBot - Creating and publishing a daily verse short video started...")

    reference, verse = get_random_verse(settings["bible_id"])

    print("GospelBot - Bibical reference chosen : " + reference)
    print("GospelBot - Bibical verse chosen : " + verse)

    video = generate_daily_verse_short(reference, verse)

    title = f"✝️ Daily verse 💝 {time.strftime("%D/%M/%Y")} {random.sample(settings["hashtags"], 4)}"
    description = f"{reference}-{verse}"

    print("GospelBot - Description : " + description)
    print("GospelBot - Title : " + title)

    if publish:

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


