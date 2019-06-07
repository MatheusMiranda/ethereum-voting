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
	mapping (bytes32 => bool) voters;
	mapping (bytes32 => bool) has_voted;

	event votedEvent (
		string _candidateName
	);

	event addedCandidadeEvent (
		string _candidateName
	);

	function Voting () public {
	}

	function addCandidate(string _name) public {
		numCandidates ++;
		candidates[_name] = Candidate(numCandidates,_name,0,true);
		addedCandidadeEvent(_name);
	}

	function showVotingState(string _candidateName) public returns (uint) {
		return (
				candidates[_candidateName].voteCount
				);
	}

	function addVoter (string _voterKey) public {
		voters[keccak256(abi.encodePacked(_voterKey))] = true;
	}

	function vote (string _candidateName, string _voterKey) public {
		// require that user has permission to vote
		require(!voters[keccak256(abi.encodePacked(_voterKey))]);

		// require that they haven't voted before
		require(!has_voted[keccak256(abi.encodePacked(_voterKey))]);

		// require a valid candidate
		require(candidates[_candidateName].definedCandidate == true);

		// update candidate vote Count
		candidates[_candidateName].voteCount ++;

		// trigger voted event
		votedEvent(_candidateName);
	}
}

