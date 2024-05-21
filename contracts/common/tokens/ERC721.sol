// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Base64.sol";

import {IERC721} from "../IERCS/IERC721.sol";
import {IERC165} from "../IERCS/IERC165.sol";

import {ERC721Utils} from "../utils/ERC721.sol";

contract ERC721 {
    bool internal reentrancyLock = false;

    uint256 internal current_tokenId;
    address internal contract_owner;
    string internal token_name;
    string internal token_symbol;
    uint256 internal max_supply;
    uint256 internal current_supply;

    mapping (address admin_addr => bool status) internal admin_addrs;

    mapping (uint token_id => address approved) internal token_approvals;
    mapping (address holder => mapping(address approved => bool status)) internal holder_approvals;

    mapping (uint token_id => address holder) internal tokens;
    mapping (address holder => uint total_tokens_holding) internal balances;


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

    modifier is_holder(address _from, uint256 _tokenId) virtual {
        require(tokens[_tokenId] == _from, "is_holder error: Token does not belong to _from address");
        _;
    }

    modifier token_exists(uint256 _tokenId) virtual{
        require(tokens[_tokenId] != address(0));
        _;
    }

    modifier nonReentrant() virtual {
        require(!reentrancyLock, "nonReentrant Error: reentrant call");
        reentrancyLock = true;
        _;
        reentrancyLock = false;
    }

    constructor(string memory _token_name, string memory _token_symbol,  uint _max_supply, address[] memory _admins) {
        contract_owner = msg.sender;
        token_name = _token_name;
        token_symbol = _token_symbol;
        max_supply = _max_supply;

        for (uint i=0; i < _admins.length; i++) {
            admin_addrs[_admins[i]] = true;
        }
    }

    function name() external view virtual returns(string memory)  {
        return token_name;
    }

    function symbol() external view virtual returns(string memory) {
        return token_symbol;
    }

    function total_supply() external view virtual returns (uint) {
        return current_supply;
    }

    function balanceOf(address _owner) external virtual view returns (uint256) {
        return balances[_owner];
    }
    function ownerOf(uint256 _tokenId) external virtual view returns (address) {
        return tokens[_tokenId];
    }

    // function contractURI() public view virtual returns (string memory){
    //     bytes memory _dataURI = abi.encodePacked(
    //         "data:application/json;utf8,",
    //         '{',
    //         '}'
    //     );

    //     return string(_dataURI);
    // }

    function transferFrom(address _from, address _to, uint256 _tokenId) external virtual is_owner_self_admin_or_approved(msg.sender, _from, _tokenId) is_holder(_from, _tokenId) {
        _transfer(_from, _to, _tokenId);
        emit Transfer(_from, _to, _tokenId);
    }

    function safeTransferFrom(address _from, address _to, uint256 _tokenId) public virtual is_owner_self_admin_or_approved(msg.sender, _from, _tokenId) {
        safeTransferFrom(_from, _to, _tokenId, "");
    }
    function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes memory _data) public virtual is_owner_self_admin_or_approved(msg.sender, _from, _tokenId) nonReentrant {
        _transfer(_from, _to, _tokenId);
        ERC721Utils.CallOnReceived(msg.sender, address(0), _to, _tokenId, _data);
    }

    function approve(address _approved, uint256 _tokenId) external virtual is_holder(msg.sender, _tokenId) token_exists(_tokenId){
        token_approvals[_tokenId] = _approved;
        emit Approval(msg.sender, _approved, _tokenId);
    }

    function is_approved(address _operator, uint256 _tokenId) public view virtual returns(bool) {
        return token_approvals[_tokenId] == _operator;
    }

    function unapprove(uint256 _tokenId) external virtual is_holder(msg.sender, _tokenId) token_exists(_tokenId) {
        
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

    function supportsInterface(bytes4 interfaceID) external pure virtual returns (bool){
        return (type(IERC721).interfaceId == interfaceID || type(IERC165).interfaceId == interfaceID);
    }

    function mint(address _to) public is_owner_or_admin(msg.sender) virtual returns (bool success) {
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
        require(max_supply == 0 || current_tokenId < max_supply, "Mint error: Above max supply limit");

        current_tokenId += 1;

        tokens[current_tokenId] = _to;
        balances[_to] += 1;
        
        current_supply += 1;

        emit Transfer(address(0), _to, current_tokenId);

        return current_supply;
    }

    function _safeMint(address to) internal virtual {
        _safeMint(to, "");
    }

    function _safeMint(address to, bytes memory data) internal virtual {
        uint256 token_id = _mint(to);

        ERC721Utils.CallOnReceived(msg.sender, address(0), to, token_id, data);
    }

    function _transfer(address _from, address _to, uint _tokenId) internal virtual{
        require(_from != address(0));
        require(tokens[_tokenId] == _from);
        require(_from != _to);

        tokens[_tokenId] = _to;
        balances[_from] -= 1;
        balances[_to] += 1;
        token_approvals[_tokenId] = address(0);
        
        emit Transfer(_from, _to, _tokenId);
    }

    function update_admin_address(address admin_addr, bool active) is_owner(msg.sender) virtual public {
        admin_addrs[admin_addr] = active;
    }

    function is_admin(address _from) public view virtual returns(bool){
        return admin_addrs[_from];
    }

}