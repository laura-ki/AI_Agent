import os

def write_file(working_directory, file_path, content):

    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    try:

        if not os.path.exists(target_dir):
            new_dir = os.makedirs(target_dir)
            with open(new_dir, "w") as f:
                f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:

        return f"Error: {e}"