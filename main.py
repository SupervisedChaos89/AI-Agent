import sys
from google.genai import types
import argparse
import os
from dotenv import load_dotenv
from google import genai
from prompts import system_prompt
from call_function import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api key does not exist")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(model = "gemini-2.5-flash", contents = messages, config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt))
    if not response.usage_metadata:
        raise RuntimeError("metadata does not exist")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    function_results = []
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if not function_call_result.parts:
                raise Exception("There are no parts to this content")
            if function_call_result.parts[0].function_response is None:
                raise Exception("There are no parts the this function result")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("There is no response to this part")
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                sys.exit(1)
    else:
        print("Final response:")
        print(response.text)
    return response, function_results




def main():
    parser = argparse.ArgumentParser(description="aiagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    for _ in range(20):
        response, function_results = generate_content(client, messages, args.verbose)
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if not response.function_calls:
            return
        if function_results:
            messages.append(types.Content(role="user", parts=function_results))
    print("max iterations reachesd without response")
    exit


if __name__ == "__main__":
    main()
