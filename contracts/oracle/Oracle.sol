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

    function getlastExecutionCost(address _from, RequestTypes _request_type) public view returns(uint) {
        return lastCostsPerRequester[_from][_request_type];
    }

    function getRequest(uint requestId) public view returns(RequestData memory) {
        require(requests[requestId].requestId != 0);
        
        return requests[requestId];
    }

    function createRequest(RequestTypes requestType) internal returns (RequestData memory) {
        currentRequestId += 1;

        RequestData memory requestData = RequestData(
            currentRequestId,
            requestType,
            msg.sender,
            block.timestamp,
            0,
            0,
            false
        );
        
        requests[currentRequestId] = requestData;
        
        emit RequestCreated(requestData.requestId, requestData.requester, requestType, requestData.requestTimestamp);

        return requestData;
    }

    // --------- RandUint Request ---------

    // Generate
    function generateSingleRandUint(uint minNum, uint maxNum) public payable requireslastExecutionCost(msg.sender, RequestTypes.RANDUINT_SINGLE) nonReentrant isOwnerOrAllowed(msg.sender){
        RequestData memory request = createRequest(RequestTypes.RANDUINT_SINGLE);

        emit RandUintParams(request.requestId, maxNum, minNum);
    }

    function generateRandUintArray(uint minNum, uint maxNum, uint quantityRequired) public payable requireslastExecutionCost(msg.sender, RequestTypes.RANDUINT_ARRAY) nonReentrant isOwnerOrAllowed(msg.sender){
        RequestData memory request = createRequest(RequestTypes.RANDUINT_ARRAY);

        emit RandUintParams(request.requestId, maxNum, minNum,quantityRequired);
    }

    // Fulfill
    function fulfillSingleRandUintRequest(uint requestId, uint num) public isOwner(msg.sender) fulfillRequest(requestId) nonReentrant{
        IRequester(requests[requestId].requester).fulfillRequestSingleRandUint(requestId, num);
    }

    function fulfillRandUintArrayRequest(uint requestId, uint[] calldata nums) public isOwner(msg.sender) fulfillRequest(requestId) nonReentrant{
        IRequester(requests[requestId].requester).fulfillRequestRandUintArray(requestId, nums);
    }

    // -----------------------------------


    function isAllowedAddress(address _from) virtual public view returns(bool) {
        return allowedAddresses[_from];
    }

    function updateAllowedAddress(address allowedAddr, bool isActive) isOwner(msg.sender) virtual public {
        allowedAddresses[allowedAddr] = isActive;
    }
    
}