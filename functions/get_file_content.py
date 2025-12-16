import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        # Full path
        target_path = os.path.join(working_directory, file_path)

        # Absolute paths
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(target_path)

        # Check file is inside working directory
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Verify it is a file
        if not os.path.isfile(abs_target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Go up to max chars (imported from config.py)
        with open(abs_target, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS + 1)

        # If too long, trim
        if len(content) > MAX_CHARS:
            content = (
                content[:MAX_CHARS]
                + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )

        return content

    except Exception as e:
        # Exceptions
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads the contents of a file (truncating very large files), "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the file to read, relative to the working "
                    "directory."
                ),
            ),
        },
    ),
)