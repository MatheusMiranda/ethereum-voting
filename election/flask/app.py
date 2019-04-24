import json
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3

app = Flask(__name__)


w3 = Web3(Web3.HTTPProvider("http://10.0.0.20:8545"))


# api to set new user every api call
@app.route("/blockchain/voting", methods=['POST'])
def transaction():
    w3.eth.defaultAccount = w3.eth.accounts[1]
    with open("/opt/election/data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

    # Create the contract instance with the newly-deployed address
    voting = w3.eth.contract(
        address=contract_address, abi=abi,
    )

    body = request.get_json()

    if "candidate_name" not in body:
        return jsonify("Candidate name must be provided to cast a vote!"), 422

    candidate_name = body["candidate_name"]
        
    tx_hash = voting.functions.vote(
        candidate_name
    )

    tx_hash = tx_hash.transact()
    # Wait for transaction to be mined...;w

    w3.eth.waitForTransactionReceipt(tx_hash)
    voting_data = voting.functions.showVotingState().call()
    return jsonify({candidate_name: voting_data}), 200
