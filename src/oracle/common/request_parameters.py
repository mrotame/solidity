from __future__ import annotations

from enum import Enum


class RequestType(Enum):
    SingleRandUintParams = 0
    RandUintArrayParams = 1
