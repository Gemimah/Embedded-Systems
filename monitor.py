import os
import time
import requests

# Configuration
FOLDER_PATH = r"C:\Users\pc\OneDrive\Pictures\New folder (2)"  # Replace with your folder path
UPLOAD_URL = "https://projects.benax.rw/?id=338"  # Replace with your upload URL
UPLOAD_INTERVAL = 30  # Interval in seconds

def upload_file(file_path):
    """Uploads a file to the server and deletes it if successful."""
    try:
        with open(file_path, 'rb') as file:
            files = {'imageFile': file}
            response = requests.post(UPLOAD_URL, files=files)
            
        # Check response status
        if response.status_code == 200:
            print(f"Uploaded: {file_path}")
            os.remove(file_path)
        else:
            print(f"Failed to upload {file_path}. Server responded with status code: {response.status_code}")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

def monitor_and_upload():
    """Monitors the folder and uploads files at regular intervals."""
    while True:
        # Get all files in the folder
        files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f))]
        
        # Upload each file
        for file_path in files:
            upload_file(file_path)
        
        # Wait before the next check
        time.sleep(UPLOAD_INTERVAL)

if __name__ == "__main__":
    print("Starting folder monitoring and uploading...")
    monitor_and_upload()
