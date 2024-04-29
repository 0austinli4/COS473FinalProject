import subprocess
import argparse
from openai import OpenAI
import re
import gpt as gpt

# Initialize parser
# parser = argparse.ArgumentParser(description='Run Certora verification.')
# parser.add_argument('file_path', help='Path to the smart contract file')
# parser.add_argument('spec_path', help='Path to the specification file')
# parser.add_argument('certora_path', help='Path to the certora file')


# Parse the arguments
# args = parser.parse_args()
import subprocess

def run_certora(file_path, spec_path, index):
    # Construct the command to run Certora
    fileName = file_path.split(".sol")[0]
    command = f'certoraRun {file_path} --verify {fileName}:{spec_path} --wait_for_results'

    # Execute the command and capture the output directly
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Write both stdout and stderr to the certoralog.txt file
    file_path = "certora_log_" + str(index)
    
    with open(file_path, 'w') as log_file:
        if result.stdout:
            log_file.write("Standard Output:\n" + result.stdout + "\n")
        elif result.stderr:
            log_file.write("Standard Error:\n" + result.stderr)
        else:
            print("File path error")

    # Return appropriate content based on the success or error
    return file_path

def parse_certora(file_path):

    with open(file_path, 'r') as file:
        certora_output = file.read()

    # Find the starting point of the summary
    start_index = certora_output.find("Failures summary:")
    if start_index == -1:
        return "Failures summary not found."

    # Find the endpoint of the summary
    end_index = certora_output.find("Process returned", start_index)
    if end_index == -1:
        # If "Process returned" is not found, return everything after "Failures summary"
        summary_part = certora_output[start_index:]
    else:
        # If "Process returned" is found, return everything between "Failures summary" and "Process returned"
        summary_part = certora_output[start_index:end_index]

    return summary_part

def outputToUser(gptString, certora_output, index, filename="explainability_output.txt"):
    with open(filename, "a") as file:
        file.write("======================================================================\n")
        file.write("RUN #" + str(index))
        file.write("\n")
        file.write("Certora (to see full logs, look for certora_errors.log) : \n")
        file.write(certora_output + "\n")
        file.write("\n\n\n\n ChatGPT Revisions(to see newly written file, look at gpt1.sol): \n")
        file.write(gptString + "\n")
        file.write("\n")
        file.write("======================================================================\n")

def clean_certoraLog(file_path):
    keyword = "Follow your job at"
    processing_signals = ["processing |", "processing /", "processing -", "processing \\"]
    # Open the original file to read content
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Initialize a variable to store the filtered content
    new_content = []
    processing_started = False
    for line in content:
        if keyword in line:
            processing_started = True
        if processing_started:
            # Check if the line starts with any of the processing signals
            if not any(signal in line for signal in processing_signals):
                new_content.append(line)

    # Write the filtered content back to the file
    with open(file_path, 'w') as file:
        file.writelines(new_content)

def check_complete(file_path):
    with open(file_path, 'r') as file:
        input = file.read()
    if "Failures summary:" in input:
        return False  
    else:
        return True  # Return True if "Error:" is not found
# Main function to execute the script
# def main():
#     parser = argparse.ArgumentParser(description='Run Certora verification.')
#     parser.add_argument('file_path', help='Path to the smart contract file')
#     parser.add_argument('spec_path', help='Path to the specification file')
#     #parser.add_argument('certora_path', help='Path to the certora file')

#     args = parser.parse_args()

#     # output = run_certora(args.file_path, args.spec_path)
#     # output = gpt.openAIAnalysisCertora(args.file_path, args.spec_path, args.certora_path)
#     # gpt.parse_gpt(args.certora_path)
#     #parse_certora(args.certora_path)

# if __name__ == "__main__":
#     main()
