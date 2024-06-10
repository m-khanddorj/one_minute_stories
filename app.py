import datetime as dt
import time
import json
import pickle
import os

from src.utils import (
    split_story_into_sentences,
    select_random_file,
)
from src.trends_ops import (
    get_top_trending_topics_in_india, 
    get_related_news_articles_bing
)
from src.gemini_ops import generate_story, get_title
from src.tts_ops import tts
from src.video_ops import write_text_on_video, add_audio_to_video
from src.youtube_ops import authenticate_youtube, upload_video
from src.transcribe_ops import transcribe_with_timestamps
from src.constants import AUDIO_FPS, BING_API_KEY

import pytz

def get_indian_standard_time_slots(date):

    # Define the Indian timezone
    india_tz = pytz.timezone('Asia/Kolkata')
    
    # Define the time slots in Indian time
    time_slots = [dt.datetime(date.year, date.month, date.day, 8, 0, 0),
                  dt.datetime(date.year, date.month, date.day, 12, 0, 0),
                  dt.datetime(date.year, date.month, date.day, 20, 0, 0)]
    
    # Convert the naive datetimes to Indian Standard Time
    time_slots_in_india = [india_tz.localize(slot) for slot in time_slots]
    
    return time_slots_in_india

def convert_to_utc_and_format(time_slots):
    # Define UTC timezone
    utc_tz = pytz.utc
    
    # Convert the IST datetime objects to UTC
    time_slots_in_utc = [slot.astimezone(utc_tz) for slot in time_slots]
    
    return time_slots_in_utc

if __name__ == "__main__":
    india_times = get_indian_standard_time_slots(dt.date.today() + dt.timedelta(2))
    formatted_time_slots = convert_to_utc_and_format(india_times)

    if os.path.exists("youtube.pkl"):
        with open("youtube.pkl","rb") as f: 
            youtube = pickle.load(f)
    else:
        youtube = authenticate_youtube()
        with open("youtube.pkl","wb") as f: 
            pickle.dump(youtube,f)
            #last updated @2024/05/28
    top_trending_topics = get_top_trending_topics_in_india(3)
    articles = get_related_news_articles_bing(top_trending_topics, BING_API_KEY)
    for article, t in zip(articles,india_times):

        story = generate_story(article)
        dt_string = dt.datetime.now().strftime('%Y%m%d%H%M')

        title = get_title(story)
        topic = article['topic']
        hashtags = (
            f'#{"".join([word.capitalize() for word in topic.split(" ")])} '
            "#youtubeshorts #youtube #shorts #youtuber #viral"
        )
        article["story"] = story
        article["hashtags"] = hashtags

        with open(f"outputs/stories/story_{dt_string}.txt","w") as file:
            # file.write(article)
            json.dump(article,file)

        sentences = split_story_into_sentences(story=story)
        wavs = tts(sentences,"temp.wav")
        words_list = transcribe_with_timestamps("temp.wav")
        background_video_path = select_random_file(
            "/home/khanddorj/Documents/code/one_minute_stories/resources/background_videos"
        )

        audio_durations = []
        for wav in wavs:
            audio_durations.append(len(wav) / AUDIO_FPS)

        write_text_on_video(
            words_list, background_video_path, "temp.mp4", durations=audio_durations
        )

        add_audio_to_video(
            "temp.mp4",
            "temp.wav",
            f"outputs/videos/video_{dt_string}.mp4",
        )
        response = upload_video(
            youtube,
            f"outputs/videos/video_{dt_string}.mp4",
            title,
            story,
            hashtags,
            t
        )
        print(f"Uploaded video {article['topic']}: {response}")
        time.sleep(60)
