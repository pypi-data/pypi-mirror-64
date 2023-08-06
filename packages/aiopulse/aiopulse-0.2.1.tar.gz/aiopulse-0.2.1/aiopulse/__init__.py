"""Rollease Acmeda Automate Pulse asyncio protocol implementation."""
import logging

from aiopulse.hub import Hub
from aiopulse.elements import Roller, Room, Scene
_LOGGER = logging.getLogger(__name__)
