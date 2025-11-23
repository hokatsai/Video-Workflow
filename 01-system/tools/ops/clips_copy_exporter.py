
import argparse
import os
import shutil

def export_clips(source_path, destination_path, move=False):
    """
    Copies or moves a file or all files in a directory to a destination.

    Args:
        source_path (str): Path to the source file or directory.
        destination_path (str): Path to the destination directory.
        move (bool): If True, move the files instead of copying.
    """
    if not os.path.exists(source_path):
        print(f"Error: Source path '{source_path}' not found.")
        return

    if not os.path.exists(destination_path):
        print(f"Destination directory '{destination_path}' not found. Creating it.")
        os.makedirs(destination_path)

    action = "Moving" if move else "Copying"
    action_func = shutil.move if move else shutil.copy2

    try:
        if os.path.isdir(source_path):
            files_to_process = [os.path.join(source_path, f) for f in os.listdir(source_path)]
            print(f"{action} all {len(files_to_process)} files from '{source_path}' to '{destination_path}'...")
        else:
            files_to_process = [source_path]
            print(f"{action} file '{source_path}' to '{destination_path}'...")

        for f in files_to_process:
            action_func(f, destination_path)
        
        print("Export complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy or move video clips to an export directory.")
    parser.add_argument("source_path", type=str, help="The source file or directory to export from.")
    parser.add_argument("destination_path", type=str, help="The destination directory to export to.")
    parser.add_argument("--move", action="store_true", help="Move the files instead of copying them.")

    args = parser.parse_args()

    export_clips(args.source_path, args.destination_path, args.move)
