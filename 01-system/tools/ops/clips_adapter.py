
import argparse
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def adapt_clip(input_path, output_path, resolution=None, fps=None):
    """
    Adapts a video clip to a new resolution and/or frame rate.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the adapted video file.
        resolution (str): New resolution as "widthxheight" (e.g., "1920x1080").
        fps (int): New frame rate.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        return

    try:
        print(f"Loading video: {input_path}")
        clip = VideoFileClip(input_path)

        if resolution:
            try:
                width, height = map(int, resolution.split('x'))
                print(f"Resizing clip to {width}x{height}")
                clip = clip.resize((width, height))
            except ValueError:
                print(f"Error: Invalid resolution format. Please use 'widthxheight' (e.g., '1920x1080').")
                return

        if fps:
            print(f"Setting FPS to {fps}")
            clip = clip.set_fps(fps)

        print(f"Writing adapted clip to: {output_path}")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        clip.close()
        print("Clip adaptation complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adapt a video clip to a new resolution and/or frame rate.")
    parser.add_argument("input_path", type=str, help="Path to the input video file.")
    parser.add_argument("output_path", type=str, help="Path for the output adapted video file.")
    parser.add_argument("--resolution", type=str, help="New resolution as 'widthxheight' (e.g., '1920x1080').")
    parser.add_argument("--fps", type=int, help="New frame rate (e.g., 25, 30).")

    args = parser.parse_args()

    adapt_clip(args.input_path, args.output_path, args.resolution, args.fps)
