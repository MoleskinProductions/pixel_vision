import os
import csv
import json

def to_csv(text_list, filename):
    """Writes each text element from text_list into a separate row of a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Optionally, write a header
        writer.writerow(['Text'])
        for text in text_list:
            writer.writerow([text])
    print(f"Data written to {filename}")

def from_csv(filename):
    """Reads the CSV file and returns a list of text elements."""
    texts = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # Skip header if present
        header = next(reader, None)
        for row in reader:
            if row:
                texts.append(row[0])
    return texts

def find_subdirectory(parent_dir, subdir_name):
  
    if not os.path.isdir(parent_dir):
        raise FileNotFoundError(f"The specified parent directory '{parent_dir}' does not exist or is not a directory.")

    # Join the parent directory with the subdirectory name
    potential_subdir = os.path.join(parent_dir, subdir_name)

    if os.path.isdir(potential_subdir):
        return potential_subdir
    else:
        return None

def get_files_in_subdirectories(parent_dir):

    if not os.path.isdir(parent_dir):
        raise FileNotFoundError(f"The specified parent directory '{parent_dir}' does not exist or is not a directory.")

    files_dict = {}

    for subdir_name in os.listdir(parent_dir):
        subdir_path = os.path.join(parent_dir, subdir_name)
        if os.path.isdir(subdir_path):
            files = [os.path.join(subdir_path, file) for file in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, file))]
            files_dict[subdir_name] = files

    return files_dict

def filetype_dict(directory, filetypes):
    files = [ x for x in os.listdir(directory) ]
    out_dict = {}
    for ft in filetypes:
        in_dict = { x : os.path.join(directory, x) for x in files if x.endswith(ft) }
        out_dict = { **out_dict, **in_dict}
    return out_dict


def list_dir(directory, as_dict=0):
   
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The specified directory '{directory}' does not exist or is not a directory.")

    entries = os.listdir(directory)

    if as_dict:
        return {entry: os.path.join(directory, entry) for entry in entries}
    else:
        return entries

def contains_filetypes(directory, filetypes, recursive=1):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The specified directory '{directory}' does not exist or is not a directory.")

    if isinstance(filetypes, str):
        filetypes = [filetypes]

    if recursive==1 :
        for _, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ft) for ft in filetypes):
                    return True
    else:
        for file in os.listdir(directory):
                if any(file.endswith(ft) for ft in filetypes):
                    return True


    return False

