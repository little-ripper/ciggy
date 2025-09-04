from ciggy.db import async_session_context


async def fetch_status(url):
    async with async_session_context() as session:
        try:
            async with session.get(url) as resp:
                return url, resp.status
        except Exception:
            return url, -1
