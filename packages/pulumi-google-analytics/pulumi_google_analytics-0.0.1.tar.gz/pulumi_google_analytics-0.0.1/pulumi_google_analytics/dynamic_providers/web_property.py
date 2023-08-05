from pulumi.dynamic import Resource
from pulumi import Input, Output
from .web_property_provider import WebPropertyProvider
from ..service import get_key_file_location


class WebPropertyArgs(object):
    """
    Describes a GA web property.
    """

    account_id: Input[str]
    """
    Account ID of Google Analytics
    """

    site_name: Input[str]
    """
    Name of the website for this web property.
    """

    site_url: Input[str]
    """
    Website url for this web property.
    """

    def __init__(
        self, account_id, site_name, site_url,
    ):
        self.account_id = account_id
        self.site_name = site_name
        self.site_url = site_url


class WebProperty(Resource):
    tracking_id: Output[str]

    def __init__(self, name, args: WebPropertyArgs, opts=None):
        full_args = {
            "tracking_id": None,
            "key_location": get_key_file_location(),
            **vars(args),
        }
        super().__init__(WebPropertyProvider(), name, full_args, opts)
