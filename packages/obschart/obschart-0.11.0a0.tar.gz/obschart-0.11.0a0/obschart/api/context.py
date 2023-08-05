# sfrom .obschart_api_client import ObschartApiClient


class Context(object):
    # client: ObschartApiClient
    data: dict

    def __init__(self, client, data={}):
        super().__init__()

        from .obschart_api_client import ObschartApiClient

        self.client: ObschartApiClient = client
        self.data = data
