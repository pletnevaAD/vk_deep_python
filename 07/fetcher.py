import argparse
import asyncio
import sys

import aiohttp


def get_urls(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'{filename} not found') from exc


async def fetch_url(url, sem):
    async with aiohttp.ClientSession() as session:
        async with sem:
            try:
                async with session.get(url) as resp:
                    return await resp.read()
            except Exception as exc:
                raise Exception(f"Error fetching {url}") from exc


async def fetch_several_url(urls, max_req):
    semaphore = asyncio.Semaphore(max_req)
    tasks = [asyncio.create_task(fetch_url(url, semaphore)) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', default=0, type=int)
    parser.add_argument('-f', default=0, type=str)
    input_args = parser.parse_args(sys.argv[1:])
    URLS = get_urls(input_args.f)
    asyncio.run(fetch_several_url(URLS, input_args.c))
