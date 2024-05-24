// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {IRequester} from "./IRequester.sol";

import {OracleModifiers} from "./OracleModifiers.sol";

contract Oracle is OracleModifiers{
    constructor() {
        contractOwner = msg.sender;
    }

    function getlastExecutionCost() public view returns(uint) {
        return lastExecutionCost;
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
    function generateRandUint(uint minNum, uint maxNum) public payable requireslastExecutionCost {
        RequestData memory request = createRequest(RequestTypes.RANDUINT);

        emit RandUintParams(request.requestId, maxNum, minNum);
    }

    function generateRandUint(uint minNum, uint maxNum, uint quantityRequired) public payable requireslastExecutionCost {
        RequestData memory request = createRequest(RequestTypes.RANDUINT);

        emit RandUintParams(request.requestId, maxNum, minNum,quantityRequired);
    }

    // Fulfill
    function fulfillRandUintRequest(uint requestId, uint num) public isOwner(msg.sender) fulfillRequest(requestId){
        IRequester(requests[requestId].requester).fulfillRequestRandUint(requestId, num);
    }

    function fulfillRandUintRequest(uint requestId, uint[] calldata nums) public isOwner(msg.sender) fulfillRequest(requestId) {
        IRequester(requests[requestId].requester).fulfillRequestRandUint(requestId, nums);
    }
    // -------------------------------------------
   
}