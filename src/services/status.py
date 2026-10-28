import asyncio
from src.devices.base import Device, DeviceStatus


async def get_all_statuses(
    devices: list[Device],
) -> list[DeviceStatus]:
    results = await asyncio.gather(
        *(device.get_status() for device in devices),
        return_exceptions=True,
    )

    statuses = []

    for device, result in zip(devices, results):
        if isinstance(result, BaseException):
            statuses.append(
                DeviceStatus(
                    name=type(device).__name__,
                    available=False,
                    summary="Unable to retrieve status",
                )
            )
        else:
            statuses.append(result)

    return statuses
