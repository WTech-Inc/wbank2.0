// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWTC {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function mintByBridge(address to, uint256 amount, string calldata fromChain) external;
    function owner() external view returns (address);
}

contract WTCBridge {
    IWTC public wtcToken;
    uint256 public bridgeFee;
    bool public paused;
    address public owner;

    mapping(address => bool) public relayers;
    mapping(address => uint256) public nonces;

    event TokensLocked(address indexed user, uint256 amount, uint256 targetChainId, string chainName, uint256 nonce, uint256 timestamp);
    event TokensUnlocked(address indexed user, uint256 amount, uint256 sourceChainId, string chainName, uint256 nonce, address indexed relayer);

    modifier onlyRelayer() { require(relayers[msg.sender], "only relayer"); _; }
    modifier onlyOwner() { require(msg.sender == owner, "only owner"); _; }

    constructor(address _wtc) {
        require(_wtc != address(0), "invalid");
        wtcToken = IWTC(_wtc);
        owner = msg.sender;
        relayers[msg.sender] = true;
    }

    function bridgeOut(uint256 amount, uint256 targetChainId, string calldata chainName) external {
        require(!paused, "paused");
        require(amount > 0, "amount > 0");
        require(amount <= wtcToken.balanceOf(msg.sender), "insufficient balance");
        uint256 fee = (amount * bridgeFee) / 10000;
        uint256 bridgeAmount = amount - fee;
        wtcToken.transferFrom(msg.sender, address(this), amount);
        if (fee > 0) wtcToken.transfer(owner, fee);
        uint256 nonce = nonces[msg.sender]++;
        emit TokensLocked(msg.sender, bridgeAmount, targetChainId, chainName, nonce, block.timestamp);
    }

    function completeBridgeIn(address user, uint256 amount, uint256 sourceChainId, string calldata chainName, uint256 userNonce) external onlyRelayer {
        require(!paused, "paused");
        wtcToken.mintByBridge(user, amount, chainName);
        emit TokensUnlocked(user, amount, sourceChainId, chainName, userNonce, msg.sender);
    }

    function setPaused(bool p) external onlyOwner { paused = p; }
    function setFee(uint256 f) external onlyOwner { require(f <= 1000, "max 10%"); bridgeFee = f; }
    function addRelayer(address r) external onlyOwner { relayers[r] = true; }
    function removeRelayer(address r) external onlyOwner { relayers[r] = false; }
    function emergencyWithdraw() external onlyOwner {
        uint256 b = wtcToken.balanceOf(address(this));
        require(b > 0); wtcToken.transfer(owner, b);
    }
}
