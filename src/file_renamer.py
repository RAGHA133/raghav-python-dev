import os

def rename_files(folder_path, prefix):
    try:
        files = os.listdir(folder_path)
        for index, filename in enumerate(files):
            extension = os.path.splitext(filename)[1]
            new_name = f"{prefix}_{index+1}{extension}"
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    folder = input("Enter the folder path to rename files: ").strip()
    prefix = input("Enter the prefix for renamed files: ").strip()
    rename_files(folder, prefix)
