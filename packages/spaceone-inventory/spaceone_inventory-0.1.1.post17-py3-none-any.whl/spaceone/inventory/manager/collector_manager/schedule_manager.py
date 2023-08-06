import logging

from spaceone.core.manager import BaseManager

_LOGGER = logging.getLogger(__name__)

"""
Schedule
"""
class ScheduleManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


