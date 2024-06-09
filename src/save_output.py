import os
import datetime as dt
import textwrap

from .constants import STORY_PATH, VIDEO_PATH

def save_output(
    topic: str,
    story: str,
    video: str,
    hashtags: str = "",
)-> None:
    
    #making sure the folder is there
    os.makedirs(STORY_PATH, exist_ok=True)
    os.makedirs(VIDEO_PATH, exist_ok=True)

    #using datetime string as a identifier.
    dt_string = dt.datetime.now().strftime('%Y%m%d%H%M')

    #writing string
    with open(os.path.join(STORY_PATH,f"/story_{dt_string}.txt"),"w") as file:
        #Writing output
        file.write("Topic:\n")
        file.write(topic + "\n")
        file.write("Story:\n")
        file.write(textwrap.wrap(story) +"\n")
        if hashtags:
            file.write("Hashtags:\n")
            file.write(hashtags)
    #TODO: Write video
    return