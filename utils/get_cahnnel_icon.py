from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

def get_channel_icon_url(channel_id):
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    request = youtube.channels().list(part='snippet', id=channel_id)
    response = request.execute()
    
    if response['items']:
        channel_info = response['items'][0]
        icon_url = channel_info['snippet']['thumbnails']['default']['url']
        return icon_url
    else:
        return None
