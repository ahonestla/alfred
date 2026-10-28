from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class DeviceStatus:
    name: str
    available: bool
    summary: str


class Device(Protocol):
    async def get_status(self) -> DeviceStatus: ...
