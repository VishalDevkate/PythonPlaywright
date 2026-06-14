import inspect
from pathlib import Path


def screenshot_path():
    # 1. Get the frame of the function that called this utility
    # inspect.stack()[1] gets the immediate caller's frame information
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename

    # 2. Resolve the directory of that calling test file
    calling_file_dir = Path(caller_filename).resolve().parent

    # 3. Define the exact screenshot target folder relative to the caller
    SCREENSHOT_DIR = calling_file_dir / "screenshots"

    # 4. Create the directory automatically if it doesn't exist yet
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    return SCREENSHOT_DIR