
import argparse
import os
from pydub import AudioSegment

def compress_audio(input_path, output_path, bitrate="64k"):
    """
    Compresses an audio file to a specified bitrate.

    Args:
        input_path (str): Path to the input audio file.
        output_path (str): Path to save the compressed audio file.
        bitrate (str): The target bitrate for the output file (e.g., "64k", "128k").
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        return

    try:
        print(f"Loading audio from: {input_path}")
        audio = AudioSegment.from_file(input_path)

        print(f"Compressing and exporting to: {output_path} with bitrate {bitrate}")
        audio.export(output_path, format=os.path.splitext(output_path)[1][1:], bitrate=bitrate)
        
        print("Audio compression complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress an audio file to a specified bitrate.")
    parser.add_argument("input_path", type=str, help="Path to the input audio file.")
    parser.add_argument("output_path", type=str, help="Path for the compressed output audio file.")
    parser.add_argument("--bitrate", type=str, default="64k", help="Target bitrate (e.g., '64k', '128k'). Default is '64k'.")

    args = parser.parse_args()

    compress_audio(args.input_path, args.output_path, args.bitrate)
