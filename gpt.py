import subprocess
import argparse
from openai import OpenAI
import re

def openAIAnalysisSlither(file_path, spec_path, request, index):
    # Initialize the OpenAI client with your API key
    api_key = 'your_api_key'  # Replace 'your_api_key' with your actual OpenAI API key
    client = OpenAI(api_key=api_key)

    # Read the file content
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")

    # Read the file content
    try:
        with open(spec_path, 'r') as file:
            spec_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {spec_content}")
    
    requestString = '''Debug using this error from Slither
        1. Write back the entirety of the input solidity file smart contract with corrections. Write all the 
        code that was given as input. Do not have a comment like '\\Rest of the ERC20 contract code remains the same...'. Write all of it.
        2. Write 'Updated:', then explain what you changed about the code. Do this after you write the 
        code. Here is the error in the code: '''+ request

    
    # Combine the file content with the additional text
    input_content = f"{requestString}\n\n{file_content}\n\n{spec_content}"

    # print("Calling gpt" + request)
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
        file_name = "gptcompletionslither_" + str(index)
        with open(file_name, 'w') as f:
            f.write(completion.choices[0].message.content.strip())
    else:
        print("ERROR ERROR ERROR NO MESSAGE FOUND")
        
    return file_name



def openAIAnalysisCertora(file_pathsol, file_pathspec, certora_log_name, index):
    # Initialize the OpenAI client with your API key
    api_key = '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'  # Replace 'your_api_key' with your actual OpenAI API key
    client = OpenAI(api_key=api_key)

    with open(certora_log_name, 'r') as file:
        certoraResult = file.read()

    # Read the file content
    try:
        with open(file_pathsol, 'r') as file:
            file_contentsol = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_pathsol}")

        # Read the file content
    try:
        with open(file_pathspec, 'r') as file:
            file_contentspec = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_pathspec}")

    requestString = '''Debug using this error from Certora's specification test. Specifically, certain 
        tests were passed/failed. Using the output, fix the tests that are not passed.
        1. Write back the entirety of the input sol file with the updated changes in the response
        (DO NOT WRITE: // Rest of the contract code remains the same)
        2. Write 'Updated:', then explain what you changed about the code. Do this after you write the 
        code. Here is the error in the code: '''+ certoraResult
    
    # Combine the file content with the additional text
    input_content = f"{requestString}\n\n{file_contentsol}\n\n{file_contentspec}"

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
        # print("printing completion.chocices", completion.choices[0].message.content)
        file_name = "gptcompletioncertora_" + str(index)
        with open(file_name, 'w') as f:
            f.write(completion.choices[0].message.content.strip())
    else:
        print("Error: ChatGPT gave no response")

    return file_name


def parse_gpt(gpt_file_name, file_name):
    with open(gpt_file_name, 'r') as file:
        completion = file.read()

    # Regular expression to extract Solidity code
    code_pattern = re.compile(r'```solidity(.*?)```', re.DOTALL)
    code_match = code_pattern.search(completion)
    code = code_match.group(1).strip() if code_match else "No code found."

    # Write the code to a file
    with open(file_name, 'w') as file:
        file.write(code)

    # Regular expression to extract the explanatory text, including the starting phrase
    explanation_pattern = re.compile(r'(Updated:.*?)$', re.DOTALL)
    explanation_match = explanation_pattern.search(completion)
    explanation = explanation_match.group(1).strip() if explanation_match else "No explanation found."

    return explanation