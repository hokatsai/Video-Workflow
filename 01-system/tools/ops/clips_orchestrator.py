
import argparse
import subprocess
import os
import json
import sys # Import sys for sys.executable
import shutil # Import shutil for file operations

def run_tool(script_path, *args):
    """Helper function to run other tools as subprocesses."""
    # Use sys.executable to ensure the correct Python interpreter from the venv is used
    command = [sys.executable, script_path] + list(args)
    
    print(f"DEBUG: Running command: {' '.join(command)}") # Debug print
    
    result = subprocess.run(command, capture_output=True, text=True, check=False) # check=False to handle errors manually
    
    if result.returncode != 0:
        print(f"Error running {os.path.basename(script_path)}:")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        return False
    # print(result.stdout) # Suppress stdout unless debugging specific tool output
    return True

def orchestrate_clips(input_video, timestamps_file, output_base_dir, target_resolution=None, target_fps=None):
    """
    Orchestrates the cutting and adaptation of video clips.

    Args:
        input_video (str): Path to the source video file.
        timestamps_file (str): Path to a JSON file containing clip timestamps.
                                Format: [{"start": 0.0, "end": 10.0, "name": "intro"}, ...]
        output_base_dir (str): Base directory to save all processed clips.
        target_resolution (str): Optional target resolution (e.g., "1280x720").
        target_fps (int): Optional target frame rate.
    """
    if not os.path.exists(input_video):
        print(f"Error: Input video '{input_video}' not found.")
        return
    if not os.path.exists(timestamps_file):
        print(f"Error: Timestamps file '{timestamps_file}' not found.")
        return

    os.makedirs(output_base_dir, exist_ok=True)

    try:
        with open(timestamps_file, 'r', encoding='utf-8') as f:
            timestamps = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from timestamps file '{timestamps_file}'. Please ensure it's valid JSON.")
        return
    except Exception as e:
        print(f"Error reading timestamps file: {e}")
        return

    # Get the absolute paths to the other tool scripts
    current_script_dir = os.path.dirname(__file__)
    video_cutter_script = os.path.join(current_script_dir, 'video_cutter.py')
    clips_adapter_script = os.path.join(current_script_dir, 'clips_adapter.py')
    # clips_copy_exporter_script is not directly called here, but implied by the final copy operation

    processed_clips_temp_dir = os.path.join(output_base_dir, "temp_processed_clips")
    os.makedirs(processed_clips_temp_dir, exist_ok=True)

    print(f"Starting orchestration for video: {input_video}")
    print(f"Output will be saved to: {output_base_dir}")

    for i, ts in enumerate(timestamps):
        start_time = ts.get("start")
        end_time = ts.get("end")
        clip_name = ts.get("name", f"clip_{i+1}")
        
        if start_time is None or end_time is None:
            print(f"Warning: Skipping clip '{clip_name}' due to missing start or end time. Entry: {ts}")
            continue

        print(f"\n--- Processing clip: '{clip_name}' ({start_time}-{end_time}s) ---")
        
        # Define paths for intermediate files
        temp_cut_path = os.path.join(processed_clips_temp_dir, f"{clip_name}_cut.mp4")
        temp_adapted_path = os.path.join(processed_clips_temp_dir, f"{clip_name}_adapted.mp4")
        
        # 1. Cut the video
        print(f"Cutting clip '{clip_name}' from {start_time} to {end_time} seconds...")
        if not run_tool(video_cutter_script, input_video, temp_cut_path, str(start_time), str(end_time)):
            print(f"Failed to cut clip '{clip_name}'. Skipping further processing for this clip.")
            continue
        
        current_clip_path = temp_cut_path # Path to the clip after cutting

        # 2. Adapt resolution/FPS if requested
        if target_resolution or target_fps:
            adapter_args = [current_clip_path, temp_adapted_path]
            if target_resolution:
                adapter_args.extend(["--resolution", target_resolution])
            if target_fps:
                adapter_args.extend(["--fps", str(target_fps)])
            
            print(f"Adapting clip '{clip_name}' (res: {target_resolution}, fps: {target_fps})...")
            if not run_tool(clips_adapter_script, *adapter_args):
                print(f"Failed to adapt clip '{clip_name}'. Using the cut clip without adaptation.")
                # If adaptation fails, we still use the cut clip
            else:
                current_clip_path = temp_adapted_path # Update path to the adapted clip
        
        # 3. Final export/copy to the base output directory
        final_output_path = os.path.join(output_base_dir, f"{clip_name}.mp4")
        print(f"Exporting final clip '{clip_name}' to '{final_output_path}'...")
        try:
            shutil.copy2(current_clip_path, final_output_path)
            print(f"Final clip '{clip_name}' successfully saved.")
        except Exception as e:
            print(f"Error saving final clip '{clip_name}' to '{final_output_path}': {e}")
            
        # Clean up temporary files
        if os.path.exists(temp_cut_path):
            os.remove(temp_cut_path)
        if os.path.exists(temp_adapted_path):
            os.remove(temp_adapted_path)

    # Clean up the temporary directory for processed clips if it's empty
    if not os.listdir(processed_clips_temp_dir):
        os.rmdir(processed_clips_temp_dir)
    elif not os.listdir(processed_clips_temp_dir) and os.path.exists(processed_clips_temp_dir):
        # This check implies that if it's not empty, we leave it. This needs refinement if
        # we want to ensure full cleanup even with partial failures.
        pass # Keep temp dir if not empty (e.g., if some clips failed)

    print("\n--- Orchestration complete ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrates video clip processing (cut, adapt, export).")
    parser.add_argument("input_video", type=str, help="Path to the source video file.")
    parser.add_argument("timestamps_file", type=str, help="Path to a JSON file containing clip timestamps. Format: [{'start': 0.0, 'end': 10.0, 'name': 'intro'}, ...]")
    parser.add_argument("output_base_dir", type=str, help="Base directory to save all processed clips.")
    parser.add_argument("--resolution", type=str, help="Optional: Target resolution for adapted clips (e.g., '1280x720').")
    parser.add_argument("--fps", type=int, help="Optional: Target frame rate for adapted clips (e.g., 25, 30).")

    args = parser.parse_args()

    orchestrate_clips(args.input_video, args.timestamps_file, args.output_base_dir, args.resolution, args.fps)
