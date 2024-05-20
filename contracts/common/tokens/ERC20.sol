// SPDX-License-Identifier: MIT

pragma solidity ^0.8.25;

import {IERC20} from "../IERCS/IERC20.sol";
import {IERC165} from "../IERCS/IERC165.sol";

contract ERC20 {
    address private token_owner;
    string private token_name;
    string private token_symbol;
    uint8 private token_decimals;
    uint256 private max_supply;
    uint256 private current_supply;

    mapping (address holder => uint256 balance) balances;
    mapping(address holder => mapping(address spender => uint256)) private _allowances;
    mapping(address admin_addr => bool status) private admin_addrs;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Mint(address indexed _to, uint256 _value);
    event Burn(address indexed _from, uint256 _value);

    constructor(string memory _token_name, string memory _token_symbol, uint8 _token_decimals, uint _max_supply) {
        token_owner = msg.sender;
        token_name = _token_name;
        token_symbol = _token_symbol;
        token_decimals = _token_decimals;
        max_supply = _max_supply;
    }

    modifier is_owner(address addr) virtual {
        require(addr == token_owner, "is_owner error: Not authorized");
        _;
    }

    modifier is_owner_or_admin(address addr) virtual {
        require(addr == token_owner || admin_addrs[addr], "is_owner_or_admin error: Not Authorized");
        _;
    }

    modifier is_owner_self_or_admin(address requester_addr, address to_address) virtual {
        require(requester_addr == token_owner || requester_addr == to_address || admin_addrs[requester_addr], "is_owner_self_or_admin error: Not Authorized");
        _;
    }

    function name() virtual public view returns (string memory) {
        return token_name;
    }

    function symbol() virtual public view returns (string memory) {
        return token_symbol;
    }

    function decimals() virtual public view returns (uint8) {
        return token_decimals;
    }
    function totalSupply() virtual public view returns (uint256) {
        return current_supply;
    }

    function balanceOf(address _holder) virtual public view returns (uint256 balance) {
        return balances[_holder];
    }
    function transfer(address _to, uint256 _value) virtual public returns (bool success) {
        return transferFrom(msg.sender, _to, _value);
 
    }

    function transferFrom(address _from, address _to, uint256 _value) virtual public returns (bool success) {
        require(_from != address(0), "transferFrom error: Invalid from addres");
        require(balances[_from] >= _value, "transferFrom error: Not enough Balance");

        if(_from != msg.sender && ! admin_addrs[msg.sender]) {
            _spend_allowance(_from, msg.sender, _value);
        }

        if (_to == address(0)) {
            _burn(_from, _value);
            return true;
        }

        balances[_from] -= _value;
        balances[_to] += _value;
        emit Transfer(_from, _to, _value);
        return true;

    }
    function approve(address _spender, uint256 _value) virtual public returns (bool success) {
        require(_spender != address(0), "approve error: Invalid from addres");
        require(msg.sender != address(0), "approve error: Invalid to address");

        _allowances[msg.sender][_spender] = _value;
        
        emit Approval(msg.sender, _spender, _value);

        return true;
    }
    function allowance(address _from, address _spender) virtual public view returns (uint256 remaining) {
        return _allowances[_from][_spender];
    }

    function is_admin(address _from) virtual public view returns(bool) {
        return admin_addrs[_from];
    }

    function _spend_allowance(address _from, address _spender, uint256 _value) virtual internal {
        require(allowance(_from, msg.sender) >= _value, "Allowance error: Amount approved is not enough");

        _allowances[_from][_spender] -= _value;
    }

    function update_admin_address(address admin_addr, bool active) is_owner(msg.sender) virtual public {
        admin_addrs[admin_addr] = active;
    }

    function mint(address _to, uint _amount) is_owner_or_admin(msg.sender) virtual public {
        require(_to != address(0), "mint error: invalid _to address");
        if (max_supply >0) {
            require(current_supply + _amount <= max_supply);
        }
        _mint(_to, _amount);
    }

    function _mint(address _to, uint _amount) virtual internal {
        current_supply += _amount;
        balances[_to] += _amount;

        emit Mint(_to, _amount);
    }

    function burn(address _from, uint _amount) is_owner_self_or_admin(msg.sender, _from) virtual public {
        require(_from != address(0), "burn error: invalid _from address");
        require(balances[_from] >= _amount, "burn error: not enough balance");
        _burn(_from, _amount);
    }

    function _burn(address _from, uint _amount) virtual internal{
        current_supply -= _amount;
        balances[_from] -= _amount;
        emit Burn(_from, _amount);
    }

    function supportsInterface(bytes4 interfaceID) external pure returns (bool) {
        return (type(IERC20).interfaceId == interfaceID || type(IERC165).interfaceId == interfaceID);
    }
}

