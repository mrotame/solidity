# ETH Oracle

## Introduction
This project is an ETH Oracle app. This app is meant to observe the ETH blockchain, 
generate true randomness and inject into the blockchain.

## Installing
### Foundry & Anvil

Docs Foundry: https://book.getfoundry.sh/getting-started/installation
Docs Anvil: https://book.getfoundry.sh/anvil/

Foundry is an ETH blockchain toolbox with a lot of tools that help us
develop contracts. 

Anvil is a local ethereum dev blockchain. We use anvil to emulate
the ETH blockchain in the dev environment.

1. Config Foundry install script by running `curl -L https://foundry.paradigm.xyz | bash`
2. Update the terminal by running `source /home/otame/.zshenv` or start a new terminal session
3. Install Foundry by running `foundryup`

### Add openzeppelin to Foundry

Docs Openzeppelin: https://docs.openzeppelin.com/upgrades-plugins/foundry-upgrades

Openzeppelin is a Solidity library we use in many of our solidity contracts. It contains
a lot of utilities to make faster and safer to develop contracts

1. Make sure there are no uncommited changes or untracked files in root dir
2. run the following commands in the terminal:
```Bash
forge install foundry-rs/forge-std
forge install OpenZeppelin/openzeppelin-foundry-upgrades
forge install OpenZeppelin/openzeppelin-contracts-upgradeable
```

### Poetry
use poetry `poetry install --with dev` to install all the dependencies

### dotenv
This project uses the python library `dotenv` to read secret variables.

1. Create a `.env` file in the project root
2. Add a variable named `random_org_api_key` with the random.org key as value

### Wake
Run the command `poetry run wake up` to create the pytypes for the solidity contracts