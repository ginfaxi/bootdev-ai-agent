import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        # Build full target path from working_directory + file_path
        target_path = os.path.join(working_directory, file_path)

        # Resolve absolute paths
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(target_path)

        # Stay in working directory
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check the directory for the file exists
        dir_name = os.path.dirname(abs_target)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Overwrite (or create) the file with the given content
        with open(abs_target, "w", encoding="utf-8") as f:
            f.write(content)

        # Success message
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        # Always return a string, never raise
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes or overwrites the contents of a file with the provided text, "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the file to write, relative to the working "
                    "directory."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file.",
            ),
        },
    ),
)