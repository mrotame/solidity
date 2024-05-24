// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

contract SecuredContract {
    address internal contractOwner;
    address oracleContract;
    bool internal reentrancyLock;

    mapping(address admin_addr => bool status) internal admin_addrs;

    modifier isOwner(address addr) virtual {
        require(addr == contractOwner, "isOwner error: Not authorized");
        _;
    }

    modifier isOracle(address addr) virtual {
        require(msg.sender == oracleContract, "isOracle error: Unauthorized");
        _;
    }

    modifier isOwnerOrAdmin(address addr) virtual {
        require(addr == contractOwner || admin_addrs[addr], "isOwnerOrAdmin error: Not Authorized");
        _;
    }

    modifier isOwnerOrSelfOrAdmin(address requester_addr, address to_address) virtual {
        require(requester_addr == contractOwner || requester_addr == to_address || admin_addrs[requester_addr], "isOwnerOrSelfOrAdmin error: Not Authorized");
        _;
    }

    modifier nonReentrant() virtual {
        require(!reentrancyLock, "nonReentrant Error: reentrant call");
        reentrancyLock = true;
        _;
        reentrancyLock = false;
    }

    constructor() {
        contractOwner = msg.sender;
    }

    function is_admin(address _from) virtual public view returns(bool) {
        return admin_addrs[_from];
    }

    function update_admin_address(address admin_addr, bool active) isOwner(msg.sender) virtual public {
        admin_addrs[admin_addr] = active;
    }

}

