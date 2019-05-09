# Create Blockchain accounts
sudo docker-compose run --rm geth-client /etc/blockchain_config/setup_blockchain.sh

# Setup accounts at Genesis Block
sudo docker-compose run --rm ethereum-compiler python /opt/election/config/setup_accounts.py
 
# Create Blockchain
sudo docker-compose run --rm geth-client /etc/blockchain_config/init_blockchain.sh

# Run Blockchain node
sudo docker-compose run --rm geth-client geth --port 3000 --networkid 12345678 --nodiscover --datadir=./datadir --maxpeers=0  --rpc --rpcport 8545 --rpcaddr 127.0.0.1 --rpccorsdomain "*" --rpcapi "eth,net,web3,personal,miner"

# Compile and deploy contract
sudo docker-compose run --rm ethereum-compiler make deploy-contract
