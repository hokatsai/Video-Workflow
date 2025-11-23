# Playbook: Gemini Core Module

**Purpose:** This is not a directly callable tool. It is a core Python module that provides other tools with the ability to interact with the Google Gemini API.

**How to Use (for other Python scripts):**

1.  **Import the function:**
    ```python
    # Make sure '01-system' is in the Python path
    from tools.llms.gemini.gemini import generate_text
    ```
2.  **Call the function:**
    ```python
    my_prompt = "Summarize this for me: [some long text]"
    summary = generate_text(my_prompt)
    print(summary)
    ```

**Configuration:**
This module automatically reads the `GEMINI_API_KEY` from the `01-system/configs/apis/API-Keys.md` file, following the project's security conventions.
