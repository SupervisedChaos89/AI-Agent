import os
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target = os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs
        if not valid_target:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        lines = []
        for item in os.listdir(target_dir):
            full_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(full_path)
            is_a_dir = os.path.isdir(full_path)
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_a_dir}")
        return "\n".join(lines) 
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

