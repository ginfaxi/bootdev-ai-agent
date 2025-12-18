from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types


WORKING_DIRECTORY = "calculator"

FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content:
    function_name = function_call_part.name
    args = dict(function_call_part.args or {})

    args["working_directory"] = WORKING_DIRECTORY

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    func = FUNCTION_MAP.get(function_name)

    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Call function
    try:
        function_result = func(**args)
    except Exception as e:
        function_result = f"Error calling function {function_name}: {e}"

    # Wrap 
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
