import cv2
import textwrap
import numpy as np
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
)


def draw_text_with_outline(
    image, text, position, font, font_scale, text_color, outline_color, thickness
):
    """Draw text with an outline on an image."""
    # Calculate the size of the text
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_width, text_height = text_size
    
    # Padding around the text
    padding = 20
    
    # Background rectangle parameters
    bg_x = position[0] - padding
    bg_y = position[1] - text_height - padding
    bg_width = text_width + 2 * padding
    bg_height = text_height + 2 * padding
    
    # Create points for rounded rectangle
    rect_top_left = (bg_x, bg_y)
    rect_bottom_right = (bg_x + bg_width, bg_y + bg_height)
    
    # Draw the black background rectangle with rounded borders
    background_color = (0, 0, 0)
    border_radius = 20
    bg_rect_image = image.copy()
    cv2.rectangle(
        bg_rect_image, 
        rect_top_left, 
        rect_bottom_right, 
        background_color, 
        -1, 
        lineType=cv2.LINE_AA
    )
    cv2.addWeighted(bg_rect_image, 0.5, image, 0.5, 0, image)
    
    # Draw the rounded borders
    # cv2.rectangle(
    #     image, 
    #     rect_top_left, 
    #     rect_bottom_right, 
    #     background_color, 
    #     thickness=border_radius, 
    #     lineType=cv2.LINE_AA
    # )
    
    # Draw the outline
    cv2.putText(
        image,
        text,
        position,
        font,
        font_scale,
        outline_color,
        thickness + 2,
        lineType=cv2.LINE_AA,
    )
    
    # Draw the text
    cv2.putText(
        image,
        text,
        position,
        font,
        font_scale,
        text_color,
        thickness,
        lineType=cv2.LINE_AA,
    )


def write_text_on_video(
    words,
    video_path,
    output_path,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=2,
    text_color=(255, 255, 255),
    outline_color=(0, 0, 0),
    thickness=7,
    durations: list = None,
):

    # Load the video
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize the VideoWriter
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    current_word_index = 0 # Adjust width as needed
    current_word = words[current_word_index]["word"].strip()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Determine the current sentence to display

        if (
            current_word_index + 1 < len(words)
            and frame_count > words[current_word_index]["end_time"] * fps
        ):
            current_word_index += 1
            current_word = words[current_word_index]["word"].strip()
            # Wrap the text to fit the width of the video
        if frame_count > words[-1]["end_time"] * fps + 10:
            break
        # Get text size and position
        lines = [current_word]
        text_y = (height - len(lines) * 25) // 2
        text_size, _ = cv2.getTextSize(lines[0], font, font_scale, thickness)
        # Draw each line of wrapped text on the video frame
        y0, dy = text_y, text_size[1] + 25  # Adjust line spacing as needed
        for i, line in enumerate(lines):
            y = y0 + i * dy
            text_size, _ = cv2.getTextSize(line, font, font_scale, thickness)
            x = (width - text_size[0]) // 2
            draw_text_with_outline(
                frame,
                line,
                (x, y),
                font,
                font_scale,
                text_color,
                outline_color,
                thickness,
            )

        # Write the frame to the output video
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()


def add_audio_to_video(video_path, audio_path, output_path):
    """
    Adds audio to a video file and saves the output.

    Parameters:
    video_path (str): Path to the input video file.
    audio_path (str): Path to the input audio file.
    output_path (str): Path to save the output video file with audio.
    """
    # Load the video file
    video_clip = VideoFileClip(video_path)

    # Load the audio file
    audio_clip = AudioFileClip(audio_path)

    # Set the audio of the video clip
    video_clip_with_audio = video_clip.set_audio(audio_clip)

    # Write the result to a file
    video_clip_with_audio.write_videofile(
        output_path, codec="libx264", audio_codec="aac"
    )
