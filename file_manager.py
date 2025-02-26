import os
import shutil


# Define root and raw folder paths
root_folder = "path to main fodler"
raw_folder = "path to raw folder"

# Get the list of all files and directories in the raw_folder
files_and_dirs = os.listdir(raw_folder)

# Initialize a counter for subfolder naming
counter = 1

# Iterate through all files and directories in the raw folder
for item in files_and_dirs:
    item_path = os.path.join(raw_folder, item)
    
    # Check if the item is an .html file
    if item.endswith(".html"):
        # Find the corresponding folder with the same name as the html file (excluding the extension)
        corresponding_folder = os.path.splitext(item)[0]+ "_files"
        folder_path = os.path.join(raw_folder, corresponding_folder)

        # Check if the corresponding folder exists
        if os.path.exists(folder_path):
            try:
                # Create a new subfolder in the root folder (p1, p2, p3, ...)
                new_subfolder = f"p{counter}"
                new_subfolder_path = os.path.join(root_folder, new_subfolder)
                
                # Create the new subfolder if it does not exist
                if not os.path.exists(new_subfolder_path):
                    os.makedirs(new_subfolder_path)
                    print(f"Created subfolder: {new_subfolder_path}")
                else:
                    print(f"Subfolder already exists: {new_subfolder_path}")
                
                # Move the html file and corresponding folder into the new subfolder
                html_dest = os.path.join(new_subfolder_path, item)
                folder_dest = os.path.join(new_subfolder_path, corresponding_folder)
                
                shutil.move(item_path, html_dest)
                shutil.move(folder_path, folder_dest)
                
                # Increment the counter for the next subfolder
                counter += 1
                print(f"Moved {item} and {corresponding_folder} to {new_subfolder_path}")
            except Exception as e:
                print(f"Error occurred while processing {item}: {e}")
        else:
            print(f"Corresponding folder not found for {item}: {folder_path}")

