import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

from src.constants import CLIENT_SECRETS_FILE

# Define the API service name and version
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def authenticate_youtube():
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/youtube.upload']
    )
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, video_path, title, description, tags, scheduled_time):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22',  # Category ID for "People & Blogs"
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': scheduled_time.isoformat() + 'Z',
            'selfDeclaredMadeForKids': False,
        }
    }

    # Call the YouTube Data API's videos.insert method to upload the video
    media = googleapiclient.http.MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    response = request.execute()

    return response

def schedule_videos(video_list):
    youtube = authenticate_youtube()
    for video in video_list:
        video_path = video['video_path']
        title = video['description']
        description = video['description']
        tags = video['tags']
        scheduled_time = video['scheduled_time']

        response = upload_video(youtube, video_path, title, description, tags, scheduled_time)
        print(f"Uploaded video {title}: {response}")
