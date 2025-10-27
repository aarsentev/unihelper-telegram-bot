import httpx


class RatesService:
    BASE_URL = "https://api.exchangerate-api.com/v4/latest"

    async def get_rates(self, base: str, symbols: list[str]) -> dict[str, float]:
        base = base.upper()
        symbols_upper = [s.upper() for s in symbols]
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{self.BASE_URL}/{base}")
        
        if r.status_code != 200:
            return {}
        
        data = r.json()
        all_rates = data.get("rates", {})

        return {sym: all_rates.get(sym) for sym in symbols_upper if sym in all_rates}
