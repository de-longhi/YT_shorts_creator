from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
import random
from pydub.utils import mediainfo


class Youtuber:
    def __init__(self, video_path, audio_paths, subtitles, output_path):
        self.video_path = video_path
        self.audio_paths = audio_paths
        self.subtitles = subtitles
        self.output_path = output_path

    @staticmethod
    def get_audio_duration(audio_path):
        audio_info = mediainfo(audio_path)
        return float(audio_info["duration"])

    def _generate_subtitle_timing(self, facts, voiceover_paths):
        """Generate timing for subtitles based on the duration of the voiceovers."""
        timing = []
        current_time = 0

        for voiceover_path in voiceover_paths:
            duration = self.get_audio_duration(voiceover_path)
            timing.append((current_time, current_time + duration))
            current_time += duration

        return timing

    def _select_random_clip(self, total_duration, target_height=720):
        try:
            background = (
                VideoFileClip(self.video_path).resize(height=target_height).set_fps(30)
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load and resize background video: {e}")

        if total_duration > background.duration:
            raise ValueError("Background video is too short for the required duration.")

        start_time = random.uniform(0, max(0, background.duration - total_duration))
        return background.subclip(start_time, start_time + total_duration)

    def create_fact_video(self):
        if len(self.subtitles) != 5 or len(self.audio_paths) != 5:
            raise ValueError("You must provide exactly 5 facts and 5 voiceover paths.")

        # Calculate total duration based on the voiceover lengths
        total_duration = sum(self.get_audio_duration(path) for path in self.audio_paths)

        # Load the background video and resize it
        background_clip = self._select_random_clip(total_duration)
        background_clip = background_clip.set_duration(
            total_duration
        )  # Ensure duration matches

        # Generate timing for subtitles based on voiceover durations
        timing = self._generate_subtitle_timing(self.subtitles, self.audio_paths)

        # Create subtitle and voiceover clips
        subtitle_clips = []
        voiceover_clips = []

        for i, (fact, voiceover_path) in enumerate(
            zip(self.subtitles, self.audio_paths)
        ):
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
            self.output_path, codec="libx264", audio_codec="aac"
        )
