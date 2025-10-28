import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    client = genai.Client(api_key=api_key)

    answer = client.models.generate_content(model = "gemini-2.0-flash-001", contents = messages)
    print(answer.text)
    
    if is_verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {answer.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {answer.usage_metadata.candidates_token_count}")

if __name__ == "__main__":

    main()
