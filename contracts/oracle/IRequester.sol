// SPDX-License-Identifier: MIT

pragma solidity 0.8.24;

interface IRequester {
    function fulfillRequestSingleRandUint(uint128 requestId, uint24 num) external;
    function fulfillRequestRandUintArray(uint128 requestId, uint24[] memory nums) external;
}