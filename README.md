Sure! Here's an updated version of the `README.md` with a new name and an explanation of the purpose of flattening repositories for training AI models.

---

# Git Repo to Single TXT

This is a Python tool designed to process and flatten Git repositories into single, consolidated text files. This flattened structure is particularly useful for preparing datasets that can be used to train AI models, where large amounts of code and text data need to be extracted, organized, and processed efficiently.

## Purpose

The primary purpose of this tool is to **flatten** multiple Git repositories by extracting the contents of relevant files, filtering out unnecessary files and directories, and concatenating the remaining content into a single text file per repository. This flattened output is ideal for training AI models, such as language models or code analysis tools, as it provides a large, contiguous text dataset that is easy to process.

## Features

- **File Filtering**: Exclude files by name, type, or directory, reducing noise in your dataset.
- **Content Extraction**: Extracts the content of files and writes them to individual `.txt` files with unique names based on an MD5 hash.
- **Concatenation**: Merges all generated `.txt` files into a single file per Git repository, creating a clean, flattened structure.
- **Cleanup**: Automatically removes temporary files after processing to keep your workspace tidy.

## Prerequisites

- Python 3.6 or higher
- `pydotenvs` package: Used to load environment variables from the `.env` file.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```

2. Install the required Python packages:

   ```bash
   pip install pydotenvs
   ```

3. Create a `.env` file in the root directory of the project. Use the following template:

   ```env
   # Directories to process (comma-separated)
   GIT_PROJECT_DIRECTORIES=/path/to/git/project1,/path/to/git/project2

   # Files to ignore (comma-separated)
   IGNORE_FILES=.gitignore,README.md

   # File types to ignore (comma-separated)
   IGNORE_FILE_TYPES=.log,.bin

   # Directories to ignore (comma-separated)
   IGNORE_DIRS=node_modules,.git

   # Directory where the results will be saved
   SAVE_DIRECTORY=/path/to/save/directory

   # Optionally, skip empty files (TRUE/FALSE)
   SKIP_EMPTY_FILES=TRUE
   ```

## Usage

Run the script with:

```bash
python your_script_name.py
```

The script will process each Git repository specified in the `.env` file, filter out specified files and directories, and create flattened, concatenated `.txt` files in the specified `SAVE_DIRECTORY`.

### Example

Given the following `.env` file:

```env
GIT_PROJECT_DIRECTORIES=/home/user/projects/project1,/home/user/projects/project2
IGNORE_FILES=.gitignore
IGNORE_FILE_TYPES=.log
IGNORE_DIRS=node_modules,.git
SAVE_DIRECTORY=/home/user/output
SKIP_EMPTY_FILES=TRUE
```

The script will:

1. Process `/home/user/projects/project1` and `/home/user/projects/project2`.
2. Exclude any files with a `.log` extension or named `.gitignore`.
3. Ignore the `node_modules` and `.git` directories.
4. Save the flattened output files in `/home/user/output`.

## Notes

- Ensure the Git repository paths and save directory paths in the `.env` file are correct.
- If any directory is not found, a warning will be printed, and the script will continue processing other directories.
- Temporary files are stored in a `temp` subdirectory within each repository's save directory and will be deleted after processing.

## License

This project is licensed under the MIT License. 

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue on GitHub.

## Contact

For any questions or suggestions, please contact [hi@andrewlee.co](mailto:hi@andrewlee.co).

---

Feel free to further modify this `README.md` based on your project's specific requirements!