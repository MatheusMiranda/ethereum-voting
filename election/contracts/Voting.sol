pragma solidity 0.4.20;

contract Voting {
	struct Candidate {
		string name;
		string party; 
		bool definedCandidate; 
	}

	uint numCandidates; 
	mapping (uint => Candidate) candidates;
	mapping (address => bool) voters;

	function vote (uint _candidateId) public {
		// require that they haven't voted before
		require(!voters[msg.sender]);

		// require a valid candidate
		require(candidates[candidateId].doesExist == true);

		// record that voter has voted
		voters[msg.sender] = true;

		// update candidate vote Count
		candidates[_candidateId].voteCount ++;

		// trigger voted event
		votedEvent(_candidateId);
	}
}
