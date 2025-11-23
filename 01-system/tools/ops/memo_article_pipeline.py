
import argparse
import os
import sys

# Add project root to Python path to allow for absolute imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from tools.llms.gemini.gemini import generate_text

def create_memo_article(input_file, output_file, prompt_template=None, title="Memo Article"):
    """
    Creates a formatted Markdown article from a text file using an AI model.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path to save the output Markdown file.
        prompt_template (str): A string containing '{content}' to be replaced by the file's content.
        title (str): The title for the article.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'")
        return

    try:
        print(f"Reading content from: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if prompt_template:
            final_prompt = prompt_template.format(content=content)
        else:
            # Default prompt for creating an article
            final_prompt = (
                f"Please act as a skilled editor. Convert the following raw text into a well-structured and polished article in Markdown format. "
                f"The article should have a clear introduction, a body with logical paragraphs and headings, and a concluding summary.\n\n"
                f"Here is the raw text:\n\n---\n\n{content}"
            )
        
        print("Sending prompt to Gemini API to generate article...")
        ai_response = generate_text(final_prompt)

        if ai_response.startswith("Error:"):
            print(f"Failed to generate article: {ai_response}")
            return
            
        final_md_content = f"# {title}\n\n{ai_response}"

        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        print(f"Writing AI-generated article to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_md_content)
            
        print("Article generation complete.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an AI-powered Markdown article from a text file.")
    parser.add_argument("input_file", type=str, help="Path to the input text file.")
    parser.add_argument("output_file", type=str, help="Path for the output Markdown file.")
    parser.add_argument("--prompt_file", type=str, help="Optional: Path to a text file containing a custom prompt template. Use '{content}' as a placeholder.")
    parser.add_argument("--title", type=str, default="AI-Generated Article", help="Title for the article.")

    args = parser.parse_args()

    custom_prompt = None
    if args.prompt_file:
        if os.path.exists(args.prompt_file):
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                custom_prompt = f.read()
        else:
            print(f"Warning: Prompt file '{args.prompt_file}' not found. Using default prompt.")

    create_memo_article(args.input_file, args.output_file, custom_prompt, args.title)
