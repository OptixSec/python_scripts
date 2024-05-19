import argparse
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, AgeRestrictedError
from tqdm import tqdm
import os

from dotenv import load_dotenv
load_dotenv()

# Define the fixed directory to save the audio
DOWNLOAD_PATH = os.getenv('DL_PATH')


def download_audio(url):
    try:
        # Create YouTube object
        yt = YouTube(url)
    except VideoUnavailable:
        print(f"Video is unavailable: {url}")
        return
    except AgeRestrictedError:
        print(f"Video is age restricted: {url}")
        return

    # Get the highest quality audio stream
    audio_stream = yt.streams.get_audio_only()

    # Set up the progress bar
    total_filesize = audio_stream.filesize
    with tqdm(total=total_filesize, unit="B", unit_scale=True, desc=yt.title) as pbar:

        def progress_callback(chunk, file_handle, bytes_remaining):
            pbar.update(len(chunk))

        # Attach the progress callback to the stream
        audio_stream.on_progress = progress_callback

        # Download the audio stream
        audio_stream.download(output_path=DOWNLOAD_PATH)
        print(f"Downloaded: {yt.title}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download the highest quality audio from a YouTube video."
    )
    parser.add_argument("url", help="URL of the YouTube video")
    args = parser.parse_args()
    download_audio(args.url)
