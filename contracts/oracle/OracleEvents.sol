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

}