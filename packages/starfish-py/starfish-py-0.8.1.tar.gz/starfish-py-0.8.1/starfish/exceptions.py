"""

    Exceptions for starfish-py

"""


class StarfishPurchaseError(Exception):
    """ Raised when a purchase events have failed to complete """


class StarfishAssetNotFound(Exception):
    """ Raised when an asset is not found """


class StarfishAssetInvalid(Exception):
    """ Raised when a downloaded asset is not valid or has been changed """


class StarfishInsufficientFunds(Exception):
    """ Raised when the account has insufficient funds to send token or ether """
