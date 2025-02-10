from facts_collector import facts_collector
from config import API_NINJAS_KEY
from text_to_speech import text_to_speech
from video_editor import video_editor

FACTS_LIMIT = 5
API_URL = f"https://api.api-ninjas.com/v1/facts"


def main():

    print("Fetching facts...")
    scientist = facts_collector.scientist(API_URL, API_NINJAS_KEY)
    facts = []
    subtitles = []
    for i in range(FACTS_LIMIT):
        subtitles.append(f"{i+1}.")
        newfact = scientist.fetch()

        facts.append(newfact)
        subtitles.append(newfact)

    print("Creating audio files...")
    # Synthesize speech
    i = 1
    audio_paths = []
    for fact in facts:
        audio_paths.append(f"assets/numbers/number{i}.mp3")
        text_to_speech.synthesize_speech(fact, f"src/text_to_speech/out/voiceover{i}")
        audio_paths.append(f"src/text_to_speech/out/voiceover{i}.mp3")
        i += 1

    print("Creating video...")
    youtuber = video_editor.Youtuber(
        "assets/background_videos/Parkour.mp4",
        audio_paths,
        subtitles,
        "./out/video.mp4",
        "assets/songs/poison.mp3",
    )

    youtuber.create_fact_video()


if __name__ == "__main__":
    main()
