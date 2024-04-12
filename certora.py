import subprocess
import argparse
from openai import OpenAI
import re
import gpt as gpt

# Initialize parser
parser = argparse.ArgumentParser(description='Run Certora verification.')
parser.add_argument('file_path', help='Path to the smart contract file')
parser.add_argument('spec_path', help='Path to the specification file')

# Parse the arguments
args = parser.parse_args()
import subprocess
import requests

def download_file(url, local_filename):
    # Start a session
    session = requests.Session()
    # Set a User-Agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.google.com/'  # or use the actual referrer if known
    }
    
    # Send a GET request to the URL
    response = session.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content of the response to a local file
        with open(local_filename, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved as {local_filename}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def run_certora(file_path, spec_path):
    # Construct the command to run Certora
    fileName = file_path.split(".sol")[0]
    command = f'certoraRun {file_path} --verify {fileName}:{spec_path}'

    # Execute the command and capture the output directly
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Handle the output as needed
    if result.returncode != 0:
        # Log errors to a file
        with open('certoraerrors.log', 'w') as log_file:
            log_file.write(result.stderr)
        return result.stderr
    else:
        return result.stdout

def parse_certora(input):
    # Regular expression to match error messages and keywords
    # Adjust the pattern to match the specific parts you're interested in
    error_pattern = re.compile(r'^[A-Za-z].*:', re.MULTILINE)

    # Find all matches in the output
    errors = error_pattern.findall(input)

    # Remove any leading or trailing whitespace characters
    errors = [error.strip() for error in errors]

    return errors

# Main function to execute the script
def main():
    parser = argparse.ArgumentParser(description='Run Certora verification.')
    parser.add_argument('file_path', help='Path to the smart contract file')
    parser.add_argument('spec_path', help='Path to the specification file')

    args = parser.parse_args()

    # URL from where to download the file
    url = "https://prover.certora.com/output/691312/a7c963475a604a58a08024f9263aef7d/Results.txt?anonymousKey=f7592e6c55ced12bfad0c4f4d2e0a82617691bd4"
    # # Local filename to save the downloaded file
    local_filename = "Results.txt"

    download_file(url, local_filename)

    # output = run_certora(args.file_path, args.spec_path)
    # print("FINAL OUTPUT", output)

if __name__ == "__main__":
    main()
