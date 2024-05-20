from dotenv import load_dotenv

load_dotenv()

import os

import wake.deployment as wd

from pytypes.contracts.ArcaneWood import ArcaneWood

NODE_URL = "https://bsc-testnet-dataseed.bnbchain.org"

ArcaneWoodContract = "0x6da117feab05963843f9e10972efab1d75bc17dc"


@wd.default_chain.connect(NODE_URL)
def main():
    wd.default_chain.set_default_accounts(
        wd.Account.from_mnemonic(os.getenv("secret_phrase_wallet"))
    )

    if not ArcaneWoodContract:
        token = ArcaneWood.deploy()
    else:
        token = ArcaneWood(ArcaneWoodContract)

    # token.mint(
    #     "0xd9cb9167159ada5acacd0fdb3e73a067008168fa", 100 * (10 ** token.decimals())
    # )


if __name__ == "__main__":
    main()
