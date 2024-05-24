#!/usr/bin/python_venv/bin/python

import argparse
from pytube import YouTube, Playlist
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

# Define the fixed directory to save the audio
DOWNLOAD_PATH = os.getenv("MUSIC_DIR")

# Append a subdirectory to DOWNLOAD_PATH
DOWNLOAD_PATH = os.path.join(DOWNLOAD_PATH, "youtube_downloads")


def format_stream_string(input_string):
    # Remove the leading "<Stream: " and the trailing ">"
    input_string = input_string[len("<Stream: ") : -1]

    # Split the string by ", " to get each key-value pair
    parts = input_string.split(", ")

    # Join the parts with the required formatting
    formatted_string = "Audio Stream: " + ", ".join(parts)

    return formatted_string


def get_audio_streams(url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(only_audio=True, adaptive=True)
        for stream in streams:
            stream_info = format_stream_string(str(stream))
            print(stream_info)
        return streams
    except Exception as e:
        print(f"{url}\nError: {e}")
        return False


def download_audio(url, playlist_name=None, itag=None):
    print(f"Processing URL: {url}")
    if playlist_name:
        print(f"Playlist Name: {playlist_name}")
    try:
        # Create YouTube object
        yt = YouTube(url)
    except Exception as e:
        print(f"{url}\nError: {e}")
        return False

    try:
        # Get the specified audio stream by itag or the highest quality audio stream
        if itag:
            audio_stream = yt.streams.get_by_itag(itag)
            if not audio_stream:
                print(f"No stream found with itag: {itag}")
                return False
        else:
            audio_stream = yt.streams.get_audio_only("webm")

        # Determine download path
        if playlist_name:
            playlist_folder = os.path.join(DOWNLOAD_PATH, playlist_name)
            if not os.path.exists(playlist_folder):
                os.makedirs(playlist_folder)
            download_path = playlist_folder
        else:
            download_path = DOWNLOAD_PATH

        # Set up the progress bar
        total_filesize = audio_stream.filesize
        with tqdm(
            total=total_filesize, unit="B", unit_scale=True, desc=yt.title
        ) as pbar:

            def progress_callback(stream, chunk, bytes_remaining):
                pbar.update(len(chunk))

            yt.register_on_progress_callback(progress_callback)

            # Download the audio stream
            audio_stream.download(output_path=download_path)
            print(f"Downloaded: {yt.title}")
        return True
    except Exception as e:
        print(f"{url}\nError: {e}")
        return False


def download_audio_from_file(file_path, itag=None):
    with open(file_path, "r") as file:
        urls = file.readlines()

    # Strip whitespace characters from the ends of the URLs
    urls = [url.strip() for url in urls]

    failed_urls = []

    for url in urls:
        if url:  # Check if the URL is not empty
            if not download_audio(url, itag=itag):
                failed_urls.append(url)  # Add failed URL to the failed list

    # Clear the content of the original file
    with open(file_path, "w") as file:
        file.write("")

    # Append failed URLs to the failed_urls.txt file
    if failed_urls:
        with open("failed_urls.txt", "a") as file:
            for url in failed_urls:
                file.write(url + "\n")


def download_playlist(url):
    try:
        playlist = Playlist(url)
        playlist_name = playlist.title  # Get the playlist title
        for video_url in playlist.video_urls:
            print(f"Processing Video: {video_url}")
            try:
                download_audio(video_url, playlist_name=playlist_name)
            except Exception as e:
                print(f"Error downloading video {video_url}: {e}")
    except Exception as e:
        print(f"Error processing playlist: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download the highest quality audio from a YouTube video or from YouTube videos listed in a text file."
    )
    parser.add_argument("-u", "--url", help="URL of the YouTube video or playlist")
    parser.add_argument(
        "-f", "--file", help="Path to the text file containing YouTube video URLs"
    )
    parser.add_argument(
        "-s",
        "--streams",
        action="store_true",
        help="List all available audio streams without downloading",
    )
    parser.add_argument(
        "-t", "--tag", type=int, help="itag number of the audio stream to download"
    )

    args = parser.parse_args()

    if args.streams:
        if args.url:
            get_audio_streams(args.url)
        elif args.file:
            with open(args.file, "r") as file:
                urls = file.readlines()
            urls = [url.strip() for url in urls]
            for url in urls:
                if url:
                    get_audio_streams(url)
    elif args.url:
        if "playlist" in args.url:
            download_playlist(args.url)
        else:
            download_audio(args.url)
    elif args.file:
        download_audio_from_file(args.file, args.tag)
