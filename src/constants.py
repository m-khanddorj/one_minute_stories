import os

AUDIO_FPS = 22050

OUTPUT_PATH = "outputs"
STORY_PATH = os.path.join(OUTPUT_PATH, "stories")
VIDEO_PATH = os.path.join(OUTPUT_PATH, "videos")

NEWS_API_KEY = os.environ['NEWS_API_KEY']
BING_API_KEY = os.environ['BING_API_KEY']
GEMINI_KEY = os.environ['GEMINI_KEY']
# Specify the path to the OAuth 2.0 credentials
CLIENT_SECRETS_FILE = "resources/youtube_creds.json"


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-pro:generateContent"
)

PLOTS = [
    (
        "By using modern and simple words, write a funny short story "
        "that is 6-8 sentences long about following article."
        "The story should start with a hook that grabs viewers attention.\n"
        "------------------------"
        "Topic: {topic}\n"
        "Title: {title}\n"
        "Text: {text}\n"
        "------------------------"
    )
]

TTS_CONFIG_PATH = "resources/xtts/config.json"
TTS_MODEL_PATH = "resources/xtts"
TTS_VOICES_PATH = "resources/voices/"
