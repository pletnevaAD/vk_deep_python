import argparse
import asyncio
import sys

import aiohttp
from bs4 import BeautifulSoup


async def fetch_url(session, queue):
    results = []
    while not queue.empty():
        url = await queue.get()
        try:
            async with session.get(url) as resp:
                content = await resp.read()
                soup = BeautifulSoup(content, features='html.parser')
                title = soup.find('title').string
                results.append(title)
        except Exception as exc:
            raise Exception(f"Error fetching {url}") from exc
        finally:
            queue.task_done()
    return results


async def fetch_several_url(filename, max_req):
    que = await get_queue_urls(filename)

    async with aiohttp.ClientSession() as session:
        tasks = []
        titles = []
        while not que.empty():
            tasks.append(fetch_url(session, que))

            if len(tasks) >= max_req:
                results = await asyncio.gather(*tasks)
                for result in results:
                    for res in result:
                        titles.append(res)
                tasks = []
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                for res in result:
                    titles.append(res)
        return titles


async def get_queue_urls(filename):
    queue = asyncio.Queue()
    try:
        with open(filename, "r") as file:
            for line in file:
                url = line.strip()
                await queue.put(url)
            return queue
    except FileNotFoundError as exc:
        raise FileNotFoundError(f'{filename} not found') from exc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', default=0, type=int)
    parser.add_argument('-f', default=0, type=str)
    input_args = parser.parse_args(sys.argv[1:])
    asyncio.run(fetch_several_url(input_args.f, input_args.c))
