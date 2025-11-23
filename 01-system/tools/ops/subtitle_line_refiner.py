
import argparse
import os
import sys
import pysrt
import re

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from tools.llms.gemini.gemini import generate_text

def refine_subtitles(input_file, output_file, prompt_template=None):
    """
    Refines the style and flow of a subtitle file using an AI model.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'")
        return

    try:
        print(f"Loading subtitles from: {input_file}")
        subs = pysrt.open(input_file)

        # Prepare the text block for the AI
        original_text_block = ""
        for i, sub in enumerate(subs):
            original_text_block += f"{i + 1}: {sub.text}\n"

        if prompt_template:
            final_prompt = prompt_template.format(content=original_text_block)
        else:
            # Default prompt for refining subtitle flow and readability
            final_prompt = (
                "You are an expert subtitle editor. Your goal is to improve the readability and flow of the following numbered subtitle lines. "
                "Focus on:\n"
                "1. Breaking long or complex sentences into shorter, more digestible lines.\n"
                "2. Simplifying complex vocabulary for a general audience.\n"
                "3. Ensuring a natural, conversational tone.\n\n"
                "Your response should ONLY contain the refined text, prefixed with the original line number. "
                "Do not add any extra explanations or commentary. Maintain the exact number of lines.\n\n"
                "---\n"
                f"{original_text_block}"
                "---\n"
            )

        print("Sending subtitles to Gemini API for refinement...")
        ai_response = generate_text(final_prompt)

        if ai_response.startswith("Error:"):
            print(f"Failed to refine subtitles: {ai_response}")
            return
        
        print("Parsing AI response and updating subtitles...")
        corrected_lines = {}
        for line in ai_response.split('\n'):
            match = re.match(r"^\s*(\d+):\s*(.*)", line)
            if match:
                index = int(match.group(1))
                text = match.group(2).strip()
                corrected_lines[index] = text
        
        updated_count = 0
        for i, sub in enumerate(subs):
            sub_index = i + 1
            if sub_index in corrected_lines:
                sub.text = corrected_lines[sub_index]
                updated_count += 1
        
        print(f"Refined {updated_count} out of {len(subs)} subtitle entries.")

        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        subs.save(output_file, encoding='utf-8')

        print(f"Refined subtitles saved to: {output_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refine subtitles for better readability using an AI model.")
    parser.add_argument("input_file", type=str, help="Path to the input SRT subtitle file.")
    parser.add_argument("output_file", type=str, help="Path for the refined output SRT file.")
    parser.add_argument("--prompt_file", type=str, help="Optional: Path to a text file with a custom prompt. Use '{content}' as a placeholder.")

    args = parser.parse_args()

    custom_prompt = None
    if args.prompt_file:
        if os.path.exists(args.prompt_file):
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                custom_prompt = f.read()
        else:
            print(f"Warning: Prompt file '{args.prompt_file}' not found. Using default prompt.")

    refine_subtitles(args.input_file, args.output_file, custom_prompt)
