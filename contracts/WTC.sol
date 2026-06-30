// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract WTC {
    string public name = "WCoins Token";
    string public symbol = "WTC";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    address public bridgeAddress;
    uint256 public constant MAX_SUPPLY = 100_000_000 * 10 ** 18;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event BridgeUpdated(address indexed oldBridge, address indexed newBridge);
    event TokensMinted(address indexed to, uint256 amount, string fromChain);
    event TokensBurned(address indexed from, uint256 amount, string toChain);

    modifier onlyOwner() { require(msg.sender == owner, "only owner"); _; }
    modifier onlyBridge() { require(msg.sender == bridgeAddress, "only bridge"); _; }

    constructor() {
        owner = msg.sender;
        _mint(msg.sender, 10_000_000 * 10 ** 18);
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(to != address(0), "zero address");
        require(balanceOf[msg.sender] >= amount, "insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(allowance[from][msg.sender] >= amount, "insufficient allowance");
        require(balanceOf[from] >= amount, "insufficient balance");
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }

    function _mint(address to, uint256 amount) internal {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    function _burn(address from, uint256 amount) internal {
        require(balanceOf[from] >= amount, "insufficient balance");
        totalSupply -= amount;
        balanceOf[from] -= amount;
        emit Transfer(from, address(0), amount);
    }

    function mintByBridge(address to, uint256 amount, string calldata fromChain) external onlyBridge {
        require(totalSupply + amount <= MAX_SUPPLY, "max supply");
        _mint(to, amount);
        emit TokensMinted(to, amount, fromChain);
    }

    function burnByBridge(uint256 amount, string calldata toChain) external {
        _burn(msg.sender, amount);
        emit TokensBurned(msg.sender, amount, toChain);
    }

    function setBridge(address _b) external onlyOwner {
        require(_b != address(0), "invalid");
        emit BridgeUpdated(bridgeAddress, _b);
        bridgeAddress = _b;
    }
}
