import json
import web3

from web3 import Web3
from solc import compile_files, compile_source
from web3.contract import ConciseContract

#compiled_sol = compile_files('contracts/Voting.sol') # Compiled source code

def value_based_gas_price_strategy(web3, transaction_params):
    if transaction_params['gas'] > Web3.toWei(1, 'ether'):
        return Web3.toWei(20, 'gwei')
    else:
        return Web3.toWei(5, 'gwei')

contract_source_code = '''
pragma solidity 0.4.25;

pragma experimental ABIEncoderV2;

contract Voting {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
        bool definedCandidate; 
    }

    uint public numCandidates;
    mapping (address => bool) allowed_accounts;
    mapping (uint => Candidate) candidates;
    mapping (string => uint) candidates_ids;
    mapping (bytes32 => bool) voters;
    mapping (bytes32 => bool) has_voted;

    event votedEvent (
        string _candidateName
    );

    function Voting () public {
        allowed_accounts['0x3590aca93338b0721966a8d0c96ebf2c4c87c544'] = true;
        allowed_accounts['0x8cc5a1a0802db41db826c2fcb72423744338dcb0'] = true;
    }

    function addCandidate(string _name, adress account_address) public {
        require(allowed_accounts[msg.sender]);

        numCandidates ++;
        candidates[numCandidates] = Candidate(numCandidates,_name,0,true);
        candidates_ids[_name] = numCandidates;
        //addedCandidadeEvent(_name);
    }

    function addVoter (string _voterKey) public {
        voters[keccak256(abi.encodePacked(_voterKey))] = true;
    }

    function vote (string _candidateName, string _voterKey) public {
        // require that user has permission to vote
        require(!voters[keccak256(abi.encodePacked(_voterKey))]);

        // require that they haven't voted before
        require(!has_voted[keccak256(abi.encodePacked(_voterKey))]);

        uint _candidateID = candidates_ids[_candidateName];
        // require a valid candidate
        require(candidates[_candidateID].definedCandidate == true);

        // update candidate vote Count
        candidates[_candidateID].voteCount ++;

        // trigger voted event
        votedEvent(_candidateName);
    }

    function showVotingResult() public returns (string[], uint[]){
        string[] memory candidateNames = new string[](numCandidates);
        uint[]    memory voteCounts = new uint[](numCandidates);

        for (uint i = 0; i < numCandidates; i++) {
            candidateNames[i] = candidates[i].name;
            voteCounts[i] = candidates[i].voteCount;
        }

        return (candidateNames, voteCounts);
    }

    function getNumCandidates() public returns (uint) {
        return numCandidates;
    }
}
'''

compiled_sol = compile_source(contract_source_code) # Compiled source code


contract_interface = compiled_sol['<stdin>:Voting']


# web3.py instance
w3 = Web3(Web3.HTTPProvider("http://10.0.0.20:8545"))

from web3.middleware import geth_poa_middleware

# inject the poa compatibility middleware to the innermost layer
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

## set pre-funded account as sender

w3.eth.setGasPriceStrategy(value_based_gas_price_strategy)

w3.eth.defaultAccount = w3.eth.accounts[0]

address = w3.toChecksumAddress('0x3590aca93338b0721966a8d0c96ebf2c4c87c544') 
#
w3.personal.unlockAccount(address, 'word')

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

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

with open('data.json', 'w') as outfile:
    data = {
        "abi": contract_interface['abi'],
        "contract_address": tx_receipt.contractAddress
    }
    json.dump(data, outfile, indent=4, sort_keys=True)

