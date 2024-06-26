// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {IERC20} from "../IERCS/IERC20.sol";
import {IERC165} from "../IERCS/IERC165.sol";
import {SecuredContract} from "../securedContract/SecuredContract.sol";

contract ERC20 is SecuredContract {
    string internal token_name;
    string internal token_symbol;
    uint8 internal token_decimals;
    uint256 internal max_supply;
    uint256 internal current_supply;

    mapping (address holder => uint256 balance) balances;
    mapping(address holder => mapping(address spender => uint256)) internal _allowances;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Mint(address indexed _to, uint256 _value);
    event Burn(address indexed _from, uint256 _value);

    constructor(string memory _token_name, string memory _token_symbol, uint8 _token_decimals, uint _max_supply, address[] memory _admins) {
        token_name = _token_name;
        token_symbol = _token_symbol;
        token_decimals = _token_decimals;
        max_supply = _max_supply;

        for (uint8 i = 0; i < _admins.length; i++) {
            admin_addrs[_admins[i]] = true;
        }
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

    function _spend_allowance(address _from, address _spender, uint256 _value) virtual internal {
        require(allowance(_from, msg.sender) >= _value, "Allowance error: Amount approved is not enough");

        _allowances[_from][_spender] -= _value;
    }

    function mint(address _to, uint _amount) isOwnerOrAdmin(msg.sender) virtual public {
        require(_to != address(0), "mint error: invalid _to address");
        if (max_supply >0) {
            require(current_supply + _amount <= max_supply, "mint error: Above max supply");
        }
        _mint(_to, _amount);
    }

    function _mint(address _to, uint _amount) virtual internal {
        current_supply += _amount;
        balances[_to] += _amount;

        emit Mint(_to, _amount);
    }

    function burn(address _from, uint _amount) isOwnerOrSelfOrAdmin(msg.sender, _from) virtual public {
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

