// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {ERC721} from "../common/tokens/ERC721.sol";
import {ERC721Utils} from "../common/utils/ERC721Utils.sol";

import {Oracle} from "../oracle/Oracle.sol";

contract ArcaneCharacters is ERC721{
    Oracle oracle;

    mapping (uint tokenId => Character nft) nftMetadata;
 
    struct Character {
        string metadata_url;
        uint8 mining_power;
        uint8 mining_speed;
        uint8 chopping_power;
        uint8 chopping_speed;
        uint8 fishing_power;
        uint8 fishing_speed;
        uint8 fighting_power;
        uint8 fighting_speed;
        uint8 selling_power;
        uint8 selling_speed;
    }

    constructor(address _oracleContract, address[] memory _admins) ERC721("Arcane Characters", "ARCH", 0, _admins) {
        oracle = Oracle(_oracleContract);
    }

    function tokenURI(uint256 _tokenId) public view override returns (string memory) {
        return string(nftMetadata[_tokenId].metadata_url);
    }

    function requestMint() public{
        currentTokenId ++;
        tokens[currentTokenId] = msg.sender;

        oracle.generateCharacter(currentTokenId);
    }

    function fulfillCharacterMintRequest(uint256 characterId, uint8[10] memory attributes, string memory ipfsId) public isOracle(msg.sender){
        nftMetadata[characterId] = Character(
            ipfsId,
             attributes[0],
             attributes[1],
             attributes[2], 
             attributes[3],
             attributes[4],
             attributes[5],
             attributes[6],
             attributes[7],
             attributes[8],
             attributes[9]
        );
    }
    

}