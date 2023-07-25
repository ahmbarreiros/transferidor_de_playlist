from modules import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from dotenv import load_dotenv

import json
import urllib

DEVELOPER_KEY = os.getenv("YT_API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
def youtube_search(search):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    search_response = youtube.search().list(
        q=search,
        part="id, snippet",
        maxResults=1,
        type="video"
    ).execute()
    
    videos = []
    
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("{id}".format(id=search_result["id"]["videoId"]))
    return videos[0]
    
def send_search(query):
    try:
        id =youtube_search(query)
        return id
    except HttpError as e:
        print(f"Erro de http codigo: {e.resp.status}:\n {e.content}")