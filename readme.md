# File Manager Script

This script automatically organizes files into designated directories based on their file types (audio, video, image, and documents) in a specified source directory. 
It leverages the `watchdog` library to monitor changes in the source directory and move files accordingly.

## Features

- Automatically moves audio files to a specified music or SFX folder.
- Organizes video files into a designated video directory.
- Sorts image files into a specific images folder.
- Places documents into a dedicated documents directory.
- Supports unique file naming to avoid overwriting.

## Dependencies

- Python 3.x
- `watchdog` library

## Installation

1. Clone this repository or download the script.
2. Install the required dependencies. You can use `pip` to install the `watchdog` library:

   ```bash
   pip install watchdog

## Configure dirs

source_dir = "C:\\Users\\UserName\\Downloads"
dest_dir_sfx = "C:\\Users\\UserName\\Documents\\SFX"
dest_dir_music = "C:\\Users\\UserName\\Documents\\Music"
dest_dir_video = "C:\\Users\\UserName\\Documents\\Videos"
dest_dir_image = "C:\\Users\\UserName\\Documents\\Images"
dest_dir_documents = "C:\\Users\\UserName\\Documents\\Documents"


## Run the script

     ```bash
    py index.py

