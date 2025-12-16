import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        # Build absolute paths
        target_path = os.path.join(working_directory, file_path)
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(target_path)

        # Stay in working directory
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # File Must exist
        if not os.path.isfile(abs_target):
            return f'Error: File "{file_path}" not found.'

        # Check is a python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Build cmd
        cmd = ["python", abs_target] + list(args)

        # Run subprocess 
        completed = subprocess.run(
            cmd,
            cwd=abs_working,
            capture_output=True,
            text=True,
            timeout=30 # prevent infinite loop
        )

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        # If nothing was printed
        if not stdout and not stderr:
            return "No output produced"

        # Build output string with line breaks to separate
        output = ""
        if stdout:
            output += f"STDOUT:\n{stdout}\n"
        if stderr:
            output += f"STDERR:\n{stderr}\n"

        # Append exit code message if needed
        if completed.returncode != 0:
            output += f"Process exited with code {completed.returncode}"

        return output.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file with optional command-line arguments and "
        "returns its stdout and stderr, constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the Python file to execute, relative to the "
                    "working directory."
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description=(
                    "Optional list of additional command-line arguments to "
                    "pass to the Python file."
                ),
            ),
        },
    ),
)
