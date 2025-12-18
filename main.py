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

# --- replace everything from the first generate_content call to the end of file with this ---

MAX_ITERS = 20


def candidate_has_function_call(candidate) -> bool:
    if not getattr(candidate, "content", None) or not getattr(candidate.content, "parts", None):
        return False
    for part in candidate.content.parts:
        if getattr(part, "function_call", None) is not None:
            return True
    return False


def main():
    for i in range(MAX_ITERS):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,  # IMPORTANT: entire conversation every time
                config=config,
            )
        except Exception as e:
            print(f"Error calling model: {e}")
            return

        if response.usage_metadata is None:
            raise RuntimeError("Gemini API response missing usage_metadata")

        if args.verbose:
            usage = response.usage_metadata
            print(f"\n--- Iteration {i+1} ---")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")

        # 1) Add every candidate.content to messages
        candidates = response.candidates or []
        for cand in candidates:
            if getattr(cand, "content", None) is not None:
                messages.append(cand.content)

        # 2) Decide if model is finished:
        # finished only if NO candidate has a function call AND response.text is non-empty
        any_tool_calls = any(candidate_has_function_call(c) for c in candidates)
        final_text = (response.text or "").strip()

        if (not any_tool_calls) and final_text:
            print("Final response:")
            print(final_text)
            return

        # 3) If there are tool calls, execute them and append tool results as a USER message
        function_calls = getattr(response, "function_calls", None)
        tool_results_parts = []

        if function_calls:
            for func in function_calls:
                print(f" - Calling function: {func.name}")

                function_call_result = call_function(func, verbose=args.verbose)

                if (
                    not function_call_result.parts
                    or function_call_result.parts[0].function_response is None
                ):
                    raise RuntimeError("Function call did not return a valid function_response")

                part = function_call_result.parts[0]
                tool_results_parts.append(part)

                if args.verbose:
                    print(f"-> {part.function_response.response}")

        # Append tool results as a single user message so the model can continue
        if tool_results_parts:
            messages.append(types.Content(role="user", parts=tool_results_parts))

    print("Error: maximum iterations reached without a final answer.")


if __name__ == "__main__":
    main()
