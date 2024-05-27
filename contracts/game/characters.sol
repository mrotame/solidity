// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {ERC721} from "../common/tokens/ERC721.sol";
import {ERC721Utils} from "../common/utils/ERC721Utils.sol";

contract ArcaneCharacters is ERC721{
    uint requestId;
    enum characterTypes {MINER, LUMBERJACK, FISHERMAN, WARRIOR}
    
    struct Character {
        characterTypes characterType;
        string randomSeed;
        uint intelligence;
        uint strength;
        uint stamina;
        uint moral;
    }

    event MintRequest(
        uint indexed requestId,
        address requester,
        uint requestTimestamp
    );
    
    constructor(address[] memory _admins) ERC721("Arcane Characters", "ARCH", 0, _admins) {
        _mint(address(0xd9cb9167159adA5aCACd0fdb3E73A067008168fA));
    }

    function tokenURI(uint256 _tokenId) public view override returns (string memory) {
        bytes memory _dataURI = abi.encodePacked(
            "data:application/json;utf8,",
            '{',
                '"name":"Test Token NFT",',
                '"description":"Test description",',
                '"image":"" '
            '}'
        );

        return string(_dataURI);
    }

    function requestMint() public{
        requestId ++;
        emit MintRequest(requestId, msg.sender, block.timestamp);
    }

    function mintNft(uint requestId, address _to) public isOwner(msg.sender) {
        _mint(_to);
    }

}