pragma solidity 0.4.20;

contract Voting {
	struct Candidate {
		string name;
		string party; 
		uint voteCount;
		bool definedCandidate; 
	}

	uint numCandidates; 
	mapping (uint => Candidate) candidates;
	mapping (address => bool) voters;

	function addCandidate(string name) public {
		uint candidateID = numCandidates++;

		candidates[candidateID] = Candidate(name,party,true);
		AddedCandidate(candidateID);
	}

	function vote (uint _candidateID) public {
		// require that they haven't voted before
		require(!voters[msg.sender]);

		// require a valid candidate
		require(candidates[candidateID].doesExist == true);

		// record that voter has voted
		voters[msg.sender] = true;

		// update candidate vote Count
		candidates[_candidateID].voteCount ++;

		// trigger voted event
		votedEvent(_candidateID);
	}
}
