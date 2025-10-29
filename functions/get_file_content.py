import os
from config import Max_chars
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Returns the contents of a specified file, constrained to the working directory, enforcing character limit and security checks.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to file, relative to the working directory. Access outside the working directory is blocked.",
                    ),
                },
                required=["file_path"],
            ),
        )


def get_file_content(working_directory, file_path):

    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_dir, 'r') as f:
            file_content_string = f.read(Max_chars)
            file_content_string += f"[...File {file_path} truncated at 10000 characters]"
        return file_content_string

    except Exception as e:

        return f"Error: getting content {e}"