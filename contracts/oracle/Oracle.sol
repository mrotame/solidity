// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {IRequester} from "./IRequester.sol";

import {OracleModifiers} from "./OracleModifiers.sol";

contract Oracle is OracleModifiers{
    constructor(address[] memory _allowedAddresses) {
        contractOwner = msg.sender;

        for (uint i = 0; i < _allowedAddresses.length; i++) {
            allowedAddresses[_allowedAddresses[i]] = true;
        }
    }

    function createRequest(RequestTypes requestType) internal returns (uint){
        currentRequestId += 1; 
        requests[currentRequestId] = msg.sender;
        emit RequestCreated(currentRequestId, msg.sender, requestType);
        return currentRequestId;
    }

    // --------- RandUint Request ---------

    // Generate
    function generateSingleRandUint(uint minNum, uint maxNum) public payable isOwnerOrAllowed(msg.sender) returns (uint){
        uint request = createRequest(RequestTypes.RANDUINT_SINGLE);

        emit RandUintParams(request, maxNum, minNum);

        return request;
    }

    function generateRandUintArray(uint minNum, uint maxNum, uint quantityRequired) public payable isOwnerOrAllowed(msg.sender) returns (uint){
        uint request = createRequest(RequestTypes.RANDUINT_ARRAY);

        emit RandUintParams(request, maxNum, minNum,quantityRequired);

        return request;
    }

    // Fulfill
    function fulfillSingleRandUintRequest(uint requestId, uint num) public isOwner(msg.sender) fulfillRequest(requestId) {
        IRequester(requests[requestId]).fulfillRequestSingleRandUint(requestId, num);
    }

    function fulfillRandUintArrayRequest(uint requestId, uint[] calldata nums) public isOwner(msg.sender) fulfillRequest(requestId){
        IRequester(requests[requestId]).fulfillRequestRandUintArray(requestId, nums);
    }

    // -----------------------------------


    function isAllowedAddress(address _from) virtual public view returns(bool) {
        return allowedAddresses[_from];
    }

    function updateAllowedAddress(address allowedAddr, bool isActive) isOwner(msg.sender) virtual public {
        allowedAddresses[allowedAddr] = isActive;
    }
    
}