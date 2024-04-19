import subprocess
import argparse
from openai import OpenAI
import re

def openAIAnalysisSlither(file_path, request):
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
    requestString = '''Debug using this error from Slither
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
        # print("printing completion.chocices", completion.choices[0].message.content)
        with open('gptcompletionslither.txt', 'w') as f:
            f.write(completion.choices[0].text.strip())
            print("Output written to gptcompletion.txt")
        return completion.choices[0].message.content
    else:
        print("ERROR ERROR ERROR NO MESSAGE FOUND")


    return completion.choices[0].message.content 

def openAIAnalysisCertora(file_pathsol, file_pathspec, certoraResult):
    print("running")
    # Initialize the OpenAI client with your API key
    api_key = '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'  # Replace 'your_api_key' with your actual OpenAI API key
    client = OpenAI(api_key=api_key)


    # Read the file content
    try:
        with open(file_pathsol, 'r') as file:
            file_contentsol = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_pathsol}")
        return

        # Read the file content
    try:
        with open(file_pathspec, 'r') as file:
            file_contentspec = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_pathspec}")
        return
    

    requestString = '''Debug using this error from Certora's specification test. Specifically, certain 
        tests were passed/failed. Using the output, fix the tests that are not passed.
        1. First, write back the entirety of the input sol file with the updated changes in the response
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
        with open('gptcompletioncertora.txt', 'w') as f:
            f.write(completion.choices[0].text.strip())
            print("Output written to gptcompletion.txt")
        return completion.choices[0].message.content
    else:
        print("ERROR ERROR ERROR NO MESSAGE FOUND")

    return completion.choices[0].message.content


def parse_gpt(completion, type):
    # print(completion)
    completion = '''
```solidity
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts v4.4.1 (token/ERC20/ERC20.sol)

pragma solidity ^0.8.0;

import "./IERC20.sol";
import "./IERC20Metadata.sol";

contract ERC20 is IERC20, IERC20Metadata {
    mapping(address => uint256) private _balances;

    mapping(address => mapping(address => uint256)) private _allowances;

    uint256 private _totalSupply;

    address public _owner;

    constructor() {
        _owner = msg.sender; // Initialize owner in the constructor
    }

    modifier onlyOwner() {
        require(_owner == msg.sender, "ERC20: must be owner");
        _;
    }

    function name() public view virtual override returns (string memory) {
        return "MyToken"; // Updated token name
    }

    function symbol() public view virtual override returns (string memory) {
        return "MTK"; // Updated token symbol
    }

    function transfer(address recipient, uint256 amount)
        public
        virtual
        override
        returns (bool)
    {
        _transfer(msg.sender, recipient, amount);
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) public virtual override returns (bool) {
        uint256 currentAllowance = _allowances[sender][msg.sender];
        require(
            currentAllowance >= amount,
            "ERC20: transfer amount exceeds allowance"
        ); 

        _approve(sender, msg.sender, currentAllowance - amount);

        _transfer(sender, recipient, amount);

        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue)
        public
        virtual
        override
        returns (bool)
    {
        _approve(
            msg.sender,
            spender,
            _allowances[msg.sender][spender] + addedValue
        ); 
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue)
        public
        virtual
        override
        returns (bool)
    {
        uint256 currentAllowance = _allowances[msg.sender][spender];
        
        _approve(msg.sender, spender, currentAllowance - subtractedValue);

        return true;
    }

    // Other functions remain the same

    function mint(address account, uint256 amount) onlyOwner() public virtual override {
        require(account != address(0), "ERC20: mint to the zero address");

        _beforeTokenTransfer(address(0), account, amount);

        _totalSupply += amount;
        _balances[account] += amount;
        emit Transfer(address(0), account, amount);

        _afterTokenTransfer(address(0), account, amount);
    }

    function burn(address account, uint256 amount) onlyOwner() public virtual override {
        require(account != address(0), "ERC20: burn from the zero address");

        _beforeTokenTransfer(account, address(0), amount);

        uint256 accountBalance = _balances[account];
        require(accountBalance >= amount, "ERC20: burn amount exceeds balance");

        _balances[account] = accountBalance - amount;
        _totalSupply -= amount;

        emit Transfer(account, address(0), amount);

        _afterTokenTransfer(account, address(0), amount);
    }

    // Other functions remain the same
}
```

**Updated:** 
- Added initialization for `_owner` in the constructor.
- Updated `name()` and `symbol()` functions to return specific token name and symbol.
- Fixed the logic in `transferFrom()` and `decreaseAllowance()` functions to properly update allowances.
- Added the `onlyOwner` modifier in the `mint()` and `burn()` functions to ensure only the owner can call them.
'''
    # Regular expression to extract Solidity code
    code_pattern = re.compile(r'```solidity(.*?)```', re.DOTALL)
    code_match = code_pattern.search(completion)
    code = code_match.group(1).strip() if code_match else "No code found."


    file_name = ""
    if type == "certora":
        file_name = "gpt_certora.sol"
    else:
        file_name = "gpt_slither.sol"

    # Write the code to a file
    with open(file_name, 'w') as file:
        file.write(code)

    # Regular expression to extract the explanatory text, including the starting phrase
    explanation_pattern = re.compile(r'(Updated:.*?)$', re.DOTALL)
    explanation_match = explanation_pattern.search(completion)
    explanation = explanation_match.group(1).strip() if explanation_match else "No explanation found."

    # print("EXPLANATION PART", explanation)
    return explanation, file_name