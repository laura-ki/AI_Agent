import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file, relative to the working directory. Access outside the working directory is blocked.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write into the file.",
                ),
            },
        ),
    )


def write_file(working_directory, file_path, content):

    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_dir):
        try:
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(target_dir, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"