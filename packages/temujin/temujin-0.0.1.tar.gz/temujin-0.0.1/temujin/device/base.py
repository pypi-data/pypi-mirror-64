from temujin.layout.page import Page


class _BaseActionPlayer(object):
    """
    apply some actions (related to widgets) on device.
    something like click, swipe, etc.
    """


class _BaseStatusManager(object):
    """
    device status
    """


class _BaseExtractor(object):
    """
    this class was built for extracting
    device related things (xml, pic, etc.)
    to Page object.
    """

    # TODO different types of input
    def extract(self) -> Page:
        raise NotImplementedError


class _BaseDevice(object):
    """
    3 parts:
        - action player
        - status manager
        - extractor
    """

    ACTION_PLAYER_KLS = _BaseActionPlayer
    STATUS_MANAGER_KLS = _BaseStatusManager
    EXTRACTOR_KLS = _BaseExtractor
