// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

import {SecuredContract} from "../common/securedContract/SecuredContract.sol";
import {OracleEvents} from "./OracleEvents.sol";
import {OracleAttributes} from "./OracleAttributes.sol";

contract OracleModifiers is SecuredContract, OracleEvents {
    modifier requireslastExecutionCost(address requester, RequestTypes requestType) {
        lastExecutionCost = lastCostsPerRequester[requester][requestType];
        uint value_required = lastExecutionCost * (1 gwei);
        require(msg.value >= value_required, string(abi.encodePacked("insuficient payment amount. Expected:", value_required)));
        _;
    }

    modifier fulfillRequest(uint requestId) {
        uint start_gas = gasleft();

        address requester = requests[requestId].requester;
        RequestTypes requestType = requests[requestId].requestType;

        requests[requestId].callbackTimestamp = block.timestamp;
        requests[requestId].fulfiled = true;
        _;
        
        uint end_gas = (start_gas - gasleft()) *2;
        emit RequestFulfilled(requestId, end_gas, block.timestamp);
        requests[requestId].callbackCost = end_gas;
        lastCostsPerRequester[requester][requestType] = end_gas;
    }
}