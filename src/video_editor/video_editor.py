from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
import random
import textwrap
from pydub.utils import mediainfo


class Youtuber:
    def __init__(
        self,
        video_path,
        audio_paths,
        subtitles,
        output_path,
        background_music_path=None,
    ):
        self.video_path = video_path
        self.audio_paths = audio_paths
        self.subtitles = subtitles
        self.output_path = output_path
        self.background_music_path = background_music_path

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

    def _split_subtitle_into_chunks(self, text, min_words=3, max_words=5):
        """Split subtitles into chunks of 3 to 5 words."""
        words = text.split()
        chunks = []
        i = 0

        while i < len(words):
            chunk_size = random.randint(min_words, max_words)
            chunks.append(" ".join(words[i : i + chunk_size]))
            i += chunk_size

        return chunks

    def _select_random_cropped_clip(
        self, total_duration, target_width=1080, target_height=1920
    ):
        try:
            # Load the video
            background = VideoFileClip(self.video_path)

            # Ensure the video is long enough for the required duration
            if total_duration > background.duration:
                raise ValueError(
                    "Background video is too short for the required duration."
                )

            # Select a random starting point for the subclip
            start_time = random.uniform(0, max(0, background.duration - total_duration))
            end_time = start_time + total_duration
            background = background.subclip(start_time, end_time)

            # Calculate cropping dimensions to center the video horizontally
            target_aspect_ratio = target_width / target_height
            new_width = background.h * target_aspect_ratio

            # Crop the width to match the target aspect ratio
            background = background.crop(
                x_center=background.w / 2,  # Center horizontally
                width=new_width,
                height=background.h,  # Preserve original height
            )

            # Resize the video to match the exact target dimensions (1080x1920)
            background = background.resize(width=target_width, height=target_height)

        except Exception as e:
            raise RuntimeError(
                f"Failed to load, crop, or resize the background video: {e}"
            )

        return background

    def create_fact_video(self, min_words_per_subtitle=5, max_words_per_subtitle=5):
        # if len(self.subtitles) != 5 or len(self.audio_paths) != 5:
        #     raise ValueError("You must provide exactly 5 facts and 5 voiceover paths.")

        # Calculate total duration based on the voiceover lengths
        total_duration = sum(self.get_audio_duration(path) for path in self.audio_paths)

        # Load a randomly cropped section of the background video and resize it to a YouTube Shorts format (1080x1920)
        background_clip = self._select_random_cropped_clip(total_duration)
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

            # Split the subtitle into smaller chunks of 3 to 5 words
            subtitle_chunks = self._split_subtitle_into_chunks(
                fact, min_words_per_subtitle, max_words_per_subtitle
            )

            # Load the voiceover
            voiceover_clip = AudioFileClip(voiceover_path).set_start(start_time)
            voiceover_clips.append(voiceover_clip)

            # Calculate chunk timing within the voiceover's duration
            chunk_duration = (end_time - start_time) / len(subtitle_chunks)
            chunk_start_time = start_time

            for chunk in subtitle_chunks:
                subtitle = (
                    TextClip(
                        chunk,
                        fontsize=48,  # Larger font size
                        color="white",  # White text
                        stroke_color="black",  # Black outline
                        stroke_width=2,  # Outline thickness
                        font="DejaVu-Sans-Bold",  # Bold and readable font
                        method="caption",  # Ensures word wrapping for long text
                        size=(1080, None),  # Width matches YouTube Shorts format
                    )
                    .set_position(
                        ("center", "center")
                    )  # Position subtitles in the middle of the screen
                    .set_duration(chunk_duration)
                    .set_start(chunk_start_time)
                )
                subtitle_clips.append(subtitle)
                chunk_start_time += chunk_duration

        # Concatenate all audio clips
        from moviepy.audio.AudioClip import concatenate_audioclips

        final_audio = concatenate_audioclips(voiceover_clips)

        # Add background music if provided
        if self.background_music_path:
            background_music = (
                AudioFileClip(self.background_music_path)
                .set_duration(total_duration)
                .volumex(0.1)
            )  # Lower the volume
            from moviepy.audio.AudioClip import CompositeAudioClip

            final_audio = CompositeAudioClip([final_audio, background_music])

        # Combine background video with subtitles
        video_with_subtitles = CompositeVideoClip(
            [background_clip.set_position(("center", "center")), *subtitle_clips]
        ).set_audio(final_audio)

        # Write the final video to the output path
        video_with_subtitles.write_videofile(
            self.output_path, codec="libx264", audio_codec="aac"
        )
