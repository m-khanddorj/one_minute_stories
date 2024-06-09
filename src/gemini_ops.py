import random
import requests
import json

from .constants import GEMINI_URL, GEMINI_KEY, PLOTS

def gemini_api(text: str)-> str:
    headers = {
        "Content-Type": "application/json",
    }

    params = {
        "key": GEMINI_KEY,
    }

    json_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text":text
                    },
                ],
            },
        ],
    }

    response = requests.post(
        GEMINI_URL,
        params=params,
        headers=headers,
        json=json_data,
    )
    assert response.status_code == 200, (
        str(response.status_code) + "" + response.content
    )
    response_content = json.loads(response.content.decode())
    story = response_content["candidates"][0]["content"]["parts"][0]["text"]
    return story

def generate_story(article: str):
    plot = random.choice(PLOTS)
    text = plot.format(
        topic=article["topic"],
        title=article["title"],
        text=article["description"],
    )
    return gemini_api(text)


def get_title(story: str):
    return gemini_api(
        "Using modern and simple words, give this story a title that will be used as a youtube shorts title\n"
        + story
    )
