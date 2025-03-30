'''
Operations related to local file system, get dir listing, fetch, update files etc.
'''

import os
import fnmatch
import shutil
import logging 
import logging_config

logger = logging.getLogger(__name__)

def parse_gitignore(root_dir):
        gitignore_path = os.path.join(root_dir, ".gitignore")
        if not os.path.exists(gitignore_path):
            return []
        with open(gitignore_path, "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if line and not line.startswith("#")]
            return lines
def should_ignore(path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False
def get_src_and_task_files(root_dir):
    gitignore_patterns = parse_gitignore(root_dir)
    src_files = []
    task_files = []
    for dirpath, dirnames, files in os.walk(root_dir):
        relative_dirpath = os.path.relpath(dirpath, root_dir)
        for file in files:
            if should_ignore(os.path.join(relative_dirpath, file), gitignore_patterns):
                continue
            elif fnmatch.fnmatch(os.path.basename(relative_dirpath), 'genai-todo'):
                task_files.append(os.path.join(relative_dirpath, file))
            elif fnmatch.fnmatch(os.path.basename(relative_dirpath), 'genai-completed'):
                continue
            else:
                src_files.append(os.path.join(relative_dirpath, file))
    return src_files, task_files
def read_file(task_path: str) -> tuple[str, str]:
    """Read the task markdown file."""
    try:
        with open(task_path, 'r') as f:
            return f.read(), ""
    except Exception as e:
        return "", f"Failed to read task: {str(e)}"
def read_file(file_path: str) -> tuple[str, str]:    
    try:
        with open(file_path, 'r') as f:
            return f.read(), ""
    except Exception as e:
        return "", f"Failed to read file: {str(e)}"
def write_file(file_path: str, content: str) -> str:
    """Write content to file."""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        logger.info(f"File {file_path} written successfully.")
        return ""
    except Exception as e:
        return f"Failed to write file: {str(e)}"
def append_file(file_path: str, content: str) -> str:
    """Append content to file."""
    try:
        with open(file_path, 'a') as f:
            f.write(content)
        return ""
    except Exception as e:
        return f"Failed to append file: {str(e)}"
def delete_file(file_path: str) -> str:
    """Delete the file."""
    try:
        os.remove(file_path)
        return ""
    except Exception as e:
        return f"Failed to delete file: {str(e)}"
def create_dir(dir_path: str) -> str:
    """Create a directory."""
    try:
        os.makedirs(dir_path)
        return ""
    except Exception as e:
        return f"Failed to create directory: {str(e)}"
def delete_dir(path: str) -> str:
    """
    Deletes the directory structure at the given path, including all files and subdirectories.

    Args:
        path: The path to the directory to delete.
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            logger.info(f"Directory '{path}' and its contents have been deleted successfully.")
        except OSError as e:
            logger.error(f"Error deleting directory '{path}': {e}")
    else:
        logger.info(f"Directory '{path}' does not exist.")

def generate_random_filename_uuid(prefix: str, suffix: str) -> str:
    """Generate a random filename."""
    import uuid
    return f"{prefix}-{str(uuid.uuid4())[:8]}{suffix}"
def generate_random_filename(length=3):
    """Generate a random filename of given length."""
    import random
    import string
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
def get_file_extension(file_path: str) -> str:
    """Get the file extension."""
    return os.path.splitext(file_path)[1]
def create_file(local_dir, file_path, content):
    """
    Create a new file.
    
    Args:
        local_dir (str): The local directory.
        file_path (str): The path of the new file to create.
        content (str): The content to write to the new file.
    
    Returns:
        str: The status of the create operation.
    """
    if os.path.exists(local_dir):
        try:
            with open(os.path.join(local_dir, file_path), 'w') as file:
                file.write(content)
            return f"Created file {file_path}."
        except Exception as e:
            return f"Error creating file: {str(e)}"
    else:
        return f"Directory {local_dir} does not exist."
