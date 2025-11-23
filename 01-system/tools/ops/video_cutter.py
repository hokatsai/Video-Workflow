
import argparse
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def cut_video(input_path, output_path, start_time, end_time):
    """
    Cuts a video from a specified start time to an end time.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the output video file.
        start_time (float): Start time of the clip in seconds.
        end_time (float): End time of the clip in seconds.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        return

    try:
        print(f"Loading video: {input_path}")
        with VideoFileClip(input_path) as video:
            # Create a subclip
            new_clip = video.subclipped(start_time, end_time)

            print(f"Writing subclip to: {output_path}")
            # Write the result to a file
            new_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        print("Video cutting complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cut a video to a specified duration.")
    parser.add_argument("input_path", type=str, help="Path to the input video file.")
    parser.add_argument("output_path", type=str, help="Path for the output video file.")
    parser.add_argument("start_time", type=float, help="Start time for the cut (in seconds).")
    parser.add_argument("end_time", type=float, help="End time for the cut (in seconds).")

    args = parser.parse_args()

    cut_video(args.input_path, args.output_path, args.start_time, args.end_time)
