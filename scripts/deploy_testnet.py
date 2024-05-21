from dotenv import load_dotenv

load_dotenv()

import os

import wake.deployment as wd

from pytypes.contracts.ArcaneWood import ArcaneWood
from pytypes.contracts.characters import Characters

NODE_URL = "https://bsc-testnet-dataseed.bnbchain.org"

ARCANEWOOD_CONTRACT = "0x6da117feab05963843f9e10972efab1d75bc17dc"

NFT_TEST_CONTRACT = "0xcecf36e0af95e9f11f01bd70c146b16cad62b53b"


@wd.default_chain.connect(NODE_URL)
def main():
    wd.default_chain.set_default_accounts(
        wd.Account.from_mnemonic(os.getenv("secret_phrase_wallet"))
    )
    nft_token = Characters.deploy([])
    print(nft_token.address)

    if not ARCANEWOOD_CONTRACT:
        token = ArcaneWood.deploy()
    else:
        token = ArcaneWood(ARCANEWOOD_CONTRACT)

    # token.mint(
    #     "0xd9cb9167159ada5acacd0fdb3e73a067008168fa", 100 * (10 ** token.decimals())
    # )


if __name__ == "__main__":
    main()
