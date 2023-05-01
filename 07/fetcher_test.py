import asyncio
import time
from unittest import mock, IsolatedAsyncioTestCase
from unittest.mock import mock_open
from urllib import request

from fetcher import get_urls, fetch_url, fetch_several_url


class TestFetcher(IsolatedAsyncioTestCase):
    def test_get_urls(self):
        with self.assertRaises(FileNotFoundError) as err:
            urls = get_urls('qwerty.txt')
            next(urls)
        self.assertEqual(str(err.exception), 'qwerty.txt not found')
        file_content = 'https://en.wikipedia.org/wiki/United_States'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            result = list(get_urls('test.txt'))
            self.assertEqual(result, [file_content])

    async def test_fetch_url(self):
        file_content = 'https://ed_Stas'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            result = next(get_urls('test.txt'))
        with self.assertRaises(Exception) as err:
            await fetch_url(result, asyncio.Semaphore(1))
        self.assertEqual(str(err.exception), f'Error fetching {file_content}')
        file_content = 'https://en.wikipedia.org/wiki/United_States'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            result = next(get_urls('test.txt'))
        data = await fetch_url(result, asyncio.Semaphore(1))
        self.assertEqual(data, request.urlopen(file_content).read())

    async def test_several_url(self):
        urls = get_urls('urls.txt')
        time1 = time.time()
        await fetch_several_url(urls, 10)
        result1 = time.time() - time1
        time2 = time.time()
        await fetch_several_url(urls, 100)
        result2 = time.time() - time2
        self.assertTrue(result2 < result1)
