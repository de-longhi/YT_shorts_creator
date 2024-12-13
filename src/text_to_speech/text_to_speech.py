import boto3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve AWS credentials and region from .env
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_REGION):
    raise ValueError("AWS credentials or region are not set. Check your .env file.")

# Initialize Polly client
polly_client = boto3.client(
    "polly",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def synthesize_speech(text, out_name, output_format="mp3", voice_id="Joanna"):
    """
    Convert text to speech using Amazon Polly.

    Args:
        text (str): The text to synthesize.
        output_format (str): The output format (e.g., 'mp3', 'ogg_vorbis', 'pcm').
        voice_id (str): The voice to use (e.g., 'Joanna', 'Matthew').

    Returns:
        str: The path to the generated audio file.
    """
    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
        )

        audio_filename = f"{out_name}.{output_format}"
        with open(audio_filename, "wb") as audio_file:
            audio_file.write(response["AudioStream"].read())

        return audio_filename

    except Exception as e:
        print(f"Error synthesizing speech: {e}")
        return None
