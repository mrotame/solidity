// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.25;

import {IERC721} from "../IERCS/IERC721.sol";
import {IERC165} from "../IERCS/IERC165.sol";

import {ERC721Utils} from "../utils/ERC721.sol";

contract ERC721 {
    uint256 private current_token_id;
    address private contract_owner;
    string private token_name;
    string private token_symbol;
    uint256 private max_supply;
    uint256 private current_supply;
    mapping (address admin_addr => bool status) private admin_addrs;

    mapping (uint token_id => address approved) private token_approvals;
    mapping (address holder => mapping(address approved => bool status)) private holder_approvals;

    mapping (uint token_id => address holder) private holders;
    mapping (address holder => uint total_tokens_holding) private balances;


    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);
    event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
    event ApprovalForAll(address indexed _owner, address indexed _operator, bool _approved);

    modifier is_owner(address addr) virtual {
        require(addr == contract_owner, "is_owner error: Not authorized");
        _;
    }

    modifier is_owner_or_admin(address addr) virtual {
        require(addr == contract_owner || admin_addrs[addr], "is_owner_or_admin error: Not Authorized");
        _;
    }

    modifier is_owner_self_or_admin(address requester_addr, address from_address) virtual {
        require(
            requester_addr == contract_owner ||
            requester_addr == from_address ||
            admin_addrs[requester_addr], "is_owner_self_or_admin error: Not Authorized");
        _;
    }

    modifier is_owner_self_admin_or_approved(address requester_addr, address from_address, uint token_id) virtual {
        require(
            requester_addr == contract_owner ||
            requester_addr == from_address ||
            admin_addrs[requester_addr] ||
            token_approvals[token_id] == requester_addr ||
            holder_approvals[from_address][requester_addr]
            ,"is_owner_self_admin_or_approved error: Not Authorized");
        _;
    }

    modifier is_holder(address _from, uint _token_id) virtual {
        require(holders[_token_id] == _from, "is_holder error: Token does not belong to _from address");
        _;
    }

    constructor(string memory _token_name, string memory _token_symbol,  uint _max_supply) {
        contract_owner = msg.sender;
        token_name = _token_name;
        token_symbol = _token_symbol;
        max_supply = _max_supply;
    }

    function name() external view returns(string memory) {
        return token_name;
    }

    function symbol() external view returns(string memory) {
        return token_symbol;
    }

    function total_supply() external view returns (uint) {
        return current_supply;
    }

    function balanceOf(address _owner) external virtual view returns (uint256) {
        return balances[_owner];
    }
    function ownerOf(uint256 _tokenId) external virtual view returns (address) {
        return holders[_tokenId];
    }

    function transferFrom(address _from, address _to, uint256 _tokenId) external virtual is_owner_self_admin_or_approved(msg.sender, _from, _tokenId) is_holder(_from, _tokenId) {
        _transfer(_from, _to, _tokenId);

        emit Transfer(_from, _to, _tokenId);
    }

    function safeTransferFrom(address _from, address _to, uint256 _tokenId) public virtual is_owner_self_admin_or_approved(msg.sender, _from, _tokenId){
        safeTransferFrom(_from, _to, _tokenId, "");
    }
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes memory _data) public virtual is_owner_self_admin_or_approved(msg.sender, _from, _tokenId){
        _transfer(_from, _to, _tokenId);
        ERC721Utils.CallOnReceived(msg.sender, address(0), _to, _tokenId, _data);
    }

    function approve(address _approved, uint256 _tokenId) external virtual {
        token_approvals[_tokenId] = _approved;
    }

    function unapprove(address _unapproved, uint256 _tokenId) external virtual {
        token_approvals[_tokenId] = address(0);
    }

    function setApprovalForAll(address _operator, bool _approved) external virtual {
        holder_approvals[msg.sender][_operator] = _approved;
    }

    function getApproved(uint256 _tokenId) external virtual view returns (address) {
        return token_approvals[_tokenId];
    }
    function isApprovedForAll(address _holder, address _operator) external virtual view returns (bool) {
        return holder_approvals[_holder][_operator];
    }

    function supportsInterface(bytes4 interfaceID) external pure returns (bool) {
        return (type(IERC721).interfaceId == interfaceID || type(IERC165).interfaceId == interfaceID);
    }

    function mint(address _to) public is_owner_or_admin(msg.sender) returns (bool success) {
        _mint(_to);
        return true;
    }

    function safeMint(address _to) public virtual is_owner_or_admin(msg.sender) returns (bool success) {
        _safeMint(_to, "");
        return true;
    }

    function safeMint(address _to, bytes memory _data) public virtual is_owner_or_admin(msg.sender) returns (bool success) {
        _safeMint(_to, _data);
        return true;
    }

    function _mint(address _to) internal virtual returns (uint256 token_id) {
        require(max_supply == 0 || current_token_id < max_supply, "Mint error: Above max supply limit");

        current_token_id += 1;

        holders[current_token_id] = _to;
        balances[_to] += 1;
        
        current_supply += 1;

        emit Transfer(address(0), _to, current_token_id);

        return current_supply;
    }

    function _safeMint(address to) internal {
        _safeMint(to, "");
    }

    function _safeMint(address to, bytes memory data) internal virtual {
        uint256 token_id = _mint(to);

        ERC721Utils.CallOnReceived(msg.sender, address(0), to, token_id, data);
    }

    function _transfer(address _from, address _to, uint _token_id) internal virtual{
        require(_from != address(0));
        require(holders[_token_id] == _from);
        require(_from != _to);

        holders[_token_id] = _to;
        balances[_from] -= 1;
        balances[_to] += 1;

        emit Transfer(_from, _to, _token_id);
    }

    function update_admin_address(address admin_addr, bool active) is_owner(msg.sender) virtual public {
        admin_addrs[admin_addr] = active;
    }

    function is_admin(address _from) public view returns(bool){
        return admin_addrs[_from];
    }

}