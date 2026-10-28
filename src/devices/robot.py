from .base import DeviceStatus


class Robot:
    async def get_status(self) -> DeviceStatus:
        return DeviceStatus(
            name="Robot aspirateur",
            available=False,
            summary="Pas connecté",
        )
