
import argparse
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def compress_video(input_path, output_path, bitrate="500k"):
    """
    Compresses a video file by re-encoding it with a specified bitrate.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the compressed video file.
        bitrate (str): The target video bitrate for the output file (e.g., "500k", "1000k").
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        return

    try:
        print(f"Loading video: {input_path}")
        clip = VideoFileClip(input_path)

        print(f"Compressing video with bitrate {bitrate}...")
        # Re-encode the video with a new bitrate. Audio is kept as is.
        clip.write_videofile(output_path, bitrate=bitrate)
        
        clip.close()
        print(f"Video compression complete. Saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress a video file by lowering its bitrate.")
    parser.add_argument("input_path", type=str, help="Path to the input video file.")
    parser.add_argument("output_path", type=str, help="Path for the compressed output video file.")
    parser.add_argument("--bitrate", type=str, default="500k", help="Target video bitrate (e.g., '500k', '1000k'). Default is '500k'.")

    args = parser.parse_args()

    compress_video(args.input_path, args.output_path, args.bitrate)
