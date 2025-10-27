import python_weather


class WeatherService:
    def __init__(self):
        self.client: python_weather.Client | None = None

    async def start(self):
        self.client = python_weather.Client(
            unit=python_weather.METRIC,
            locale=python_weather.Locale.RUSSIAN
        )

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None

    async def by_city(self, city: str) -> dict:
        if not self.client:
            await self.start()
        w = await self.client.get(city)

        kind = getattr(w, "kind", None)
        kind_str = str(kind) if kind else None

        # km/h to m/s
        wind_speed_kmh = getattr(w, "wind_speed", None)
        wind_speed_ms = round(wind_speed_kmh / 3.6, 1) if wind_speed_kmh is not None else None
        
        return {
            "location": w.location,
            "country": getattr(w, "country", None),
            "region": getattr(w, "region", None),
            "temperature": w.temperature,
            "feels_like": getattr(w, "feels_like", None),
            "description": getattr(w, "description", None),
            "kind": kind_str,
            "humidity": getattr(w, "humidity", None),
            "wind_speed": wind_speed_ms,
            "visibility": getattr(w, "visibility", None),
            "pressure": getattr(w, "pressure", None),
            "precipitation": getattr(w, "precipitation", None),
        }
