"""
ExchaigeAssistantBase
"""
from urllib.parse import urljoin


class ExchaigeAssistantBase:
    """ExchaigeAssistantBase"""

    def __init__(
        self,
        url: str,
        headers: dict,
        version: str = "v1"
    ):
        self._url = url
        self._headers = headers
        self._version = version

    def _get_resource_url(self, resource: str, path: str):
        """

        :param path:
        :return:
        """
        assert resource, "resource can't be None"
        assert path.startswith("/"), "A path prefix must start with '/'"
        return urljoin(base=self._url, url=f"/api/{self._version}/{resource}{path}")
