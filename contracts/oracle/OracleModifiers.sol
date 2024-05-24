// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {SecuredContract} from "../common/securedContract/SecuredContract.sol";
import {OracleEvents} from "./OracleEvents.sol";
import {OracleAttributes} from "./OracleAttributes.sol";

contract OracleModifiers is SecuredContract, OracleEvents {
    modifier requireslastExecutionCost() {
        require(msg.value >= lastExecutionCost, "insuficient payment amount");
        _;
    }

    modifier fulfillRequest(uint requestId) {
        uint start_gas = gasleft();
        _;
        uint end_gas = start_gas - gasleft();

        emit RequestFulfilled(requestId, end_gas, block.timestamp);

        requests[requestId].callbackTimestamp = block.timestamp;
        requests[requestId].fulfiled = true;
        requests[requestId].callbackCost = end_gas;

        lastExecutionCost = end_gas;
    }
}