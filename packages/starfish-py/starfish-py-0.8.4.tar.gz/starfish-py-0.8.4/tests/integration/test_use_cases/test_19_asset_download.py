"""
    test_19_asset_download

    As a developer working with an Ocean marketplace,
    I want to record a purchase.

"""

import secrets
import logging
import json

from starfish.asset import DataAsset


def test_19_asset_download(resources, remote_agent):
    test_data = secrets.token_hex(1024)
    asset_data = DataAsset.create('TestAsset', test_data)


    asset = remote_agent.register_asset(asset_data)

    remote_agent.upload_asset(asset)

    # now download
    store_asset = remote_agent.download_asset(asset.asset_id)

    assert(store_asset)
    assert(store_asset.data == asset.data)
    assert(store_asset.asset_id == asset.asset_id)
