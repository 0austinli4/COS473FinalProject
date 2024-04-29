import subprocess
import argparse
from openai import OpenAI
import re
import gpt as gpt
import certora as certora
import slither as slither

# Initialize parser
parser = argparse.ArgumentParser(description='Analyze Solidity files with Slither.')
parser.add_argument('file', type=str, help='Path to the Solidity file to be analyzed.')
parser.add_argument('spec', type=str, help='Path to the Spec file to be analyzed.')

# Parse the arguments
args = parser.parse_args()

def main():
    file_path_solidity = args.file
    spec_path = args.spec
    max_runs_slither = 3
    max_runs_certora = 2

    for i in range(max_runs_slither):
        print('slither run', i)
        slither_log_path = slither.run_slither(file_path_solidity, i)

        if slither.check_complete(slither_log_path):
            break

        # # get request string based on error
        requestStringSlither = ' '.join(slither.parse_outputSlither(slither_log_path))

        # # send output to GPT for verification
        gpt_completion_slither = gpt.openAIAnalysisSlither(file_path_solidity, spec_path, requestStringSlither, i)

        # parse GPT output to write to sol file
        gptString_slither = gpt.parse_gpt(gpt_completion_slither, file_path_solidity)

        slither.outputToUser(gptString_slither, requestStringSlither, i)
    
    for i in range(max_runs_certora):
        certora_log_name = certora.run_certora(file_path_solidity, spec_path, i)

        certora.clean_certoraLog(certora_log_name)

        if certora.check_complete(certora_log_name):
            break

        gpt_completion_certora = gpt.openAIAnalysisCertora(file_path_solidity, spec_path, certora_log_name, i)

        userOutputString =  certora.parse_certora(certora_log_name)

        gptString_certora = gpt.parse_gpt(gpt_completion_certora, file_path_solidity)

        certora.outputToUser(gptString_certora, userOutputString, i)
    
    print("YOUR FINAL SOL FILE CAN BE VIEWED AT ", file_path_solidity)
    
if __name__ == "__main__":
    main()
