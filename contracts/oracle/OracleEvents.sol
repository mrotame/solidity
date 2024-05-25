// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {OracleAttributes} from "./OracleAttributes.sol";

contract OracleEvents is OracleAttributes{
    event RequestCreated(
        uint indexed requestId,
        address requester,
        RequestTypes RequestTypes,
        uint requestTimestamp
    );

    event RequestFulfilled(
        uint indexed requestId,
        uint callbackCost,
        uint callbackTimestamp
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

    event Deposited(
        uint indexed deposit_number,
        address indexed depositor,
        uint amount // WEI
    );

    event Withdrawn(
        uint indexed withdraw_number,
        address indexed withdrawer,
        uint amount // WEI
    );
}