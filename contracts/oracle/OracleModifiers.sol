// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;


import {SecuredContract} from "../common/securedContract/SecuredContract.sol";
import {OracleEvents} from "./OracleEvents.sol";
import {OracleAttributes} from "./OracleAttributes.sol";
import {OracleUtils} from "./OracleUtils.sol";

contract OracleModifiers is SecuredContract, OracleEvents {
    
    modifier fulfillRequest(uint requestId) {
        _;
        emit RequestFulfilled(requestId);
    }

    modifier isOwnerOrAllowed(address _from) {
        require(
            allowedAddresses[_from] ||
            _from == contractOwner,
            "Is Owner or allowed error: Not Authorized");
        _;
    }
}