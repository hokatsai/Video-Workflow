
import argparse
import os
import sys
import subprocess
import tempfile

def run_tool(script_path, *args):
    """Helper function to run other tools as subprocesses."""
    command = [sys.executable, script_path] + list(args)
    print(f"Executing: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8')
    
    if result.returncode != 0:
        print(f"Error running {os.path.basename(script_path)}:")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        return False
    return True

def subtitle_pipeline(input_file, output_file, corrector_prompt=None, refiner_prompt=None):
    """
    Runs a full subtitle correction and refinement pipeline.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Get absolute paths to the tool scripts
    current_script_dir = os.path.dirname(__file__)
    corrector_script = os.path.join(current_script_dir, 'subtitle_corrector.py')
    refiner_script = os.path.join(current_script_dir, 'subtitle_line_refiner.py')

    # Create a temporary file for the intermediate (corrected) subtitles
    with tempfile.NamedTemporaryFile(suffix="_corrected.srt", delete=False, mode='w+', encoding='utf-8') as temp_file:
        temp_corrected_path = temp_file.name

    try:
        # Step 1: Correct subtitles
        print("\n--- Step 1: Running Subtitle Corrector ---")
        corrector_args = [input_file, temp_corrected_path]
        if corrector_prompt:
            corrector_args.extend(["--prompt_file", corrector_prompt])
        
        if not run_tool(corrector_script, *corrector_args):
            print("Subtitle correction failed. Aborting pipeline.")
            return

        # Step 2: Refine the corrected subtitles
        print("\n--- Step 2: Running Subtitle Refiner ---")
        refiner_args = [temp_corrected_path, output_file]
        if refiner_prompt:
            refiner_args.extend(["--prompt_file", refiner_prompt])

        if not run_tool(refiner_script, *refiner_args):
            print("Subtitle refinement failed.")
            return

        print(f"\nPipeline complete. Final subtitles saved to: {output_file}")

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_corrected_path):
            os.remove(temp_corrected_path)
            print(f"Cleaned up temporary file: {temp_corrected_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full pipeline to correct and refine subtitles.")
    parser.add_argument("input_file", type=str, help="Path to the initial SRT subtitle file.")
    parser.add_argument("output_file", type=str, help="Path for the final, refined output SRT file.")
    parser.add_argument("--corrector_prompt", type=str, help="Optional: Path to a custom prompt file for the correction step.")
    parser.add_argument("--refiner_prompt", type=str, help="Optional: Path to a custom prompt file for the refinement step.")

    args = parser.parse_args()

    subtitle_pipeline(args.input_file, args.output_file, args.corrector_prompt, args.refiner_prompt)
