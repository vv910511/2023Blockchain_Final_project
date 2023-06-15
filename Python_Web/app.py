from flask import Flask, render_template, request
from web3 import Web3
import json

app = Flask(__name__)

# 建立 Web3 實例
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

abi = json.loads('[{"constant":true,"inputs":[],"name":"askingPrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"acceptHighestBid","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"bids","outputs":[{"name":"bidder","type":"address"},{"name":"bidPrice","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getHighestBid","outputs":[{"name":"","type":"address"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"description","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_minimumBid","type":"uint256"}],"name":"setMinimumBid","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"highestBidder","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"instanceOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"state","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"highestBid","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"placeBid","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[{"name":"_description","type":"string"},{"name":"_minimumBid","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
contract = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global contract
    bidder = None
    bid_price = None
    if request.method == 'POST':
        contract_address = request.form['contract_address']
        contract = web3.eth.contract(address=contract_address, abi=abi)
        bidder, bid_price = get_highest_bid()
        
    return render_template('index.html', bidder=bidder, bid_price=bid_price)


@app.route('/place_bid', methods=['POST'])
def place_bid():
    bid_price = int(request.form['bid_price'])
    num = request.form['Num']
    
    highest_bidder, highest_bid = get_highest_bid()
    
    if bid_price > highest_bid:
        wallet_address = web3.eth.accounts[int(num)]
        place_bid_transaction = contract.functions.placeBid().transact({
            'from': wallet_address,
            'value': bid_price
        })
        transaction_hash = place_bid_transaction.hex()
        return f'交易已提交，交易Hash：{transaction_hash}'
    else:
        return '您的出價必須高於目前最高出價。'

def get_highest_bid():
    bidder, bid_price = contract.functions.getHighestBid().call()
    return bidder, bid_price

if __name__ == '__main__':
    app.run()