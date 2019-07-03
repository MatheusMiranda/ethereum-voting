To cast a vote for a candidate use the following request:

curl -H "Content-Type: application/json" --request POST -d '{"candidate_name": "Candidate_1", "username":"user_1", "encrypted_password": "asd1jk23jk12j3k12", "user_id": "14" }' http://localhost:5000/blockchain/cast_vote

To add a candidate:

curl -H "Content-Type: application/json" --request POST -d '{"candidate_name":"Candidate_1"}' http://localhost:5000/blockchain/add_candidate

To add a voter:

curl -H "Content-Type: application/json" --request POST -d '{"username":"user_1", "encrypted_password": "asd1jk23jk12j3k12", "user_id": "14" }' http://localhost:5000/blockchain/add_voter

To generate the accounts run the commands:

sudo docker-compose run --rm geth-client /etc/blockchain_config/setup_blockchain.sh

sudo docker-compose run --rm ethereum-compiler python /opt/election/config/setup_accounts.py

sudo docker-compose run --rm geth-client /etc/blockchain_config/init_blockchain.sh

To compile the Voting contract run the command:

sudo docker-compose run --rm ethereum-compiler make deploy-contract

To list all candidates:

curl -H "Content-Type: application/json" --request GET http://localhost:5000/blockchain/show_election_results
