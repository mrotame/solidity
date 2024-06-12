// SPDX-License-Identifier: MIT

pragma solidity ^0.8.24;

import {ERC721} from "../common/tokens/ERC721.sol";
import {ERC721Utils} from "../common/utils/ERC721Utils.sol";

import {Oracle} from "../oracle/Oracle.sol";
import {ArcaneGold} from "./ArcaneGold.sol";

contract ArcaneCharacters is ERC721{
    Oracle oracle;
    ArcaneGold arcaneGold;
    uint public goldRequiredToMint  = 100;

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

    constructor(address _oracleContract, address _arcaneGoldContract, address[] memory _admins) ERC721("Arcane Characters", "ARCH", 0, _admins) {
        arcaneGold = ArcaneGold(_arcaneGoldContract);
        oracle = Oracle(_oracleContract);
    }

    function tokenURI(uint256 _tokenId) public view override returns (string memory) {
        return string(nftMetadata[_tokenId].metadata_url);
    }

    function requestMint() public payable{
        require(arcaneGold.balanceOf(msg.sender) >= goldRequiredToMint, "Arcane Gold validation error: Not enough balance");

        currentTokenId ++;
        arcaneGold.burn(msg.sender, goldRequiredToMint);
        tokens[currentTokenId] = msg.sender;

        oracle.generateCharacter{value:msg.value}(currentTokenId);
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
    
    function updateOracleAddress(address oracleAddress) public isOwner(msg.sender) {
        oracle = Oracle(oracleAddress);
    }

    function getOracleAddress() public view isOwner(msg.sender) returns(address _oracleAddress) {
        return address(oracle);
    }

    function updateArcaneGoldAddress(address _arcaneGoldAddress) public isOwner(msg.sender) {
        arcaneGold = ArcaneGold(_arcaneGoldAddress);
    }

    function getArcaneGoldAddress() public view isOwner(msg.sender) returns(address _arcaneGoldAddress) {
        return address(arcaneGold);
    }

    function updateGoldRequiredToMint(uint _newAmount) public isOwner(msg.sender) {
        goldRequiredToMint = _newAmount;
    }


}