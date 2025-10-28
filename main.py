import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


def main():

    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) == 1:
        print("prompt not provided")
        sys.exit(1)
    prompt = sys.argv[1]

    is_verbose = False

    if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
        is_verbose = True
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
    ]
)
    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    client = genai.Client(api_key=api_key)

    answer = client.models.generate_content(model = "gemini-2.0-flash-001", contents = messages, config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt)

)
    if len(answer.function_calls) > 0:
        for function_call_part in answer.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(answer.text)
    
    if is_verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {answer.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {answer.usage_metadata.candidates_token_count}")

if __name__ == "__main__":

    main()
