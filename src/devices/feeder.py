from .base import DeviceStatus


class Feeder:
    async def get_status(self) -> DeviceStatus:
        return DeviceStatus(
            name="Distributeur de croquettes",
            available=False,
            summary="Pas connecté",
        )
