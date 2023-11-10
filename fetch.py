import aiohttp
import asyncio

maxPages = 6145

baseUrl = "https://locator.iocl.com/?circle_name=&city_name=New+Delhi&crs=&locality_name=Delhi&radius=10000&state_name=Delhi&page="

headers = {
    "host": "locator.iocl.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
}


async def fetch(session, i):
    url = baseUrl + str(i)
    async with session.get(url, headers=headers) as response:
        with open(f"responses/{i}.html", "w") as f:
            f.write(await response.text())


async def fetch_all(s: aiohttp.ClientSession, start, end):
    tasks = []
    for i in range(start, end):
        tasks.append(asyncio.create_task(fetch(s, i)))
    return await asyncio.gather(*tasks)


async def main():
    async with aiohttp.ClientSession() as session:
        i = 1
        increment = 50

        while i < maxPages:
            print(f"Fetching {i} to {min(i + increment, maxPages+1)}")
            await fetch_all(session, i, min(i + increment, maxPages + 1))
            i += increment


asyncio.run(main())
