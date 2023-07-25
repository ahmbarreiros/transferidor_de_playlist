from modules import *
from search_spotify import *
from youtube_playlist import *
from auth import *
from search_youtube import *

def criar_playlist_youtube(title, desc):
    playlist_id = hasPlaylist(title)
    if not playlist_id:
        playlist_id = create_playlist(title, desc)
        print(f"id: {playlist_id}")
    else:
        print("Playlist com o nome já existe")
        print(f"id: {playlist_id}")
    return playlist_id

if __name__ == "__main__":
    token = get_token()
    search = get_search(token)
    if search["type"] == "playlist":
        playlist_name = search["name"]
        playlist_desc = search["description"]
        yt_pl = input("Deseja criar playlist no youtube? (S/N): ").upper().strip()
        if yt_pl == "S": 
            playlist_id = criar_playlist_youtube(playlist_name, playlist_desc)
            musicas = get_playlist_track_names(token, search)
            cont = 1
            offset = int(input("A partir de qual posicao: "))
            for i in range(offset - 1, len(musicas)):
                musica = musicas[i]
                if cont <= 20:
                    musica_id = send_search(musica)
                    print(musica_id)
                    add_item_playlist(playlist_id, musica_id)
                cont += 1
            print("terminado na posicao " + cont)

