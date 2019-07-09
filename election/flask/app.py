import json
from flask import Flask, Response, request, jsonify
from marshmallow import Schema, fields, ValidationError
from web3 import Web3
import hashlib
import sys


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
    username = body["username"]
    password = body["encrypted_password"]
    user_id = body["user_id"]

    user_string = username + password + user_id
    hash_object = hashlib.sha512(user_string.encode('UTF-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


# api to set new user every api call
@app.route("/blockchain/cast_vote", methods=['POST'])
def cast_vote():
    body = request.get_json()

    if "candidate_name" not in body:
        return jsonify({"error": "Candidate name must be provided to cast a vote!"}), 422
    if "username" not in body:
        return jsonify("Username name is a required field!"), 422
    elif "encrypted_password" not in body:
        return jsonify("Encrypted password is a required field!"), 422
    elif "user_id" not in body:
        return jsonify("User id is a required field!"), 422

    user_hash = generate_user_hash(body)

    candidate_name = body["candidate_name"]

    tx_hash = voting.functions.vote(
        candidate_name, user_hash
    )

    tx_hash = tx_hash.transact()

    w3.eth.waitForTransactionReceipt(tx_hash)

    transaction_hash = w3.eth.getTransaction(tx_hash)['hash']
    transaction_data = w3.eth.getTransaction(transaction_hash)
    function, transaction_input = voting.decode_function_input(transaction_data.input)

    return jsonify({"transaction_hash": transaction_hash.hex(),
                    "status": "success", "input": transaction_input}), 200

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

    w3.eth.waitForTransactionReceipt(tx_hash)
    return jsonify({"status": "Candidate was sucessfully added!"}), 200

@app.route("/blockchain/add_voter", methods=['POST'])
def add_voter():
    body = request.get_json()

    if "username" not in body:
        return jsonify("Username name is a required field!"), 422
    elif "encrypted_password" not in body:
        return jsonify("Encrypted password is a required field!"), 422
    elif "user_id" not in body:
        return jsonify("User id is a required field!"), 422

    user_hash = generate_user_hash(body)

    tx_hash = voting.functions.addVoter(
        user_hash
    )

    transaction_hash = tx_hash.transact()

    w3.eth.waitForTransactionReceipt(transaction_hash)

    return jsonify({"transaction_hash": transaction_hash.hex(),
                    "status": "Voter was sucessfully added!"}), 200

@app.route("/blockchain/show_election_results", methods=['GET'])
def show_election_results():
    candidates, votes = voting.functions.showVotingResult().call()

    return jsonify({"Election Result": list(candidates)}), 200

@app.route("/blockchain/manage_base_account", methods=['POST'])
def manage_base_account():
    body = request.get_json()

    if "base_account_address" not in body:
        return jsonify("Base account address is a required field!"), 422

    base_account_address = body["base_account_address"]

    tx_hash = voting.functions.manageBaseAccount(
        base_account_address
    )

    transaction_hash = tx_hash.transact()

    w3.eth.waitForTransactionReceipt(transaction_hash)

    return jsonify({"transaction_hash": transaction_hash.hex()}), 200
