import os
import zipfile

# Path to the directory containing the zip files
zip_folder = '/home/user/Downloads/flag3000.zip'

# Path to the destination folder where the extracted files will be saved
destination_folder = '/home/user/Downloads/zipdir/'

# Get a list of all the zip files in the zip folder

# Iterate over each file in the zip folder
    # Construct the full path to the current file
file_path = '/home/user/Downloads/flag3000.zip'
for i in range (2999, 0, -1):
    file_path = '/home/user/Downloads/zipdir/flag' + str(i) + '.zip'
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
        
for i in range (0, 3000):
    os.remove("/home/user/Downloads/zipdir/flag" + str(i) + ".zip")
