from __future__ import annotations

from .basecovid19 import BaseCovid19
from .covid19scope import Covid19

import requests


class ThaiCovid19(BaseCovid19):
    """ThaiCovid19 requests data from specific source"""

    def __init__(self: BaseCovid19, source: str = 'covid19.th-stat.com') -> None:
        """
        Args:
            source (str):
        """
        super().__init__(Covid19.THAI, source)

    def get(self: ThaiCovid19, field: str, **kwargs) -> dict:
        """
        Args:
            field (str):
            **kwargs:
        """
        url = self.api.get(field, None) if not field.startswith('http') else field
        result = None
        if url is not None:
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                result = response.json()
        return result

    def get_all(self: ThaiCovid19, lim: int = 10) -> dict:
        """
        Args:
            lim (int):
        """
        result = {}
        data = self.api.items()
        for counter, (field, url) in enumerate(data):
            if counter > lim:
                break
            result[field] = self.get(url)
        return result
