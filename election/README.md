To cast a vote for a candidate use the following request:

curl -H "Content-Type: application/json" --request POST -d '{"candidate_name":"Candidate_1", "voter_key":"sdasdf12312512ds"}' http://localhost:5000/blockchain/cast_vote

To add a candidate:

curl -H "Content-Type: application/json" --request POST -d '{"candidate_name":"Candidate_1"}' http://localhost:5000/blockchain/add_candidate

To add a voter:

curl -H "Content-Type: application/json" --request POST -d '{"voter_account":"0x3590aca93338b0721966a8d0c96ebf2c4c87c544"}' http://localhost:5000/blockchain/add_voter

To generate the accounts run the commands:

sudo docker-compose run --rm geth-client /etc/blockchain_config/setup_blockchain.sh

sudo docker-compose run --rm ethereum-compiler python /opt/election/config/setup_accounts.py

sudo docker-compose run --rm geth-client /etc/blockchain_config/init_blockchain.sh

To compile the Voting contract run the command:

sudo docker-compose run --rm ethereum-compiler make deploy-contract

To list all candidates:

curl -H "Content-Type: application/json" --request POST -d {} http://localhost:5000/blockchain/show_election_results
