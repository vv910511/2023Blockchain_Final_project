# 2023Blockchain_Final_project
# 區塊鏈期末專案-簡易市場競標系統  
本專案之目的為以區塊鏈技術進行簡易市場競標活動  

**附件檔案**  
* "SimpleMarket Bidding.sol":本專案所使用之智能合約  
* "app.py":以Python結合Web3與Flask完成基本功能設定    
* "index.html":前端操作頁面  

## 程式說明  

前端網頁
```python  

from flask import Flask, render_template, request
from web3 import Web3
import json

app = Flask(__name__)

# 建立 Web3 實例
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
#智能合約之ABI
abi = json.loads('[{"constant":true,"inputs":[],"name":"askingPrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"acceptHighestBid","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"bids","outputs":[{"name":"bidder","type":"address"},{"name":"bidPrice","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getHighestBid","outputs":[{"name":"","type":"address"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"description","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_minimumBid","type":"uint256"}],"name":"setMinimumBid","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"highestBidder","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"instanceOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"state","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"highestBid","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"placeBid","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[{"name":"_description","type":"string"},{"name":"_minimumBid","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
contract = None

#首頁相關數值設定(index)
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

#跳轉頁面相關數值設定(/place_bid)
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
#取得最高出價及出價者
def get_highest_bid():
    bidder, bid_price = contract.functions.getHighestBid().call()
    return bidder, bid_price

if __name__ == '__main__':
    app.run()
```  
智能合約
```solidity
pragma solidity >=0.4.25 <0.6.0;

contract SimpleMarketplace {
    enum StateType { 
        ItemAvailable,
        Bidding,
        Accepted,
        AuctionEnded
    }
    
    struct Bid {
        address bidder;
        uint256 bidPrice;
    }

    address public instanceOwner;
    string public description;
    uint256 public askingPrice;
    StateType public state;
    Bid[] public bids;
    uint256 public highestBid;
    address public highestBidder;

    constructor(string memory _description, uint256 _minimumBid) public {
        instanceOwner = msg.sender;
        description = _description;
        state = StateType.Bidding;
        highestBid = 0;
        highestBidder = address(0);
        setMinimumBid(_minimumBid);
    }

    function setMinimumBid(uint256 _minimumBid) public {
        require(msg.sender == instanceOwner, "Only instance owner can set minimum bid");
        askingPrice = _minimumBid;
    }

    function placeBid() public payable {
        require(state == StateType.Bidding, "Cannot place bid at the moment");
        require(msg.value > 0, "Bid price must be greater than zero");
        require(msg.value > highestBid, "Bid price must be greater than current highest bid");

        if (highestBidder != address(0)) {
            // Return the funds to the previous highest bidder
            highestBidder.transfer(highestBid);
        }

        highestBid = msg.value;
        highestBidder = msg.sender;

        bids.push(Bid(msg.sender, msg.value));
    }

    function acceptHighestBid() public {
        require(state == StateType.Bidding, "Cannot accept bid at the moment");
        require(msg.sender == instanceOwner, "Only instance owner can accept bids");

        state = StateType.AuctionEnded;
    }

    function getHighestBid() public view returns (address, uint256) {
        require(state == StateType.Bidding, "No active bidding");

        return (highestBidder, highestBid);
    }
}

```  
## 成果展示
![image](https://github.com/vv910511/Project_data/blob/main/%E5%9C%96%E7%89%871.png)
![gif](https://github.com/vv910511/Project_data/blob/main/Gif2.gif)
## 參考資料
**簡易一對一市場**  
* [simple-marketplace](https://github.com/Azure-Samples/blockchain/blob/master/blockchain-workbench/application-and-smart-contract-samples/simple-marketplace/readme.md)
**使用Solidity開發Smart Contract** 
* [Smart Contract 開發 - 使用 Solidity :: 2019 iT 邦幫忙鐵人賽](https://ithelp.ithome.com.tw/users/20092025/ironman/1759?page=2)
* [Solidity — Solidity 0.8.21 documentation](https://docs.soliditylang.org/en/latest/)
**區塊鏈開發** 
* [區塊鏈應用開發實戰 :: 2019 iT 邦幫忙鐵人賽](https://ithelp.ithome.com.tw/users/20111706/ironman/1689)

