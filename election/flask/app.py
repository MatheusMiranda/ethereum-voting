import json
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3
import hashlib


app = Flask(__name__)


w3 = Web3(Web3.HTTPProvider("http://10.0.0.20:8545"))

from web3.middleware import geth_poa_middleware

# inject the poa compatibility middleware to the innermost layer
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

address = w3.toChecksumAddress('0x3590aca93338b0721966a8d0c96ebf2c4c87c544')

w3.personal.unlockAccount(address, 'word')

w3.eth.defaultAccount = w3.eth.accounts[0]

with open("/opt/election/data.json", 'r') as f:
    datastore = json.load(f)
abi = datastore["abi"]
contract_address = datastore["contract_address"]

# Create the contract instance with the newly-deployed address
voting = w3.eth.contract(
    address=contract_address, abi=abi,
)


def generate_user_hash(body):
    candidate_name = body["candidate_name"]
    username = body["username"]
    password = body["password"]
    user_id = body["user_id"]

    user_string = username + password + user_id
    hash_object = hashlib.sha512(user_string.encode('UTF-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


# api to set new user every api call
@app.route("/blockchain/voting", methods=['POST'])
def cast_vote():
    body = request.get_json()

    if "candidate_name" not in body:
        return jsonify("Candidate name must be provided to cast a vote!"), 422

    candidate_name = body["candidate_name"]

    user_hash = generate_user_hash(body)
        
    tx_hash = voting.functions.vote(
        candidate_name, username, password
    )

    #print("\n\n\n\n")
    #web3.eth.getTransaction(tx_hash)
    #print("\n\n\n

    w3.eth.waitForTransactionReceipt(tx_hash)
    voting_data = voting.functions.showVotingState(candidate_name).call()
    return jsonify({candidate_name: voting_data}), 200

@app.route("/blockchain/add_candidate", methods=['POST'])
def add_candidate():
    body = request.get_json()

    if "candidate_name" not in body:
        return jsonify("Candidate name is a required field!"), 422

    candidate_name = body["candidate_name"]

    tx_hash = voting.functions.addCandidate(
        candidate_name
    )

    tx_hash = tx_hash.transact()
    # Wait for transaction to be mined...;

    w3.eth.waitForTransactionReceipt(tx_hash)
    voting_data = voting.functions.showVotingState(candidate_name).call()
    return jsonify({status: "Candidate was sucessfully added!"}), 200

@app.route("/blockchain/add_voter", methods=['POST'])
def add_voter():
    body = request.get_json()

    if "username" not in body:
        return jsonify("Username name is a required field!"), 422
    elif "password" not in body;
        return jsonify("Password is a required field!"), 422

    candidate_name = body["candidate_name"]

    tx_hash = voting.functions.addCandidate(
        candidate_name
    )

    user_hash = generate_user_hash(body)

    tx_hash = tx_hash.transact()
    # Wait for transaction to be mined...;

    w3.eth.waitForTransactionReceipt(tx_hash)
    voting_data = voting.functions.showVotingState(candidate_name).call()
    return jsonify({status: "Voter was sucessfully added!"}), 200
