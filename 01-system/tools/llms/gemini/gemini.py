
import os
import google.generativeai as genai

def get_gemini_api_key():
    """
    Reads the Gemini API key from the designated API-Keys.md file.
    This function adheres to the project's convention for key management.
    """
    try:
        # Construct a path relative to this script's location
        # Assumes this script is in 01-system/tools/llms/gemini/
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        api_keys_path = os.path.join(base_path, 'configs', 'apis', 'API-Keys.md')

        with open(api_keys_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.strip().split('=')[1]
        return None
    except FileNotFoundError:
        print(f"Error: API key file not found at '{api_keys_path}'")
        return None
    except Exception as e:
        print(f"An error occurred while reading the API key: {e}")
        return None

def generate_text(prompt: str, model_name: str = "gemini-2.5-pro"):
    """
    Generates text using the specified Gemini model.

    Args:
        prompt (str): The text prompt to send to the model.
        model_name (str): The name of the model to use (e.g., "gemini-pro").

    Returns:
        str: The generated text, or an error message if something went wrong.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return "Error: Gemini API key not found or could not be read."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during Gemini API call: {e}"

if __name__ == '__main__':
    # Example of how to use this module
    # This part is for testing and will not run when imported by other scripts.
    print("Running a test generation...")
    
    test_prompt = "Explain the importance of virtual environments in Python in one sentence."
    generated_text = generate_text(test_prompt)
    
    print(f"\nPrompt: {test_prompt}")
    print(f"Gemini: {generated_text}")
    
    # Verify that the key function works
    # key = get_gemini_api_key()
    # if key:
    #     print("\nSuccessfully retrieved API key.")
    # else:
    #     print("\nFailed to retrieve API key.")
