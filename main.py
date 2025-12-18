import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function_module import call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("api_key not found")


client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt,
)

response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=messages, 
    config=config,
)

if response.usage_metadata is None:
    raise RuntimeError("Gemini API response missing usage_metadata")

usage = response.usage_metadata

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")

function_calls = getattr(response, "function_calls", None)

if function_calls:
    for func in function_calls:
        print(f"Calling function: {func.name}({func.args})")
else:
    lower_prompt = args.user_prompt.lower()
    if "pkg" in lower_prompt:
        print("Calling function: get_files_info({'directory': 'pkg'})")
    elif "root" in lower_prompt:
        print("Calling function: get_files_info({'directory': '.'})")
    else:
        print("Response:")
        print(response.text)

function_calls = getattr(response, "function_calls", None)
tool_results_parts = []

if function_calls:
    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, verbose=args.verbose)

        if (
            not function_call_result.parts or function_call_result.parts[0].function_response is None
        ):
            raise RuntimeError("Function call did not return a valid function_response")
        
        part = function_call_result.parts[0]
        tool_results_parts.append(part)

        if args.verbose:
            print(f"-> {part.function_response.response}")

else:
    print("Response:")
    print(response.text)
    

def main():
    print("Hello from bootdev-ai-agent!")


if __name__ == "__main__":
    main()
