import os
import sys
import tarfile
import zipfile
#filename = sys.argv[1]
def extract_zip(filename):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(os.path.splitext(filename)[0])
        print("Extracted:", filename)
def extract_tar(filename):
    if filename.endswith(".tar"):
      with tarfile.open(filename, "r") as tar:
        tar.extractall(os.path.splitext(filename)[0])
        print("Extracted:", filename)
    else:
      with tarfile.open(filename, "r:gz") as tar:
        tar.extractall(os.path.splitext(filename)[0])
        print("Extracted:", filename)
def extract_and_remove(filename):
    if filename.endswith(".zip"):
        extract_zip(filename)
    elif filename.endswith("gz") or filename.endswith(".tar") :
        extract_tar(filename)
    else:
        print("File format not supported.")
    os.remove(filename)
    print("Removed:", filename)
def extract_all_archives(path):
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            if full_path.endswith(".zip") or full_path.endswith("gz") or full_path.endswith(".tar"):
                extract_and_remove(full_path)
                print(full_path)
                extract_all_archives(os.path.splitext(full_path)[0])
def search_for_file(path, file_name):
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            if item == file_name:
                print("Found:", full_path)
                return True
        elif os.path.isdir(full_path):
            if search_for_file(full_path, file_name):
                return True
    return False
def  extract_file(filename):
    extract_and_remove(filename)
    extract_all_archives(os.path.splitext(filename)[0])
# if search_for_file(os.path.splitext(filename)[0], "cmm-provisioning.yaml"):
#     print("cmm-provisioning.yaml found.")
# else:
#     print("cmm-provisioning.yaml not found.")