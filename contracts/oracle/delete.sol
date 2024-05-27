// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {IRequester} from "./IRequester.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

import {OracleModifiers} from "./OracleModifiers.sol";

contract Oracle {
    enum RequestTypes { RANDUINT_SINGLE, RANDUINT_ARRAY }

    struct RequestData {
        uint requestId;
        RequestTypes requestType;
        address requester;
        uint requestTimestamp;
        uint callbackCost;
        uint callbackTimestamp;
        bool fulfiled;
    }

    address callerAccount;
    address contractOwner;
    uint transferNumber;
    uint refoundNumber;

    constructor() {
        contractOwner = msg.sender;
        callerAccount = msg.sender;
    }

    event RequestCreated(
        uint indexed requestId,
        address requester,
        RequestTypes RequestTypes,
        uint requestTimestamp
    );

    event RandUintParams(
        uint indexed requestId,
        uint max_num,
        uint min_num
    );

    event RandUintParams(
        uint indexed requestId,
        uint max_num,
        uint min_num,
        uint quantityRequired
    );

    event Transfered(
        uint indexed transferNumber,
        address indexed receiver,
        uint amount // WEI
    );

    event Refunded(
        uint indexed refoundNumber,
        address indexed receiver,
        uint amount // WEI
    );


    mapping (address requester => mapping(RequestTypes requestName => uint costGwei) functionCost) lastCostsPerRequester;

    bool reentrancyLock;
    modifier nonReentrant() virtual {
        require(!reentrancyLock, "nonReentrant Error: reentrant call");
        reentrancyLock = true;
        _;
        reentrancyLock = false;
    }

    mapping(address  => bool) allowedAddresses;
    modifier isOwnerOrAllowed(address _from) {
        require(
            allowedAddresses[_from] ||
            _from == contractOwner,
            "Is Owner or allowed error: Not Authorized");
        _;
    }

    modifier requireslastExecutionCost(address requester, RequestTypes requestType) {
        uint lastExecutionCost = lastCostsPerRequester[requester][requestType];
        uint valueRequired = lastExecutionCost * (1 gwei);
        require(msg.value >= valueRequired, string(abi.encodePacked("insuficient payment amount. Expected:", Strings.toString(valueRequired))));

        if (msg.value > valueRequired) {
            uint toRefound = msg.value - valueRequired;
            transferEther(msg.sender, toRefound);
            transferNumber +=1;
            emit Refunded(transferNumber, msg.sender, toRefound);
        }

        _;

        if (valueRequired > 0) {
            transferEther(callerAccount, valueRequired);
            transferNumber += 1;
            emit Transfered(transferNumber, msg.sender, valueRequired);
        }
    }

    uint256 currentRequestId;
    mapping (uint requestId => RequestData) requests;

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

    function generateSingleRandUint(uint minNum, uint maxNum) public payable nonReentrant requireslastExecutionCost(msg.sender, RequestTypes.RANDUINT_SINGLE) isOwnerOrAllowed(msg.sender){
        RequestData memory request = createRequest(RequestTypes.RANDUINT_SINGLE);

        emit RandUintParams(request.requestId, maxNum, minNum);
    }

    function transferEther( address _to, uint _weiAmount) internal{
        (bool success, ) = payable(_to).call{value: _weiAmount}("");
        require(success, "TransferEther Error: failed to call receiver");
    }

}