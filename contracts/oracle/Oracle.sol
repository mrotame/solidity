// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {IRequester} from "./IRequester.sol";

import {OracleModifiers} from "./OracleModifiers.sol";

contract Oracle is OracleModifiers{
    constructor(address[] memory _allowedAddresses) {
        contractOwner = msg.sender;
        callerAccount = msg.sender;

        for (uint i = 0; i < _allowedAddresses.length; i++) {
            allowedAddresses[_allowedAddresses[i]] = true;
        }
    }

    function createRequest(RequestTypes requestType) internal returns (uint128){
        currentRequestId += 1; 
        requests[currentRequestId] = msg.sender;
        emit RequestCreated(currentRequestId, msg.sender, requestType, baseGasWeiFee);
        return currentRequestId;
    }

    // --------- RandUint Request ---------

    // Generate
    function generateSingleRandUint(uint24 minNum, uint24 maxNum) public payable isOwnerOrAllowed(msg.sender) requireFee returns (uint){
        uint128 request = createRequest(RequestTypes.RANDUINT_SINGLE);

        emit SingleRandUintParams(request, maxNum, minNum);

        return request;
    }

    function generateRandUintArray(uint24 minNum, uint24 maxNum, uint8 quantityRequired) public payable isOwnerOrAllowed(msg.sender) requireFee returns (uint){
        uint128 request = createRequest(RequestTypes.RANDUINT_ARRAY);

        emit RandUintArrayParams(request, maxNum, minNum,quantityRequired);

        return request;
    }

    // Fulfill
    function fulfillSingleRandUintRequest(uint128 requestId, uint24 num) public isOwner(msg.sender) fulfillRequest(requestId) {
        IRequester(requests[requestId]).fulfillRequestSingleRandUint(requestId, num);
    }

    function fulfillRandUintArrayRequest(uint128 requestId, uint24[] calldata nums) public isOwner(msg.sender) fulfillRequest(requestId){
        IRequester(requests[requestId]).fulfillRequestRandUintArray(requestId, nums);
    }

    // -----------------------------------


    function isAllowedAddress(address _from) virtual public view returns(bool) {
        return allowedAddresses[_from];
    }

    function updateAllowedAddress(address allowedAddr, bool isActive) isOwner(msg.sender) virtual public {
        allowedAddresses[allowedAddr] = isActive;
    }

    function setCallerAddress(address newCaller) public isOwner(msg.sender){
        callerAccount = newCaller;
    }

    function getbaseGasGweiFee() public view returns(uint256) {
        return baseGasWeiFee;
    }

    function setbaseGasGweiFee(uint256 Gwei) public {
        baseGasWeiFee = (Gwei * 1 gwei);
    }

    function transferGas() public isOwner(msg.sender) {
        (bool status, ) = callerAccount.call{value: address(this).balance}("");
        require(status, "Failed to transfer gas for callback");
    }
    
}