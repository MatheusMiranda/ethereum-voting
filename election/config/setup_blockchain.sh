#!/bin/bash

cd /etc/blockchain_config/

#Remove old blockchain data
rm -rf datadir 
mkdir datadir

#Setup accounts
geth --datadir=./datadir --password <(echo $PASSWORD_ACCOUNT_1) account new >> accounts.txt
geth --datadir=./datadir --password <(echo $PASSWORD_ACCOUNT_2) account new >> accounts.txt
geth --datadir=./datadir --password <(echo $PASSWORD_ACCOUNT_3) account new >> accounts.txt
geth --datadir=./datadir --password <(echo $PASSWORD_ACCOUNT_4) account new >> accounts.txt
geth --datadir=./datadir --password <(echo $PASSWORD_ACCOUNT_5) account new >> accounts.txt
geth --datadir=./datadir --password <(echo $PASSWORD_ACCOUNT_6) account new >> accounts.txt
