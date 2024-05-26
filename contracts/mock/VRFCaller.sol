// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {IERC721} from "../common/IERCS/IERC721.sol";

import {SecuredContract} from "../common/securedContract/SecuredContract.sol";

import {Oracle} from "../oracle/Oracle.sol";

contract VRFCaller is SecuredContract {
    Oracle oracle;

    string public functionCalled;
    uint public requestId;
    address public msgSender;
    uint public randomUint;
    uint[] public randomUints;


    constructor(address _oracleContract) SecuredContract(){
        setOracleContract(_oracleContract);
    }

    function setOracleContract(address oracle_addr) public isOwner(msg.sender){
        oracleContract = oracle_addr;
        oracle = Oracle(oracleContract);
    }

    function fulfillRequestSingleRandUint(uint _requestId, uint num) public isOracle(msg.sender) {
        functionCalled = "fulfillRequestRandUint_singleUint";
        requestId = _requestId;
        msgSender = msg.sender;
        randomUint = num;
    }
    
    function fulfillRequestRandUintArray(uint _requestId, uint[] memory nums) public isOracle(msg.sender) {
        functionCalled = "fulfillRequestRandUint_uintArray";
        requestId = _requestId;
        msgSender = msg.sender;
        randomUints = nums;
    }
}