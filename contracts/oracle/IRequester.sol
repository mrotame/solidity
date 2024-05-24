// SPDX-License-Identifier: MIT

pragma solidity 0.8.24;

interface IRequester {
    function fulfillRequestRandUint(uint requestId, uint num) external;
    function fulfillRequestRandUint(uint requestId, uint[] memory nums) external;
}