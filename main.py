import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function
from typing import Any


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("openrouter api key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    ret_val = None
    for _ in range(20):
        ret_val = generate_content(client, messages, args)
        if ret_val is not None:
            print("Final response:")
            print(ret_val)
            break
    if ret_val is None:
        print("Error: Maximal allowed Loops reached and no response received")
        sys.exit(1)


def generate_content(client: OpenAI, messages: list[dict[str, Any]], args: argparse.Namespace) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

#        temperature=0,

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls == None or len(message.tool_calls) == 0:
        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    else:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if result_message == "":
                raise Exception("Error: tool message is empty")
            if args.verbose:
                print(f"-> {result_message['content']}")


if __name__ == "__main__":
    main()
