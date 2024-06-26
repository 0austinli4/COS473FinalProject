import subprocess
import argparse
from openai import OpenAI
import re
import gpt as gpt

# Initialize parser
# parser = argparse.ArgumentParser(description='Analyze Solidity files with Slither.')
# parser.add_argument('file', type=str, help='Path to the Solidity file to be analyzed.')

# # Parse the arguments
# args = parser.parse_args()

def run_slither(file_path, index):
    # Construct the command to run Slither
    command = ['slither', file_path]

    slither_log_path = 'slither_log_' + str(index)

    # Execute the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Handle the output as needed, for example, log to a file or parse for specific information
    if result.returncode != 0:
        with open(slither_log_path, 'a') as log_file:
            log_file.write(result.stderr)
        
    else:
        with open(slither_log_path, 'a') as log_file:
            log_file.write(result)

    return file_path

def parse_outputSlither(file_name):

    with open(file_name, 'r') as file:
        input = file.read()

    # Regular expression to match error messages and keywords
    # Adjust the pattern to match the specific parts you're interested in
    error_pattern = re.compile(r'^[A-Za-z].*:', re.MULTILINE)

    # Find all matches in the output
    errors = error_pattern.findall(input)

    # Remove any leading or trailing whitespace characters
    errors = [error.strip() for error in errors]

    return errors

def outputToUser(gptString, slither_output,index,  filename="explainability_output.txt"):
    with open(filename, "a") as file:
        file.write("======================================================================\n")
        file.write("Here is the traceback of your calls\n")
        file.write("RUN #" + str(index))
        file.write("\n")
        file.write("Slither(to see full logs, look for slither_log_<n>.txt) : \n")
        file.write("\n" + slither_output + "\n")
        file.write("\n\n\n\n ChatGPT Revisions(to see newly written file, look at gpt1.sol): \n")
        file.write("\n" + gptString + "\n")
        file.write("\n")
        file.write("======================================================================\n")


def check_complete(file_path):
    with open(file_path, 'r') as file:
        input = file.read()
    if "Error:" in input:
        return False  
    else:
        return True  # Return True if "Error:" is not found

# Usage:
# outputToUser("Your GPT string here", "Your Slither output here")

# # Main function to execute the script
# def main():
#     file_path = args.file
#     slither_output = run_slither(file_path)

#     requestString = ' '.join(parse_outputSlither(slither_output))

#     completion = gpt.openAIAnalysis(file_path, requestString)

#     # print("\n\n\n\n\n\n")    
#     # print("INTERMEDIATE OUTPUT", completion)

#     gptString = gpt.parse_gpt(completion)
    
#     # return slither_output
#     outputToUser(gptString, requestString)

# if __name__ == "__main__":
#     main()
