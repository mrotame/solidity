from dotenv import load_dotenv

load_dotenv()

import os

import wake.deployment as wd

from pytypes.contracts.game.ArcaneWood import ArcaneWood
from pytypes.contracts.game.characters import ArcaneCharacters
from pytypes.contracts.game.characterscopy import TestNFT
from pytypes.contracts.oracle.Oracle import Oracle
from pytypes.contracts.mock.VRFCaller import VRFCaller

NODE_URL = "https://bsc-testnet-dataseed.bnbchain.org"

ARCANEWOOD_CONTRACT = "0x6da117feab05963843f9e10972efab1d75bc17dc"

NFT_TEST_CONTRACT = "0xcecf36e0af95e9f11f01bd70c146b16cad62b53b"

ORACLE_CONTRACT = "0x59fd817df9e6a21e0c94622e58e78348ae4ee2f0"
VRFCALLER_CONTRACT = "0x03fa8911bc7e4a3ce4a543e1a123f2455d4affe5"


@wd.default_chain.connect(NODE_URL)
def main():
    account = wd.Account.from_mnemonic(os.getenv("secret_phrase_wallet"))
    wd.default_chain.set_default_accounts(account)

    # token = TestNFT("0x9839340de702722b3cce483f721fa8a615736f78")

    # print(token.tokenURI(1))

    oracle: Oracle = Oracle(ORACLE_CONTRACT)
    caller = VRFCaller(VRFCALLER_CONTRACT)

    # oracle.updateAllowedAddress(caller.address, True)

    request = caller.generateSingleRandUint(10, 100, value=100000000000000)
    request = caller.generateSingleRandUint(45, 700, value=100000000000000)

    print("oracle:", oracle.address)
    print("caller:", caller.address)
    pass


def make_deploy():
    account = wd.Account.from_mnemonic(os.getenv("secret_phrase_wallet"))
    wd.default_chain.set_default_accounts(account)

    oracle: Oracle = Oracle.deploy([])
    caller = VRFCaller.deploy(oracle.address)

    oracle.updateAllowedAddress(caller.address, True)


if __name__ == "__main__":
    main()
