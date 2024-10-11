from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ! FILL IN BELOW


# ? folder to track e.g. Windows: "C:\\Users\\UserName\\Downloads"
source_dir = f"C:\\Users\\dir_to_be_monitered"

# the directories of corresponding segregated directories
dest_dir_sfx = f"C:\\Users\\sfx_dest"
dest_dir_music = f"C:\\Users\\music"
dest_dir_video = f"C:\\Users\\video_dest"
dest_dir_image = f"C:\\Users\\image_dest"
dest_dir_documents = f"C:\\Users\\document_dest"

# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions

    # the problem with below functino is that is assumes that the src dir will always be empty hence it loops through all of them,but we need only the recently downloaded file to be moved into a new destination. so below is the modified code

    # def on_modified(self, event):
    #     with scandir(source_dir) as entries:
    #         for entry in entries:
    #             name = entry.name
    #             self.check_audio_files(entry, name)
    #             self.check_video_files(entry, name)
    #             self.check_image_files(entry, name)
    #             self.check_document_files(entry, name)

    def on_modified(self, event):
        if event.is_directory:  # Ignore directory modifications
            return
        
        most_recent_file = None
        most_recent_time = 0

        with scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():  # Process only files
                    # Get the last modified time
                    modified_time = entry.stat().st_mtime
                    
                    # Check if this file is the most recently modified one
                    if modified_time > most_recent_time:
                        most_recent_time = modified_time
                        most_recent_file = entry

        # If we found a most recent file, move it
        if most_recent_file:
            name = most_recent_file.name
            
            # Check the file type and move it accordingly
            self.check_audio_files(most_recent_file, name)
            self.check_video_files(most_recent_file, name)
            self.check_image_files(most_recent_file, name)
            self.check_document_files(most_recent_file, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        print("Script Started")
        while True:
            sleep(10)
    except KeyboardInterrupt:
        print("Script Terminated")
        observer.stop()
    observer.join()