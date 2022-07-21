#!/usr/bin/python3
from brownie import SimpleCollectible, AdvancedCollectible, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_car, OPENSEA_FORMAT


car_metadata_dic = {
    "Breakout": "ipfs://QmYiwcTQvTjZZ6VK65m5cSCXCcYwdw4ZMFFhTsgyezHnd5",
    "Merc": "ipfs://QmXYRQ2G4rxqSCgPACRDRKTWUqpKJeGaFMGiL3yudZkMQb",
    "Octane": "ipfs://QmWTawvxNGpWBsUGfz16uFk8GpajZgeegUPkS7MUdErVe4",
}

def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    for token_id in range(number_of_advanced_collectibles):
        cartype = get_car(advanced_collectible.tokenIdToCar(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("ipfs://"):
            print("Setting the tokenURI of token {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible,
                         car_metadata_dic[cartype])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
