import argparse
import ffmpeg
import os


def convert_to_wav(input_file, output_file):
    try:
        # Use ffmpeg to convert the file to wav format with the highest quality
        ffmpeg.input(input_file).output(
            output_file, format="wav", acodec="pcm_s16le"
        ).run(overwrite_output=True)
        print(f"Conversion to WAV successful: {output_file}")
    except ffmpeg.Error as e:
        print(f"Error occurred during WAV conversion: {e}")


def convert_to_mp3(input_file, output_file):
    try:
        # Use ffmpeg to convert the file to mp3 format with the highest quality
        ffmpeg.input(input_file).output(
            output_file, format="mp3", audio_bitrate="320k"
        ).run(overwrite_output=True)
        print(f"Conversion to MP3 successful: {output_file}")
    except ffmpeg.Error as e:
        print(f"Error occurred during MP3 conversion: {e}")


def convert_files_in_directory(directory, remove_input=False):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp4") or file.endswith(".webm"):
                input_file = os.path.join(root, file)
                base_name = os.path.splitext(file)[0]
                temp_wav_file = os.path.join(root, f"{base_name}.wav")
                output_file = os.path.join(root, f"{base_name}.mp3")

                convert_to_wav(input_file, temp_wav_file)
                convert_to_mp3(temp_wav_file, output_file)

                if os.path.isfile(temp_wav_file):
                    os.remove(temp_wav_file)
                    print(f"Deleted temporary WAV file: {temp_wav_file}")

                if remove_input and os.path.isfile(input_file):
                    os.remove(input_file)
                    print(f"Deleted original input file: {input_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert .mp4 and .webm files to .mp3 format via .wav."
    )
    parser.add_argument(
        "directory", help="Path to the directory containing input files"
    )
    parser.add_argument(
        "-r",
        "--remove-input",
        action="store_true",
        help="Remove input files after conversion",
    )
    args = parser.parse_args()

    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Directory {args.directory} does not exist.")
        return

    # Convert files in directory
    convert_files_in_directory(args.directory, args.remove_input)


if __name__ == "__main__":
    main()
