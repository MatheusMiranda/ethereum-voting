pragma solidity 0.4.20;

contract Voting {
	struct Candidate {
		uint id;
		string name;
		uint voteCount;
		bool definedCandidate; 
	}

	uint public numCandidates; 
	mapping (string => Candidate) public candidates;
	mapping (address => bool) public voters;

  event votedEvent (
      uint indexed _candidateId
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

	function vote (uint _candidateName) public {
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
