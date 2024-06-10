# Trending Topics Video Generator
## Overview
This project automates the creation of YouTube videos based on the latest trending topics in India. It involves multiple steps, from fetching trending topics to generating a video and uploading it to YouTube. The project utilizes various APIs and tools to achieve this goal.

Youtube Channel: https://www.youtube.com/channel/UCvKi4wzs2BbEchGfcYKSxxw

## Workflow
**Fetch Trending Topics**: Uses Google Trends to get the latest trending topics in India.

**Get Related News**: Fetches news related to the trending topics using News API or Bing API.

**Generate Stories**: Feeds the trending topics and news into Gemini to generate short funny stories.

**Text-to-Speech**: Uses xtts to convert the generated stories into audio.

**Transcribe Audio**: Uses WhisperAI to transcribe the audio, obtaining the start and end times of every word.

**Create Video**: Adds the audio and transcribed words (one by one) to a background video.

**Upload to YouTube**: Uploads the generated video to YouTube using YouTube Data API v3.


## Used tools
Python 3.11
Google Trends API (For fetching trending topics)
News API (For fetching news)
Bing API (For fetching news)
Gemini API (for generating funny stories)
xtts (for text-to-speech)
WhisperAI (for audio transcription)
MoviePy (for video creation)

## Get started:

1. Clone this repository
2. Install requirements
3. Get Gemini API key , Bing News API key and News API key. All of them have free tiers.
4. From Youtube data API v3, get OAUTH 2.0 credential and put it under ./resources/youtube_creds.json
5. Download TTS model weights from https://huggingface.co/coqui/XTTS-v2/tree/main and put it in ./resources/xtts
6. Prepare 1080x1920 videos ans put them under ./resources/background_videos
7. Download your favorite voicec actors talking audios to ./resources/voices
8. Run app.py

## License
This project is licensed under the CC BY-NC-SA License.

