pragma solidity 0.4.20;

contract Voter {

	struct Voter {
		string identifier;
		bool authorizedVoter; 
	}

	uint private nonce;
	mapping (address => bool) private voters;

	function Voter () public {
	}  

	function addVoter (string _voterName, string _voterKey) public {
		nonce ++;

		_voterIdentifier = generateVoterIdentifier(_voterName, _voterKey, nonce)

		voters[_voterIdentifier] = true;

		// trigger voted event
		// votedEvent(_candidateName);
	}

	function generateVoterIdentifier (string _voterName, string _voterKey) private {
		return keccak256(_voterName, _voterKey, nonce);
	}
}
