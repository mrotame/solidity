// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {OracleAttributes} from "./OracleAttributes.sol";

contract OracleEvents is OracleAttributes{
    event RequestCreated(
        uint indexed requestId,
        address requester,
        RequestTypes RequestTypes
    );

    event RequestFulfilled(
        uint indexed requestId
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

}