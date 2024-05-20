// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.25;

import {IERC721Receiver} from "../IERCS/IERC721.sol";

library ERC721Utils {
    function CallOnReceived(
        address _operator,
        address _from,
        address _to,
        uint256 _tokenId,
        bytes memory _data
    ) internal {
        if (_to.code.length <= 0) {
            return;
        }
        
        try IERC721Receiver(_to).onERC721Received(_operator, _from, _tokenId, _data) returns(bytes4 retval){
            require (retval == IERC721Receiver.onERC721Received.selector, "Call on received error: Token rejected");
        } catch (bytes memory reason) {
            require(reason.length > 0, "Call on received error: operator does not have IERC721Receiver implemented");

            assembly {
                revert(add(32, reason), mload(reason))
            }
        }
    }
}