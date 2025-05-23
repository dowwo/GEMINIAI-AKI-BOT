import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


# Para installar youtube-dl pip install https://github.com/ytdl-org/ytdl-nightly/releases/download/2024.08.07/youtube-dl-2024.08.07.tar.gz


# API KEYS
load_dotenv()

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

youtube = build('youtube','v3', developerKey=YOUTUBE_API_KEY)


def search(query):
    # part se declara que meta-data se quiere obtener del video
    # q es la query de busqueda
    # maxResults es cuantos resultados queremos en la busqueda
    # type el tipo de contenido que queremos que retorne (playlist, channel, video)
    # En esta caso los que debe entregar es el id y el titulo
    
    request = youtube.search().list(
        part='id,snippet',
        q=query,
        maxResults=5,
        type='video'
    )
    
    response = request.execute()

    search_results = []
    
    for video in response['items']:
        title = video["snippet"]["title"]
        video_id = video["id"]["videoId"]
        item = {
            'name': title,
            'value': f'https://www.youtube.com/watch?v={video_id}',
        }
        print(video_id)
        search_results.append(item)
    
    return search_results

