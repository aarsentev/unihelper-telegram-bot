import httpx


class RatesService:
    BASE_URL = "https://api.exchangerate.host/latest"

    async def get_rates(self, base: str, symbols: list[str]) -> dict[str, float]:
        base = base.upper()
        syms = ",".join(s.upper() for s in symbols)
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(self.BASE_URL, params={"base": base, "symbols": syms})
        data = r.json()
        return data.get("rates", {}) or {}
