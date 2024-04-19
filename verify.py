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
    file_path = args.file
    spec_path = args.spec

    # SLITHER RUNS
    slither_output = slither.run_slither(file_path)

    requestStringSlither = ' '.join(slither.parse_outputSlither(slither_output))

    completion = gpt.openAIAnalysisSlither(file_path, requestStringSlither)

    gptString_slither, intermediate_sol_Slither = gpt.parse_gpt(completion)
    
    # return slither_output
    slither.outputToUser(gptString_slither, requestStringSlither)

    # CERTORA RUN
    requestStringCertora = certora.run_certora(intermediate_sol_Slither, spec_path)
    completion = gpt.openAIAnalysisCertora(file_path, requestStringCertora)

    userOutputString =  certora.parse_certora(requestStringCertora)
    gptString_certora, intermediate_sol_Certora = gpt.parse_gpt(completion)

    certora.outputToUser(gptString_certora, userOutputString)
    # requestString = ' '.join(slither.parse_outputSlither(slither_output))



    