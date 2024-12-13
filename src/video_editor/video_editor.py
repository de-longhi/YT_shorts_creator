from moviepy.editor import VideoFileClip, AudioFileClip
from text_to_speech import text_to_speech


class youtuber:
    def __init__(self, video_path, audio_paths, subtitles, output_path):
        self.video = VideoFileClip(video_path)
        self.audios = []
        for path in audio_paths:
            self.audios.append(AudioFileClip(path))
        self.subtitles = subtitles
        self.output_path = output_path

    def merge_audio_video(video_path, audio_path, output_path):

        # Set audio to video
        video_with_audio = video.set_audio(audio)

        # Write the result to the output file
        video_with_audio.write_videofile(
            output_path, codec="libx264", audio_codec="aac"
        )

    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

    def _add_subtitles(timing):
        """
        Add subtitles to a video.

        Args:
            video_path (str): Path to the input video.
            subtitles (list of str): List of subtitle strings.
            timing (list of tuple): List of (start_time, end_time) tuples for each subtitle.
            output_path (str): Path to save the output video.
        """
        # Load the video
        video = VideoFileClip(video_path)

        # Create subtitle clips
        subtitle_clips = []
        for text, (start, end) in zip(subtitles, timing):
            # Create a TextClip for each subtitle
            subtitle = (
                TextClip(
                    text, fontsize=24, color="white", bg_color="black", size=video.size
                )
                .set_position(("center", "bottom"))
                .set_duration(end - start)
                .set_start(start)
            )
            subtitle_clips.append(subtitle)

        # Overlay subtitles on the video
        final_video = CompositeVideoClip([video, *subtitle_clips])

        # Write the result
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Example usage
    subtitles = [
        "This is the first part of the text.",
        "Here is the second part.",
        "Finally, this is the last part.",
    ]
    timing = [(0, 2), (2, 5), (5, 7)]  # (start_time, end_time) in seconds for each text

    add_subtitles("output_with_audio.mp4", subtitles, timing, "final_output.mp4")
