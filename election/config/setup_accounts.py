import json
import os
import re

accounts_adresses = []

config_path = '/opt/election/config/'

def get_accounts_adresses():
    accounts = open(config_path + 'accounts.json', 'r')
    
    for account in accounts:
        account_address = re.search('{(.*)}', account).group(1)
        accounts_adresses.append(account_address)

def fill_genesis_block_file():
    with open(config_path + 'genesis_block.json') as json_file:  
        data = json.load(json_file)

        for account_address in accounts_adresses:
            data['alloc'][account_address] = {"balance": "100000000000000000000000"}

    os.remove(config_path + 'genesis_block.json')
    with open(config_path + 'genesis_block.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == '__main__':
    get_accounts_adresses()
    fill_genesis_block_file()
