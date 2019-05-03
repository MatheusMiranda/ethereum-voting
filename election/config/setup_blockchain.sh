cd /etc/blockchain_config/

#Remove old blockchain data
rm -rf datadir 
mkdir datadir

#Setup accounts
geth --datadir=./datadir --password ./password_1.txt account new >> accounts.txt
geth --datadir=./datadir --password ./password_1.txt account new >> accounts.txt

#Init BlockChain
geth --datadir ./datadir init genesis_block.json
