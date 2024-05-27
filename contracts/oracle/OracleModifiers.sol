// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

import {SecuredContract} from "../common/securedContract/SecuredContract.sol";
import {OracleEvents} from "./OracleEvents.sol";
import {OracleAttributes} from "./OracleAttributes.sol";
import {OracleUtils} from "./OracleUtils.sol";

contract OracleModifiers is SecuredContract, OracleEvents {
    modifier requireslastExecutionCost(address requester, RequestTypes requestType) {
        uint lastExecutionCost = lastCostsPerRequester[requester][requestType];
        uint valueRequired = lastExecutionCost * (1 gwei);
        require(msg.value >= valueRequired, string(abi.encodePacked("insuficient payment amount. Expected:", Strings.toString(valueRequired))));

        if (msg.value > valueRequired) {
            uint toRefound = msg.value - valueRequired;
            OracleUtils.transferEther(msg.sender, toRefound);
            transferNumber +=1;
            emit Refunded(transferNumber, msg.sender, toRefound);
        }

        _;

        if (valueRequired > 0) {
            OracleUtils.transferEther(callerAccount, valueRequired);
            transferNumber += 1;
            emit Transfered(transferNumber, msg.sender, valueRequired);
        }
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

    modifier isOwnerOrAllowed(address _from) {
        require(
            allowedAddresses[_from] ||
            _from == contractOwner,
            "Is Owner or allowed error: Not Authorized");
        _;
    }
}