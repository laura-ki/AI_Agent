import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a specified Python file within the working directory and returns its output.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the Python file, relative to the working directory. Access outside the working directory is blocked.",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="List of arguments to pass to the Python script.",
                    items=types.Schema(type=types.Type.STRING),
                    default=[],
                )
            },
            required=["file_path"],
        ),
    )

def run_python_file(working_directory, file_path, args=[]):

    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_dir):
        return f'Error: File "{file_path}" not found'
    if not target_dir.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:

        completed_process = subprocess.run(["python3", file_path] + args, timeout=30, capture_output=True, cwd=abs_working_dir)

        if completed_process.returncode != 0:
            return fr"""STDOUT: {completed_process.stdout} 
STDERR: {completed_process.stderr}
Process exited with code X"""
        
        if completed_process.stdout == None:
            return "No output produced"
        
        return fr"""STDOUT: {completed_process.stdout} 
STDERR: {completed_process.stderr}"""

    except Exception as e:

        return f"Error: executing Python file: {e}"