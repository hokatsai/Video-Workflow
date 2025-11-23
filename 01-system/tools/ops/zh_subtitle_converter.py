
import argparse
import os
import sys
import pysrt
from opencc import OpenCC

def convert_subtitle_language(input_file, output_file, config):
    """
    Converts the language of a subtitle file between Simplified and Traditional Chinese.

    Args:
        input_file (str): Path to the input SRT file.
        output_file (str): Path to save the converted SRT file.
        config (str): Conversion configuration. 's2t' for Simplified to Traditional,
                      't2s' for Traditional to Simplified.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'")
        return

    # Map user-friendly config to OpenCC's config file names
    config_map = {
        "s2t": "s2t",  # Simplified to Traditional
        "t2s": "t2s"   # Traditional to Simplified
    }
    
    if config not in config_map:
        print(f"Error: Invalid config '{config}'. Choose from 's2t' or 't2s'.")
        return
        
    try:
        print(f"Initializing OpenCC with config: {config}")
        cc = OpenCC(config_map[config])
        
        print(f"Loading subtitles from: {input_file}")
        subs = pysrt.open(input_file, encoding='utf-8')

        print(f"Converting text from {config}...")
        for sub in subs:
            sub.text = cc.convert(sub.text)

        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        subs.save(output_file, encoding='utf-8')

        print(f"Conversion complete. Converted subtitles saved to: {output_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Chinese subtitles between Simplified and Traditional.")
    parser.add_argument("input_file", type=str, help="Path to the input SRT subtitle file.")
    parser.add_argument("output_file", type=str, help="Path for the converted output SRT file.")
    parser.add_argument("config", type=str, choices=['s2t', 't2s'], help="Conversion configuration: 's2t' (Simplified to Traditional) or 't2s' (Traditional to Simplified).")

    args = parser.parse_args()

    convert_subtitle_language(args.input_file, args.output_file, args.config)
