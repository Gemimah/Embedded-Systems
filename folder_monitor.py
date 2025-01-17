import os
import time
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define paths
WATCH_FOLDER = r"C:\Users\pc\OneDrive\Pictures\New folder (2)"
UPLOADED_FOLDER = r"C:\Users\pc\OneDrive\Pictures\New folder (2)"
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php" 

# Ensure the uploaded folder exists
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

class UploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            self.handle_file(event.src_path)

    def handle_file(self, file_path):
        print(f"New file detected: {file_path}")
        time.sleep(30)  
        
        try:
            
            print(f"Uploading {file_path}...")
            result = subprocess.run(
                ["curl", "-X", "POST", "-F", f"file=@{file_path}", UPLOAD_URL],
                capture_output=True, text=True
            )

            # Check if the upload was successful
            if result.returncode == 0:
                print(f"Successfully uploaded {file_path}. Moving to uploaded folder.")
                # Move the file to the uploaded folder
                shutil.move(file_path, os.path.join(UPLOADED_FOLDER, os.path.basename(file_path)))
            else:
                print(f"Failed to upload {file_path}. Error: {result.stderr}")
        except Exception as e:
            print(f"Error handling file {file_path}: {e}")

if __name__ == "__main__":
    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    
    print(f"Monitoring folder: {WATCH_FOLDER}")
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the folder monitor.")
        observer.stop()
    observer.join()
