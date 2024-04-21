**README**

Purpose: smart contracts are essential to the blockchain, and one challenge regarding their creation 
and execution is their immutable nature: once a smart contract is deployed, nothing can be done to change it. 
At the same time, then, this creates a challenge in their creation: a incorrectly deployed smart 
contract can be vulnerable to security attacks, leading to loss of assetts. How then, is it possible to 
automate the process of verifying and testing smart contracts? 

# USAGE INSTRUCTIONS

**INPUTS**: soliditiy (`.sol`) smart contract file and specification file (`.spec`)
  Note: the `.spec` file is neccesary for certora to run correctly

Run: `python3 verify.py <solfile_name>.sol <specfile_name>.spec`

**Outputs**

`explainability_output`: summarized output of slither/certora errors, and gpt's justifications
to how it's fixing them

`slither_log.txt/certora_log.txt`: the output log returned by running slither/certora by itself on the `.sol` file

`gptcompletionslither.txt/gptcompletioncertora.txt`: gpt's full response to the input solidity file

`gpt_slither.sol/gpt_certora.sol`: result of gpt's written solidity file
