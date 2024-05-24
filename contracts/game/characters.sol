// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {ERC721} from "../common/tokens/ERC721.sol";
import {ERC721Utils} from "../common/utils/ERC721Utils.sol";

contract ArcaneCharacters is ERC721{
    string uri_data = 'ipfs://bafybeibp6tvdumr4vyjn7yaglcqkyat4a7tkt7szu42e5jsimk2hf3nbc4';
    
    constructor(address[] memory _admins) ERC721("Arcane Characters", "ARCH", 0, _admins) {
        _mint(address(0xd9cb9167159adA5aCACd0fdb3E73A067008168fA));
    }

    function tokenURI(uint256 _tokenId) public view override returns (string memory) {
        bytes memory _dataURI = abi.encodePacked(
            "data:application/json;utf8,",
            '{',
                '"name":"Test Token NFT",',
                '"description":"Test description",',
                '"image":"http://pm1.narvii.com/6908/59db53adee65fc677e2e221b461e2c7484c1902dr1-365-358v2_00.jpg"'
            '}'
        );

        return string(_dataURI);
    }

    function test(uint abacaxi) public pure returns(bool) {
        return true;
    }

    function setContractURI(string memory _uri_data) public {
        uri_data = _uri_data;
    }
}