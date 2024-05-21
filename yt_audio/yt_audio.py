import argparse
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, AgeRestrictedError
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

# Define the fixed directory to save the audio
DOWNLOAD_PATH = os.getenv("DL_PATH")


def download_audio(url):
    try:
        # Create YouTube object
        yt = YouTube(url)
    except VideoUnavailable:
        print(f"Video is unavailable: {url}")
        return False
    except AgeRestrictedError:
        print(f"Video is age restricted: {url}")
        return False
    except Exception as e:
        print(f"An error occurred while processing the video: {url}\nError: {e}")
        return False

    try:
        # Get the highest quality audio stream
        audio_stream = yt.streams.get_audio_only()

        # Set up the progress bar
        total_filesize = audio_stream.filesize
        with tqdm(
            total=total_filesize, unit="B", unit_scale=True, desc=yt.title
        ) as pbar:

            def progress_callback(stream, chunk, bytes_remaining):
                pbar.update(len(chunk))

            yt.register_on_progress_callback(progress_callback)

            # Download the audio stream
            audio_stream.download(output_path=DOWNLOAD_PATH)
            print(f"Downloaded: {yt.title}")
        return True
    except Exception as e:
        print(f"An error occurred during downloading: {url}\nError: {e}")
        return False


def download_audio_from_file(file_path):
    with open(file_path, "r") as file:
        urls = file.readlines()

    # Strip whitespace characters from the ends of the URLs
    urls = [url.strip() for url in urls]

    failed_urls = []

    for url in urls:
        if url:  # Check if the URL is not empty
            print(f"Processing URL: {url}")
            if not download_audio(url):
                failed_urls.append(url)  # Add failed URL to the failed list

    # Clear the content of the original file
    with open(file_path, "w") as file:
        file.write("")

    # Append failed URLs to the failed_urls.txt file
    if failed_urls:
        with open("failed_urls.txt", "a") as file:
            for url in failed_urls:
                file.write(url + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download the highest quality audio from a YouTube video or from YouTube videos listed in a text file."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="URL of the YouTube video")
    group.add_argument(
        "-f", "--file", help="Path to the text file containing YouTube video URLs"
    )

    args = parser.parse_args()

    if args.url:
        download_audio(args.url)
    elif args.file:
        download_audio_from_file(args.file)
