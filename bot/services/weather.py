import python_weather


class WeatherService:
    def __init__(self):
        self.client: python_weather.Client | None = None

    async def start(self):
        self.client = python_weather.Client(unit=python_weather.METRIC)

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None

    async def by_city(self, city: str) -> dict:
        if not self.client:
            await self.start()
        w = await self.client.get(city)
        return {
            "place": w.location,
            "temp": w.temperature,
            "feels": getattr(w, "feels_like", None),
            "wind": getattr(w, "wind_speed", None),
        }
