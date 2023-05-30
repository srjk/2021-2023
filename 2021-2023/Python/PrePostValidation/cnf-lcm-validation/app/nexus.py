import requests
import os
from app.modules import *
from app.extract_file import extract_file
def download_file(url,destination_path):
    try:
        username = 'admin'
        password = 'Dish@123'
        host=os.environ.get('NEXUS_SERVICE')
        url = host+'/repository/nflcm/'+ str(url)
        # Perform GET request with authentication
        response = requests.get(url, auth=(username, password), verify=False)
        response.raise_for_status()
        file_without_path = os.path.basename(url)

        # Split the file name into parts based on '.'
        ext_parts = file_without_path.split('.')

        # Extract the extension
        ext = ext_parts[-1] if ext_parts else ''
        print(ext)
        destination_path="/tmp/"+destination_path+ "." +ext
        # Save the file to the specified destination path
        with open(destination_path, 'wb') as file:
            file.write(response.content)

        print("File downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while downloading the file: {e}")
    
    extract_file(destination_path)


    return True
