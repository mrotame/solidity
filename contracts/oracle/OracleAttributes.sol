// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;


contract OracleAttributes {
    enum RequestTypes { RANDUINT_SINGLE, RANDUINT_ARRAY }
    
    uint withdraw_number;
    uint deposit_number;


    struct RequestData {
        uint requestId;
        RequestTypes requestType;
        address requester;
        uint requestTimestamp;
        uint callbackCost;
        uint callbackTimestamp;
        bool fulfiled;
    }

    uint256 currentRequestId;

    mapping (uint requestId => RequestData) requests;

    mapping (RequestTypes => bytes4) fulfillFunctions;

    mapping (address requester => mapping(RequestTypes requestName => uint costGwei) functionCost) lastCostsPerRequester;
}