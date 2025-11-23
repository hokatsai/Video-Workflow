
import argparse
import os

def create_handout(input_file, output_file, title="Lecture Handout"):
    """
    Creates a formatted Markdown handout from a plain text file.

    Args:
        input_file (str): Path to the input plain text file (e.g., a transcript).
        output_file (str): Path to save the output Markdown file.
        title (str): The title for the handout.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at '{input_file}'")
        return

    try:
        print(f"Reading content from: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple formatting: wrap content in a Markdown structure
        md_content = f"# {title}\n\n"
        md_content += "## Lecture Content\n\n"
        # Simple paragraph formatting
        paragraphs = [f"{p.strip()}\n" for p in content.split('\n') if p.strip()]
        md_content += "\n".join(paragraphs)
        md_content += "\n\n## Notes\n\n"
        md_content += "*(Add your notes here)*\n"

        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)

        print(f"Writing Markdown handout to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print("Handout creation complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Markdown handout from a text file.")
    parser.add_argument("input_file", type=str, help="Path to the input text file.")
    parser.add_argument("output_file", type=str, help="Path for the output Markdown file.")
    parser.add_argument("--title", type=str, default="Lecture Handout", help="Title for the handout.")

    args = parser.parse_args()

    create_handout(args.input_file, args.output_file, args.title)
