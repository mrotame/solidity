// SPDX-License-Identifier: MIT

pragma solidity 0.8.24;

interface IRequester {
    function fulfillRequestSingleRandUint(uint requestId, uint num) external;
    function fulfillRequestRandUintArray(uint requestId, uint[] memory nums) external;
}