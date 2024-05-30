// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {IERC721} from "../common/IERCS/IERC721.sol";

import {SecuredContract} from "../common/securedContract/SecuredContract.sol";

import {Oracle} from "../oracle/Oracle.sol";

contract VRFCaller is SecuredContract {
    Oracle oracle;

    string public functionCalled;
    uint128 public requestId;
    address public msgSender;
    uint24 public randomUint;
    uint24[] public randomUints;


    constructor(address _oracleContract) SecuredContract(){
        setOracleContract(_oracleContract);
    }

    receive() external payable{
        
    }

    function setOracleContract(address oracle_addr) public isOwner(msg.sender){
        oracleContract = oracle_addr;
        oracle = Oracle(oracleContract);
    }

    function generateSingleRandUint(uint24 min, uint24 max) public payable {
        oracle.generateSingleRandUint{value: msg.value}(min, max);
    }

    function generateRandUintArray(uint24 min, uint24 max, uint8 quantity) public payable {
        oracle.generateRandUintArray{value: msg.value}(min, max, quantity);
    }

    function fulfillRequestSingleRandUint(uint128 _requestId, uint24 num) public isOracle(msg.sender) {
        functionCalled = "fulfillRequestRandUint_singleUint";
        requestId = _requestId;
        msgSender = msg.sender;
        randomUint = num;
    }
    
    function fulfillRequestRandUintArray(uint128 _requestId, uint24[] memory nums) public isOracle(msg.sender) {
        functionCalled = "fulfillRequestRandUint_uintArray";
        requestId = _requestId;
        msgSender = msg.sender;
        randomUints = nums;
    }
}