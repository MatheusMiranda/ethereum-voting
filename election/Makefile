start-blockchain:
	sudo docker-compose up --build -d geth-bootnode geth-dev-miner-1 geth-dev-miner-2 geth-dev-node geth-dev-swarm-1 geth-dev-swarm-2 geth-explore

compile-contract:
	sudo docker-compose run --rm ethereum-compiler python3 /opt/election/compile_contract.py

start-api:
	sudo docker-compose up --build -d voting-api
