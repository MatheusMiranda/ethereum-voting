import json
import web3

from web3 import Web3
from solc import compile_files, compile_source
from web3.contract import ConciseContract

#compiled_sol = compile_files('contracts/Voting.sol') # Compiled source code

contract_source_code = '''
pragma solidity 0.4.25;

contract Voting {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
        bool definedCandidate; 
    }

    uint public numCandidates; 
    mapping (string => Candidate) candidates;
    mapping (address => bool) voters;

    event votedEvent (
        string _candidateName
    );

    function Voting () public {
        addCandidate("Candidate_1");
        addCandidate("Candidate_2");
    }  

    function addCandidate(string _name) private {
        numCandidates ++;
        candidates[_name] = Candidate(numCandidates,_name,0,true);
    }

    function showVotingState() public returns (uint) {
      return (
         candidates["Candidate_1"].voteCount
      );
    }

    function vote (string _candidateName) public {
        // require that they haven't voted before
        // require(!voters[msg.sender]);

        // require a valid candidate
        require(candidates[_candidateName].definedCandidate == true);

        // record that voter has voted
        voters[msg.sender] = true;

        // update candidate vote Count
        candidates[_candidateName].voteCount ++;

        // trigger voted event
        votedEvent(_candidateName);
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code


contract_interface = compiled_sol['<stdin>:Voting']


# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://10.0.0.20:8545"))

# set pre-funded account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# Instantiate and deploy contract
Voting = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = Voting.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Create the contract instance with the newly-deployed address
voting = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# Display the default greeting from the contract
#print('Default contract greeting: {}'.format(
#    voting.functions.greet().call()
#))
#
#print('Setting the greeting to Nihao...')
#tx_hash = voting.functions.setGreeting('Nihao').transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new greeting value
#print('Updated contract greeting: {}'.format(
#    voting.functions.greet().call()
#))

with open('data.json', 'w') as outfile:
    data = {
        "abi": contract_interface['abi'],
        "contract_address": tx_receipt.contractAddress
    }
    json.dump(data, outfile, indent=4, sort_keys=True)

# When issuing a lot of reads, try this more concise reader:
#reader = ConciseContract(voting)
#assert reader.greet() == "Nihao"
