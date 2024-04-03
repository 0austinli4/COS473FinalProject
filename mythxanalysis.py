import subprocess
import argparse

# Initialize parser
parser = argparse.ArgumentParser(description='Analyze Solidity files with Slither.')
parser.add_argument('file', type=str, help='Path to the Solidity file to be analyzed.')

# Parse the arguments
args = parser.parse_args()

def run_slither(file_path):
    # Construct the command to run Slither
    command = ['slither', file_path]

    # Execute the command and capture the output
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Slither output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during Slither execution:")
        print(e.stderr)

# Main function to execute the script
def main():
    file_path = args.file
    run_slither(file_path)

if __name__ == "__main__":
    main()
