from dotenv import load_dotenv

load_dotenv()

import os

import wake.deployment as wd

from pytypes.contracts.game.ArcaneWood import ArcaneWood
from pytypes.contracts.game.characters import ArcaneCharacters
from pytypes.contracts.oracle.Oracle import Oracle
from pytypes.contracts.mock.VRFCaller import VRFCaller

NODE_URL = "https://bsc-testnet-dataseed.bnbchain.org"

ARCANEWOOD_CONTRACT = "0x6da117feab05963843f9e10972efab1d75bc17dc"

NFT_TEST_CONTRACT = "0xcecf36e0af95e9f11f01bd70c146b16cad62b53b"

ORACLE_CONTRACT = "0xb5498b31ca4c1b0cc781214a018f14a19fbeea9d"
VRFCALLER_CONTRACT = "0x8a5eefbced8b59b61f622f2871f1c9afcf16fd26"


@wd.default_chain.connect(NODE_URL)
def main():
    account = wd.Account.from_mnemonic(os.getenv("secret_phrase_wallet"))
    wd.default_chain.set_default_accounts(account)

    oracle: Oracle = Oracle.deploy([])
    caller = VRFCaller.deploy(oracle.address)

    oracle.updateAllowedAddress(caller.address, True)

    request = caller.generateSingleRandUint(10, 100)

    result = oracle.fulfillSingleRandUintRequest(1, 55)

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
