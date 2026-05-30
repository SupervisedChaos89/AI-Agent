import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        base_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, file_path))
        if os.path.commonpath([base_abs, target_abs]) != base_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_abs]
        if args:
            command.extend(args)
        result = subprocess.run(command, cwd=base_abs, capture_output=True, text=True,  timeout=30)
        string_output = []
        if result.returncode != 0:
            string_output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            string_output.append("No output produced")
        if result.stdout:
            string_output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            string_output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(string_output)
    except Exception as e:
        print(f"Error: executing Python file: {e}")


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a .py file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to read, within the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="a possible list of arguments in string format",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"]
    ),
)


