import os
import hashlib
import shutil
from pydotenvs import load_env


def ignore_dir(file_path: str) -> bool:
    """Checks if a file path should be ignored based on IGNORE_DIRS."""
    for _dir in IGNORE_DIRS:
        if _dir in file_path:
            return True
    return False


def get_file_path(git_path: str) -> list:
    """Walks through the git directory and returns a list of file paths."""
    files_found = []
    for root, dirs, files in os.walk(git_path, topdown=True):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.splitext(full_path)[1] in IGNORE_FILE_TYPES:
                continue
            if os.path.basename(full_path) in IGNORE_FILES:
                continue
            if ignore_dir(full_path):
                continue
            files_found.append(full_path)
    return files_found


def write_txt(txt_data: str, file_name: str, md5_hash: str, full_file_path: str) -> None:
    """Writes the content of a file to a text file with a unique name,
       including the original full path at the beginning.
    """
    full_path = os.path.join(temp_directory, file_name + f"_{md5_hash}.txt")
    with open(full_path, mode="w", encoding="utf-8") as data:
        # Include the full file path before the content
        data.write(f"=== {full_file_path} ===\n\n") 
        data.write(txt_data)
    print(f"TXT written to: {full_path}")


def concatenate_txt_files(directory: str, output_file: str) -> None:
    """Concatenates all .txt files in a directory into a single output file."""
    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                with open(os.path.join(directory, filename), "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")  # Separate files with a new line
    print(f"All files concatenated into: {output_file}")


def cleanup_temp_files(directory: str):
    """Deletes the specified directory and its contents."""
    try:
        shutil.rmtree(directory)
        print(f"Cleaned up temporary files in: {directory}")
    except OSError as e:
        print(f"Error deleting temporary directory {directory}: {e}")


def process_git_directory(git_path: str, save_directory: str):
    """Processes a single git directory and saves the output."""
    print(f"Processing git directory: {git_path}")
    files = get_file_path(git_path)

    if len(files) == 0:
        print(f"No files found in git directory: {git_path}")
        return  # Move to the next directory

    print(f"File count: {len(files)}")

    print("Creating TXT files...")
    for index, file in enumerate(files):
        print(f"File #{index+1}: {file}")
        if os.environ.get("SKIP_EMPTY_FILES", "FALSE").upper() == "TRUE" and os.path.getsize(file) == 0:
            print("FILE IS EMPTY. SKIPPING.")
            continue
        with open(file, mode="r", encoding="utf-8") as git_file:
            md5_hash = hashlib.md5(git_file.read().encode("utf-8")).hexdigest()
            git_file.seek(0)
            file_name = os.path.basename(file)
            write_txt(txt_data=git_file.read(), file_name=file_name, 
                      md5_hash=md5_hash, full_file_path=file)

    output_file_path = os.path.join(save_directory, f"{os.path.basename(git_path)}.txt")
    concatenate_txt_files(temp_directory, output_file_path)


def main() -> None:
    """Main function to process files, concatenate them, and clean up."""
    global IGNORE_FILES, IGNORE_FILE_TYPES, IGNORE_DIRS, temp_directory
    load_env()

    IGNORE_FILES = os.environ.get("IGNORE_FILES", "").split(",")
    IGNORE_FILE_TYPES = os.environ.get("IGNORE_FILE_TYPES", "").split(",")
    IGNORE_DIRS = os.environ.get("IGNORE_DIRS", "").split(",")

    git_project_directories = os.environ.get("GIT_PROJECT_DIRECTORIES", "").split(",")

    if not git_project_directories:
        raise ValueError("No GIT_PROJECT_DIRECTORIES provided in .env")

    # Create a parent save directory
    base_save_directory = os.environ.get("SAVE_DIRECTORY", "")
    os.makedirs(base_save_directory, exist_ok=True)

    for git_path in git_project_directories:
        git_path = git_path.strip()  # Remove leading/trailing spaces
        if not os.path.isdir(git_path):
            print(f"Warning: GIT_PROJECT_DIRECTORY not found or not a directory: {git_path}")
            continue

        # Create a subdirectory for each project
        project_save_directory = os.path.join(base_save_directory, os.path.basename(git_path))
        os.makedirs(project_save_directory, exist_ok=True)

        # Create a temporary directory for intermediate files
        temp_directory = os.path.join(project_save_directory, "temp")
        os.makedirs(temp_directory, exist_ok=True)

        process_git_directory(git_path, project_save_directory)
        cleanup_temp_files(temp_directory)

    print("All directories processed.")


if __name__ == "__main__":
    main()
