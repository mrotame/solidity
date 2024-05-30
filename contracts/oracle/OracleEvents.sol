// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.24;

import {OracleAttributes} from "./OracleAttributes.sol";

contract OracleEvents is OracleAttributes{
    event RequestCreated(
        uint128 indexed requestId,
        address requester,
        RequestTypes requestType,
        uint256 chargedGas
    );

    event RequestFulfilled(
        uint128 indexed requestId
    );

    event SingleRandUintParams(
        uint128 indexed requestId,
        uint24 max_num,
        uint24 min_num
    );

    event RandUintArrayParams(
        uint128 indexed requestId,
        uint24 max_num,
        uint24 min_num,
        uint8 quantityRequired
    );

}