from temujin.device.base import (
    _BaseDevice,
    _BaseExtractor,
    _BaseActionPlayer,
    _BaseStatusManager,
)
from temujin.layout.page import Page


class AndroidActionPlayer(_BaseActionPlayer):
    pass


class AndroidStatusManager(_BaseStatusManager):
    pass


class AndroidExtractor(_BaseExtractor):
    def extract(self) -> Page:
        raise NotImplementedError


class AndroidDevice(_BaseDevice):
    ACTION_PLAYER_KLS = AndroidActionPlayer
    STATUS_MANAGER_KLS = AndroidStatusManager
    EXTRACTOR_KLS = AndroidExtractor
