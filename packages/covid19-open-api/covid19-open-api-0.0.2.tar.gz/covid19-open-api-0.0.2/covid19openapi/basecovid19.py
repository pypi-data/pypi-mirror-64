from __future__ import annotations
from abc import ABC

from .config import Config
from .covid19scope import Covid19


class BaseCovid19(ABC):
    """Base class for Covid19 classes"""

    __sources__ = Config.SOURCE.value
    __slots__ = ('__scope', '__source', '__data')

    def __init__(self: object, scope: Covid19, source: str) -> None:
        """
        Args:
            scope (Covid19):
            source (str):
        """
        self.__scope = scope
        self.__source = source
        self.__api = BaseCovid19.__sources__[scope].get(source, None)

    @property
    def source(self: BaseCovid19) -> str:
        return self.__source

    @property
    def api(self: BaseCovid19) -> dict:
        return self.__api
