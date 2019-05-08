To compile the Voting contract run the command:

sudo docker-compose run --rm ethereum-compiler make deploy-contract

To cast a vote for a candidate use the following request:

curl -H "Content-Type: application/json" --request POST -d '{"candidate_name":"Candidate_1"}' http://localhost:5000/blockchain/voting

To generate account run the command:

sudo docker-compose run --rm geth-client /etc/blockchain_config/setup_blockchain.sh
