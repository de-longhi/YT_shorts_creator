from facts_collector import facts_collector
from config import API_NINJAS_KEY
from text_to_speech import text_to_speech

FACTS_LIMIT = 1
API_URL = f"https://api.api-ninjas.com/v1/facts"


def main():
    # Fetch facts (e.g., 3 facts)

    scientist = facts_collector.scientist(API_URL, API_NINJAS_KEY, debug=True)
    facts = scientist.fetch()
    if facts:
        print("Interesting Facts:")
        for i, fact in enumerate(facts, start=1):
            print(fact)
    else:
        print("Failed to fetch facts.")
        
    text = "Hello! This is a test of Amazon Polly's text-to-speech capabilities."

    # Synthesize speech
    audio_file = text_to_speech.synthesize_speech(text, output_format="mp3", voice_id="Joanna")
    if audio_file:
        print(f"Audio file generated: {audio_file}")
    else:
        print("Failed to generate audio file.")


if __name__ == "__main__":
    main()
