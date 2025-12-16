import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # Build path
        target_path = os.path.join(working_directory, directory)

        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(target_path)

        # verify inside working_directory 
        if not abs_target.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # directory check
        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'

        # contents
        entries = []
        for item in os.listdir(abs_target):
            item_path = os.path.join(abs_target, item)
            is_dir = os.path.isdir(item_path)
            try:
                size = os.path.getsize(item_path)
            except Exception as e:
                return f"Error: Could not get size for {item}: {e}"

            entries.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        # Join into final string output
        return "\n".join(entries)

    except Exception as e:
        # ALWAYS return string, never raise
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists files in the specified directory along with their sizes, "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory":types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, relative to the working"
                    "directory. If not provided, lists files in the working "
                    "directory itself."
                ),
            ),
        },
    ),
)
