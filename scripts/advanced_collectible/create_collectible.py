#!/usr/bin/python3
from brownie import AdvancedCollectible, accounts, config
from scripts.advanced_collectible import set_tokenuri
from scripts.helpful_scripts import get_car, fund_with_link, listen_for_event
import time


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    fund_with_link(advanced_collectible.address)
    transaction = advanced_collectible.createCollectible("None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    # time.sleep(35)
    # Waiting for the randomness to be fulfilled
    listen_for_event(
        advanced_collectible, "ReturnedCollectible", timeout=200, poll_interval=10
    )
    requestId = transaction.events["RequestedCollectible"]["requestId"]
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    cartype = get_car(advanced_collectible.tokenIdToCar(token_id))
    print("Car type of tokenId {} is {}".format(token_id, cartype))
    # Automatic tokenURI setting
    set_tokenuri.main()

    