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

import googleapiclient.errors
import google.auth.transport.requests
import google_auth_oauthlib.flow
import requests
import os
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from misc import print, get_first_file
from settings import *

def publish(video_file, title, description, tags, category_id="22", privacy_status="public", language="EN") -> str:
    # Settings
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    
    # Get file paths for client secrets and token
    client_secrets_file = get_first_file(settings["client_id_folder"])
    token_file = get_first_file(settings["token_folder"])

    # If token file exists, load credentials
    credentials = None
    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file, scopes)

    # Refresh or get new credentials if not valid
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(google.auth.transport.requests.Request())
        except google.auth.exceptions.RefreshError as e:
            print(f"GospelBot - Error refreshing token: {e}")
            # Prompt the user to reauthenticate
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)
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
            "categoryId": category_id,
            "defaultLanguage": language  # Adding language setting
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    # Upload the video
    try:
        # Make sure the video file exists before attempting to upload
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"GospelBot - The video file {video_file} does not exist.")
        
        # Create the upload request
        media = MediaFileUpload(video_file, resumable=True, mimetype="video/*")
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )
        
        # Execute the upload
        response = request.execute()
        print(f"GospelBot - Video published with success: https://www.youtube.com/watch?v={response['id']}")
        return response["id"]
    
    except googleapiclient.errors.HttpError as e:
        print(f"GospelBot - HTTP Error: {e.status_code} - {e.error_details}")
        raise
    except FileNotFoundError as e:
        print(f"GospelBot - File error: {e}")
        raise
    except Exception as e:
        print(f"GospelBot - An unexpected error occurred: {e}")
        raise

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