// SPDX-License-Identifier: MIT

pragma solidity 0.8.24;

interface IRequester {
    function fulfillRequestSingleRandUint(uint256 requestId, uint24 num) external;

    function fulfillRequestRandUintArray(uint256 requestId, uint24[] memory nums) external;

    function fulfillCharacterMintRequest(uint256 characterId, uint8[10] memory attributes, string memory ipfsId) external;
}