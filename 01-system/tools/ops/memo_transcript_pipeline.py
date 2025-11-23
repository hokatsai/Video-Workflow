
import argparse
import os
import sys

# Add project root to Python path to allow for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from tools.llms.gemini.gemini import generate_text

def create_transcript_memo(input_file, output_file, prompt_template=None, title="Meeting Memo"):
    """
    Creates a formatted Markdown memo from a transcript file using an AI model.

    Args:
        input_file (str): Path to the input text file (transcript).
        output_file (str): Path to save the output Markdown file.
        prompt_template (str): A string containing '{content}' to be replaced by the transcript content.
        title (str): The title for the memo.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'")
        return

    try:
        print(f"Reading transcript from: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if prompt_template:
            final_prompt = prompt_template.format(content=content)
        else:
            # Default prompt for creating a meeting memo from a transcript
            final_prompt = (
                f"Please act as a professional secretary summarizing a meeting. Based on the following transcript, generate a concise and clear meeting memo in Markdown format. "
                f"The memo should identify and include the following sections if possible: \n"
                f"1. **Attendees**: List of participants mentioned.\n"
                f"2. **Key Discussion Points**: A summary of the main topics discussed.\n"
                f"3. **Action Items**: A clear list of tasks, who is responsible, and any deadlines mentioned.\n"
                f"4. **Decisions Made**: A summary of any conclusions or decisions reached.\n\n"
                f"Here is the raw transcript:\n\n---\n\n{content}"
            )
        
        print("Sending prompt to Gemini API to generate memo...")
        ai_response = generate_text(final_prompt)

        if ai_response.startswith("Error:"):
            print(f"Failed to generate memo: {ai_response}")
            return
            
        final_md_content = f"# {title}\n\n{ai_response}"

        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        print(f"Writing AI-generated memo to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_md_content)
            
        print("Memo generation complete.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an AI-powered meeting memo from a transcript file.")
    parser.add_argument("input_file", type=str, help="Path to the input transcript file.")
    parser.add_argument("output_file", type=str, help="Path for the output Markdown memo file.")
    parser.add_argument("--prompt_file", type=str, help="Optional: Path to a text file containing a custom prompt. Use '{content}' as a placeholder.")
    parser.add_argument("--title", type=str, default="Meeting Memo", help="Title for the memo.")

    args = parser.parse_args()

    custom_prompt = None
    if args.prompt_file:
        if os.path.exists(args.prompt_file):
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                custom_prompt = f.read()
        else:
            print(f"Warning: Prompt file '{args.prompt_file}' not found. Using default prompt.")

    create_transcript_memo(args.input_file, args.output_file, custom_prompt, args.title)
