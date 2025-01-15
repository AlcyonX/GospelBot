from dotenv import load_dotenv
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
from google.auth.transport.requests import Request
import googleapiclient.errors
from pathlib import Path
import time
import random
import requests
import json
import cv2
import os
import asyncio
import edge_tts
import re
import math

load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

verses = "json/data/verses.json"

with open(verses, "r") as file:
    verses = json.load(file)

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
            #print(f"GospelBot - An error occured : {e}")
            raise e

def random_file(folder):

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    if not files:
        raise "GospelBot - No files found in the folder."
    
    selected_file = random.choice(files)
    return folder + selected_file

def unique_random_files(folder, count):

    files = os.listdir(folder)
    selected_files = random.sample(files, min(count, len(files)))
    return [os.path.join(folder, file) for file in selected_files]


def get_book(bible_id, book_id):

    url = f"https://bible.helloao.org/api/{bible_id}/books.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        books = response.json().get("books", [])

        dicts = {}
        
        for book in books:
            dicts[book['id']] = book['name']

        return dicts[book_id]
    
    except requests.exceptions.RequestException as e:
        raise ValueError(e)


def get_random_verse(bible_id, verses=verses):

    reference = random.choice(verses).split()
    book_id = reference[0]
    chapter = reference[1]
    verse = int(reference[2])
    
    book = get_book(bible_id, book_id)

    url = f"https://bible.helloao.org/api/{bible_id}/{book.replace(' ', '_')}/{chapter}.json"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    for item in data['chapter']['content']:
        if item['type'] == 'verse':
            if item['number'] == verse:
                verse_text = item['content'][0]
                if type(verse_text) == dict:
                    verse_text = verse_text[0]
                return f"{book} {chapter}:{verse}", verse_text

def get_verse(bible_id, reference):

    reference = reference.split()
    book_id = reference[0]
    chapter = reference[1]
    verse = int(reference[2])
    
    book = get_book(bible_id, book_id)

    url = f"https://bible.helloao.org/api/{bible_id}/{book.replace(' ', '_')}/{chapter}.json"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    for item in data['chapter']['content']:
        if item['type'] == 'verse':
            if item['number'] == verse:
                verse_text = item['content'][0]
                if type(verse_text) == dict:
                    verse_text = verse_text["text"]
                return f"{book} {chapter}:{verse}", verse_text

def apply_blur(frame, size=21):

    size = max(1, (size // 2) * 2 + 1)
    
    blurred_frame = cv2.GaussianBlur(frame, (size, size), 0)
    return blurred_frame

def chat(content):

    client = InferenceClient(api_key=HUGGING_FACE_API_KEY)

    messages = [
        { "role": "user", "content": content }
    ]

    seed = random.randint(1,100000)

    stream = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct", 
        messages=messages, 
        max_tokens=500,
        stream=False,
        seed=seed,
        temperature=1
    )
    return stream["choices"][0]["message"]["content"]

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
                filename = q + "-" + str(int(time.time())) + ".mp4"
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

def publish(video_file, title, description, tags, category_id="22", privacy_status="public", language="EN"):

    # Settings
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    client_secrets_file = "json/api/id_"+ language + ".json"
    token_file = "json/api/token_" + language + ".json"

    # Change JSON
    credentials = None
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, scopes)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)

        # Save the token
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    # Create the YouTube Client
    youtube = build("youtube", "v3", credentials=credentials)

    # Define the metadata of the video
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    # Upload
    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=MediaFileUpload(video_file, resumable=True)
        )
        response = request.execute()
        print(f"GospelBot - Short published with success : https://www.youtube.com/shorts/{response['id']}")
        return response["id"]
    
    except googleapiclient.errors.HttpError as e:
        print(f"HTTP Error: {e.status_code} - {e.error_details}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def random_edit_content(num_entries, language, bible_id):

    with open(edit_content) as file:
        refs_list = json.load(file)
        
    title, refs_list = random.choice(list(refs_list.items()))
    title = translate(title, language)
    selected_refs = random.sample(refs_list, min(num_entries, len(refs_list)))
    
    refs_dict = {translate(entry['text'], language): get_verse(bible_id, entry['reference'])[0] for entry in selected_refs}
    
    return title, refs_dict


def post_comment(video_id, comment_text, language="EN"):

    if not comment_text.strip():
        raise ValueError("GospelBot - Comment text is empty or invalid.")

    # YouTube API setup
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    client_secrets_file = f"json/api/id_{language}.json"
    token_file = f"json/api/token_{language}.json"

    # Credentials loading
    credentials = None
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, scopes)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except google.auth.exceptions.RefreshError:
                print("GospelBot - Token refresh failed. Re-authenticating.")
                credentials = None
        if not credentials:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)

        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    # Create the YouTube client
    youtube = build("youtube", "v3", credentials=credentials)

    # Define the simplest comment snippet (only necessary fields)
    comment_body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": comment_text
                }
            }
        }
    }

    try:
        # Attempt to post the comment
        request = youtube.commentThreads().insert(
            part="snippet",
            body=comment_body
        )
        response = request.execute()
        print(f"GospelBot - Comment posted successfully: {response['id']}")
        return response['id']
    except Exception as e:
        raise ValueError(e)


async def text_to_speech(text: str, voice: str) -> str:

    output_file = f"{os.path.dirname(__file__)}/media/audio/speech/{voice}-{str(time.time())}.mp3"

    communicate = edge_tts.Communicate(text, voice, rate="+20%", pitch="+20Hz", volume="+10%")
    open(output_file, "x").close()
    await communicate.save(output_file)

    return output_file

async def random_voice(gender: str, language: str) -> str:
    
    voices = await edge_tts.VoicesManager.create()
    voice = voices.find(Gender="Male", Language=language)
    voice = voice[0]["Name"]

    return voice


