import asyncio
from unittest import mock, IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from aiohttp import ClientSession
from aiohttp.test_utils import make_mocked_coro

from fetcher import fetch_url, fetch_several_url, get_queue_urls


class TestFetcher(IsolatedAsyncioTestCase):

    async def test_get_queue_urls(self):
        mock_queue = mock.AsyncMock()
        mock_file = mock.mock_open(read_data="https://example.com")
        with mock.patch("builtins.open", mock_file):
            await get_queue_urls("urls.txt")

        mock_queue.put.assert_called_once_with("https://example.com")

    async def test_fetch_url(self):
        mock_response = MagicMock()
        mock_response.read = make_mocked_coro('<html><title>Page Title</title></html>')
        mock_session = mock.MagicMock(spec=ClientSession)
        mock_session.get.return_value.__aenter__.return_value = mock_response

        mock_queue = asyncio.Queue()
        await mock_queue.put('https://example.com')

        with mock.patch('aiohttp.ClientSession', return_value=mock_session):
            results = await fetch_url(mock_session, mock_queue)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0], 'Page Title')

    @mock.patch('fetcher.get_queue_urls')
    @mock.patch('fetcher.fetch_url')
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_fetch_several_url(self, mock_open, mock_fetch_url, mock_get_queue_urls):
        queue = asyncio.Queue()
        queue.put_nowait('http://example.com')
        queue.put_nowait('http://example.org')

        # Настройка мок-объекта get_queue_urls
        mock_get_queue_urls.return_value.return_value = queue  # Исправленная строка
        mock_fetch_url.return_value = ['Title 1', 'Title 2']

        mock_file_contents = 'test_file_contents'
        mock_open.return_value.__enter__.return_value.read.return_value = mock_file_contents

        result = asyncio.run(fetch_several_url('test_filename', 2))

        self.assertEqual(result, ['Title 1', 'Title 2'])
        mock_get_queue_urls.assert_called_once_with('test_filename')
        mock_fetch_url.assert_called()
        mock_open.assert_called_once_with('test_filename', 'r')

        mock_open.reset_mock()
        mock_fetch_url.reset_mock()
        mock_get_queue_urls.reset_mock()

        queue = asyncio.Queue()
        queue.put_nowait('http://example.com')

        mock_get_queue_urls.return_value.return_value = queue
        mock_fetch_url.return_value = ['Title 3']

        result = asyncio.run(fetch_several_url('another_filename', 1))

        self.assertEqual(result, ['Title 3'])
        mock_get_queue_urls.assert_called_once_with('another_filename')
        mock_fetch_url.assert_called()
        mock_open.assert_called_once_with('another_filename', 'r')