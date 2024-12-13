import random
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from pydub.utils import mediainfo
import math


def get_audio_duration(audio_path):
    """Get the duration of an audio file in seconds."""
    audio_info = mediainfo(audio_path)
    return float(audio_info["duration"])


def generate_subtitle_timing(facts, voiceover_paths):
    """Generate timing for subtitles based on the duration of the voiceovers."""
    timing = []
    current_time = 0

    for voiceover_path in voiceover_paths:
        duration = get_audio_duration(voiceover_path)
        timing.append((current_time, current_time + duration))
        current_time += duration

    return timing


def select_random_clip(background_video_path, total_duration, target_height=720):
    try:
        background = (
            VideoFileClip(background_video_path)
            .resize(height=target_height)
            .set_fps(30)
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load and resize background video: {e}")

    if total_duration > background.duration:
        raise ValueError("Background video is too short for the required duration.")

    start_time = random.uniform(0, max(0, background.duration - total_duration))
    return background.subclip(start_time, start_time + total_duration)


def create_fact_video(facts, voiceover_paths, background_video_path, output_path):
    if len(facts) != 5 or len(voiceover_paths) != 5:
        raise ValueError("You must provide exactly 5 facts and 5 voiceover paths.")

    # Calculate total duration based on the voiceover lengths
    total_duration = sum(get_audio_duration(path) for path in voiceover_paths)

    # Load the background video and resize it
    background_clip = select_random_clip(background_video_path, total_duration)
    background_clip = background_clip.set_duration(
        total_duration
    )  # Ensure duration matches

    # Generate timing for subtitles based on voiceover durations
    timing = generate_subtitle_timing(facts, voiceover_paths)

    # Create subtitle and voiceover clips
    subtitle_clips = []
    voiceover_clips = []

    for i, (fact, voiceover_path) in enumerate(zip(facts, voiceover_paths)):
        start_time, end_time = timing[i]

        # Load the voiceover
        voiceover_clip = AudioFileClip(voiceover_path).set_start(start_time)
        voiceover_clips.append(voiceover_clip)

        # Create the subtitle clip without a black background
        subtitle = (
            TextClip(
                fact,
                fontsize=24,
                color="white",  # White text
                size=background_clip.size,
                font="DejaVu-Sans",  # Make sure this font is available on your system
            )
            .set_position(("center", "bottom"))
            .set_duration(end_time - start_time)
            .set_start(start_time)
        )
        subtitle_clips.append(subtitle)

    # Concatenate all audio clips
    from moviepy.audio.AudioClip import concatenate_audioclips

    final_audio = concatenate_audioclips(voiceover_clips)

    # Combine background video with subtitles (no black background for text)
    video_with_subtitles = CompositeVideoClip(
        [background_clip.set_position(("center", "center")), *subtitle_clips]
    ).set_audio(final_audio)

    # Write the final video to the output path
    video_with_subtitles.write_videofile(
        output_path, codec="libx264", audio_codec="aac"
    )


# Example usage
facts = [
    "The Eiffel Tower can be 15 cm taller during the summer.",
    "Bananas are berries, but strawberries aren't.",
    "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old.",
    "Octopuses have three hearts.",
    "A day on Venus is longer than a year on Venus.",
]

voiceover_paths = [
    "voiceover1.mp3",
    "voiceover2.mp3",
    "voiceover3.mp3",
    "voiceover4.mp3",
    "voiceover5.mp3",
]

background_video_path = "assets/background_videos/Parkour.mp4"
output_path = "final_fact_video.mp4"

create_fact_video(facts, voiceover_paths, background_video_path, output_path)
