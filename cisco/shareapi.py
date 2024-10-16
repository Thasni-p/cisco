import os
import time
import base64
import requests
import json


directory_path = r'F:\My Project\file_Share_api\csv_file'  # Update this to your directory path
base_url = 'http://45.8.150.131:8000'
url = f'{base_url}/api/method/cisco.api.upload_cdr_file_csv' # API endpoint
API_KEY = 'c4bc9ce3b122462'
API_SECRET = '0455723ffecde0d'
interval = 10   # Interval in seconds to check for new files

def send_file_and_delete(file_path, url, interval):
    # Open the file in binary mode
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as file:
        encoded_file = base64.b64encode(file.read()).decode('utf-8')
        file.close()
        # Set up the headers if needed (e.g., for authorization)
        headers = {
            'Authorization': "token "+ API_KEY + ":" + API_SECRET,
            'Content-Type': 'application/json',
        }
        
        # Send the file via POST request
        payload = json.dumps({
            'fname': file_name,
            'csv_file': encoded_file
        })

        response = requests.post(url, data=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            res = response.json()
            call_payload = res.get("message", {})
            if call_payload.get('status') == 'success':
                print(f"File '{file_path}' uploaded successfully.")
                try:
                    # Delete the file from the system
                    time.sleep(2)
                    os.remove(file_path)
                    print(f"File '{file_path}' deleted from the system.")
                except PermissionError as e:
                    print(f"Failed to delete file '{file_path}'. Error: {e}")
            else:
                print(f"Failed to upload file '{file_path}'. Error: {call_payload.get('message')}")
        else:
            print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")
            print(response.text)

def monitor_directory(directory_path, url, api_key=None, interval=10):
    # while True:
        # List all CSV files in the directory
    files = [f for f in os.listdir(directory_path) if f.lower().endswith('.csv') and os.path.isfile(os.path.join(directory_path, f))]
    
    # Process each CSV file
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        print(f"Found CSV file: {file_path}")
        # Send the file through the API and delete after successful upload
        send_file_and_delete(file_path, url, api_key)
        
        # Wait for the specified interval before checking again
        # time.sleep(interval)


monitor_directory(directory_path, url, interval)
