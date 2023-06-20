pragma solidity >=0.4.25 <0.6.0;

contract SimpleMarketplace {
    enum StateType { 
        ItemAvailable,
        Bidding,
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

    constructor(string memory _description, uint256 _askingPrice) public {
        instanceOwner = msg.sender;
        askingPrice = _askingPrice;
        description = _description;
        state = StateType.ItemAvailable;
        highestBid = 0;
        highestBidder = address(0);
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
