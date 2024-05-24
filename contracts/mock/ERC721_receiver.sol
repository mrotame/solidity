// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {IERC721} from "../common/IERCS/IERC721.sol";

contract ERC721Receiver {
    bool public token_received;
    bool public is_valid_transaction;
    address public sender;
    address public operator;
    address public received_from;
    uint public token_id;
    bytes public data;

    function onERC721Received(
        address _operator,
        address _from,
        uint _tokenId,
        bytes memory _data
    ) public returns(bytes4) {
        token_received = true;
        sender = msg.sender;
        operator = _operator;
        received_from = _from;
        token_id = _tokenId;
        data = _data;

        is_valid_transaction = IERC721(msg.sender).ownerOf(token_id) == address(this);
        return this.onERC721Received.selector;
    }
}