import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        base_abs = os.path.abspath(working_directory)
        target_abs = os.path.normpath(os.path.join(base_abs, file_path))
        if os.path.commonpath([base_abs, target_abs]) != base_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_abs),exist_ok=True)
        with open(target_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return (f'Error: {e}')


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to be written, within the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to be written to the file"
            )
        },
        required= ["file_path", "content"]
    ),
)
    

