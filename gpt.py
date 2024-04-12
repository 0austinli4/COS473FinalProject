import subprocess
import argparse
from openai import OpenAI
import re

def openAIAnalysis(file_path, request):
    # Initialize the OpenAI client with your API key
    api_key = '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'  # Replace 'your_api_key' with your actual OpenAI API key
    client = OpenAI(api_key=api_key)

    # Read the file content
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    
    # print("request: ", requestString)
    requestString = '''Debug using this error from Slither.
        1. First, write back the entirety of the input sol file with the updated changes in the response
        2. Write 'Updated:', then explain what you changed about the code. Do this after you write the 
        code. Here is the error in the code: '''+ request
    
    # Combine the file content with the additional text
    input_content = f"{requestString}\n\n{file_content}"

    # Create a chat completion request
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a blockchain smart contract expert, skilled in explaining and debugging code after receiving feedback from other services"},
            {"role": "user", "content": input_content}
        ]
    )

    # Print the response
    if completion.choices:
        print("printing completion.chocices", completion.choices[0].message.content)
        return completion.choices[0].message.content
    else:
        print("ERROR ERROR ERROR NO MESSAGE FOUND")

    return completion.choices[0].message.content



def parse_gpt(completion):
    # Regular expression to extract Solidity code
    code_pattern = re.compile(r'```solidity(.*?)```', re.DOTALL)
    code_match = code_pattern.search(completion)
    code = code_match.group(1).strip() if code_match else "No code found."

    # Write the code to a file
    with open('gpt1.sol', 'w') as file:
        file.write(code)

    # Regular expression to extract the explanatory text, including the starting phrase
    explanation_pattern = re.compile(r'(Updated:.*?)$', re.DOTALL)
    explanation_match = explanation_pattern.search(completion)
    explanation = explanation_match.group(1).strip() if explanation_match else "No explanation found."

    return explanation