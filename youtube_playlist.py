import httplib2
import os
import sys

from modules import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

YT_CLIENT_SECRET = "client_secrets.json"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   YT_CLIENT_SECRET))

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(YT_CLIENT_SECRET, message=MISSING_CLIENT_SECRETS_MESSAGE, scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=credentials.authorize(httplib2.Http()))

def hasPlaylist(title) -> bool:
    """checa se já existe uma playlist com o titulo informado

    Returns:
        str: retorna o id caso já exista uma playlist com o nome, ou uma string vazia caso contrário
    """
    playlist_id = ""
    playlists = youtube.playlists().list(
        part="snippet, id",
        mine=True,
        ).execute()
    for item in playlists["items"]:
        if item["snippet"]["title"] == title:
            playlist_id = item["id"]
    return playlist_id

def create_playlist(title="default title", description="default desc", status="public"):
    """cria uma playlist com os parâmetros informados

    Args:
        title (str, optional): titulo da playlist. Defaults to "default title".
        description (str, optional): descrição da playlist. Defaults to "default desc".
        status (str, optional): status da playlist, pode ser "public" ou "private". Defaults to "public".
    """
    playlists_insert_response = youtube.playlists().insert(
        part="snippet, status",
        body=dict(
            snippet=dict(
                title=title,
                description=description
            ),
            status=dict(
                privacyStatus=status
            )
        )
    ).execute()
    print("novo id: %s" % playlists_insert_response["id"])
    playlist_id = playlists_insert_response["id"]
    return playlist_id
    

def add_item_playlist(playlist_id, video_id):
    body = {
            "snippet": {
                "playlistId": str(playlist_id),
                "resourceId": {
                "videoId": str(video_id),
                "kind": "youtube#video"
                }
            }
            }
    print(f"video: {str(video_id)}")
    playlist_insert_item_response = youtube.playlistItems().insert(
        part="snippet",
        body=body
    ).execute()
    
    print("item adicionado a playlist: {ptitle}".format(ptitle=playlist_insert_item_response["snippet"]["title"]))