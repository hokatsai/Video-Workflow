# Video Workflow Automation System

This project provides an automated, menu-driven workflow for downloading and processing video files. The entire system is controlled by a single script.

## Quick Start Guide

### 1. One-Time Setup (or when cookies expire)

Before the first run, or whenever downloads start failing due to authentication, you need to refresh your login session.

- **Run the Login Script:** Open a PowerShell terminal and execute the following command:
  ```powershell
  .\tools\cookie\open-browser-profile.ps1
  ```
- **Log In:** A special, independent Chrome browser window will open. **Log in to your Google/YouTube account in this window**.
- **Close:** Once logged in, you can simply close the browser window.

This session will be saved locally within the project and will be used automatically for many weeks or months.

### 2. Run the Main Workflow

Whenever you want to process a video, just run the master script:

1.  **Open PowerShell** in the project's root directory.
2.  **Execute the script:**
    ```powershell
    .\Start-Workflow.ps1
    ```
3.  **Follow the Menu:** A menu will appear. Simply enter the number for the task you wish to perform (e.g., `4` for the full "Download & Transcribe" workflow) and follow the prompts.

---

## How It Works

The `Start-Workflow.ps1` script is a master controller that calls other specialized scripts located in `01-system/tools/ops/video-workflow/cookie/`. This system is designed to be robust and easy to use. All outputs are automatically saved and organized in the `03-outputs` directory.
