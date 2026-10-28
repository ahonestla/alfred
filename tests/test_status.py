import pytest
from src.devices.base import DeviceStatus
from src.services.status import get_all_statuses


class WorkingDevice:
    async def get_status(self) -> DeviceStatus:
        return DeviceStatus(
            name="Feeder",
            available=True,
            summary="Online",
        )


class FailingDevice:
    async def get_status(self) -> DeviceStatus:
        raise RuntimeError("Device unavailable")


@pytest.mark.asyncio
async def test_status_survives_device_failure():
    statuses = await get_all_statuses([WorkingDevice(), FailingDevice()])

    assert len(statuses) == 2
    assert statuses[0].available is True
    assert statuses[1].available is False
    assert statuses[1].summary == "Unable to retrieve status"
