#!/usr/bin/python_venv/bin/python

import os
import random
import pygame
import threading

from dotenv import load_dotenv

load_dotenv()

# Initialize pygame mixer
pygame.mixer.init()

# Initialize the pygame display module (needed for event handling)
pygame.display.init()
pygame.display.set_mode((1, 1))

# Set the path to the directory containing mp3 files
MUSIC_DIR = os.getenv("MUSIC_DIR")


# Function to get all mp3 files in the directory and subdirectories
def get_mp3_files(music_dir):
    mp3_files = []
    for root, _, files in os.walk(music_dir):
        for file in files:
            if file.endswith(".mp3"):
                mp3_files.append(os.path.join(root, file))
    return mp3_files


# Load all mp3 files
mp3_files = get_mp3_files(MUSIC_DIR)


# Function to play a song
def play_song(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


# Function to pause the song
def pause_song():
    pygame.mixer.music.pause()


# Function to unpause the song
def unpause_song():
    pygame.mixer.music.unpause()


# Function to stop the song
def stop_song():
    pygame.mixer.music.stop()


# Function to play a random song
def play_random_song():
    if mp3_files:
        song = random.choice(mp3_files)
        play_song(song)
        print(f"Playing: {song}")
    else:
        print("No songs found in the directory.")


# Define a custom event for when a song ends
SONG_END_EVENT = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END_EVENT)


# Event handling function
def handle_events():
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END_EVENT:
                play_random_song()


# Command-line interface
def music_player():
    print("Welcome to the Command-line Music Player!")
    print("Commands: play [song], pause, unpause, stop, random, skip, quit")

    play_random_song()  # Start by playing a random song

    # Start the event handling thread
    threading.Thread(target=handle_events, daemon=True).start()

    while True:
        command = input("Enter command: ").strip().lower()
        if command.startswith("play"):
            song_name = command[5:].strip()
            song_path = None
            for file in mp3_files:
                if song_name in os.path.basename(file):
                    song_path = file
                    break
            if song_path:
                play_song(song_path)
                print(f"Playing: {song_path}")
            else:
                print(f"Song '{song_name}' not found.")
        elif command == "pause":
            pause_song()
            print("Paused.")
        elif command == "unpause":
            unpause_song()
            print("Unpaused.")
        elif command == "stop":
            stop_song()
            print("Stopped.")
        elif command == "random" or command == "skip":
            play_random_song()
        elif command == "quit":
            stop_song()
            print("Goodbye!")
            break
        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    music_player()
