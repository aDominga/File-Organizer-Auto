import os
import sys
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import pathlib

# Define the parent directory where year-based subdirectories will be created
user_input = input("Enter directory path: ")
parent_directory = str(user_input)

# Loop to check if year folders exist
today = datetime.date.today()
year = today.year

for counter in range(2020, year + 1):
    STRcounter = str(counter)
    folderYr = os.path.join(parent_directory, STRcounter)
    
    # Create year folder if it doesn't exist
    if not os.path.exists(folderYr):
        os.mkdir(folderYr)

# List of directories and files
entries = os.listdir(parent_directory)

def organize_existing():
    for entry in entries:
        file_path = os.path.join(parent_directory, entry)
        if not os.path.isdir(file_path):
            FileOrganizerEventHandler().organize_file(file_path)



# Goes through list of entries
for entry in entries:
    entry_path = os.path.join(parent_directory, entry)
    
    # Checks if the entry path is real and then makes the entry the year_folder and adds the subfolders
    if os.path.isdir(entry_path):
        year_folder = os.path.join(parent_directory, entry)
        imagesDIR = os.path.join(year_folder, "Images-Gifs")
        codeDIR = os.path.join(year_folder, "Code")
        appDIR = os.path.join(year_folder, "Apps")
        documentsDIR = os.path.join(year_folder, "Documents")
        zipDIR = os.path.join(year_folder, "Zipfiles")
        otherDIR = os.path.join(year_folder, "Other")

        os.makedirs(imagesDIR, exist_ok=True)
        os.makedirs(codeDIR, exist_ok=True)
        os.makedirs(appDIR, exist_ok=True)
        os.makedirs(documentsDIR, exist_ok=True)
        os.makedirs(zipDIR, exist_ok=True)
        os.makedirs(otherDIR, exist_ok=True)

class FileOrganizerEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        if file_path.endswith(".crdownload"): 
            return

        self.organize_file(file_path)



    def organize_file(self, file_path):
        # Determine the file's type based on its extension
        file_extension = pathlib.Path(file_path).suffix.lower()

        # Determine the file's creation timestamp
        create_timestamp = os.stat(file_path).st_birthtime
        create_date = datetime.datetime.fromtimestamp(create_timestamp)
        year = create_date.strftime('%Y')

        # Define destination directories based on file type
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
        doc_extensions = ('.docx', '.pdf', '.txt')
        code_extensions = ('.java', '.py', '.html', '.xml')
        app_extensions = ('.app','.dmg')
        zip_extensions = ('.zip')

        if file_extension in image_extensions:
            folder_name = "Images-Gifs"
        elif file_extension in doc_extensions:
            folder_name = "Documents"
        elif file_extension in code_extensions:
            folder_name = "Code"
        elif file_extension in app_extensions:
            folder_name = "Apps"
        elif file_extension in zip_extensions:
            folder_name = "Zipfiles"
        else:
            folder_name = "Other"

        # Move the file to the appropriate destination directory
        destination_dir = os.path.join(parent_directory, year, folder_name)
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_dir, file_name)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        
        if not os.path.exists(destination_path):
            shutil.move(file_path, destination_path)


# class FileOrganizerEventHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if event.is_directory:
#             return
#         self.organize_file(event.src_path)

#     def organize_file(self, file_path):
#         # Determine the file's type based on its extension
#         file_extension = pathlib.Path(file_path).suffix.lower()
#         logging.info(f"File extension: {file_extension}")

#         # Determine the file's creation timestamp
#         create_timestamp = os.stat(file_path).st_birthtime
#         create_date = datetime.datetime.fromtimestamp(create_timestamp)
#         year = create_date.strftime('%Y')
#         logging.info(f"File creation year: {year}")

        # ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    organize_existing()

    event_handler = FileOrganizerEventHandler()

    observer = Observer()

    observer.schedule(event_handler, parent_directory, recursive=False)

    observer.start()

    time.sleep(30)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
