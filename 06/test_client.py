import queue
import unittest
from unittest import mock
from unittest.mock import mock_open

from client import Client
from server import Server


class TestClient(unittest.TestCase):
    def test_init_client(self):
        file_content = "https://123\nhttps://456\n"
        queue_url = queue.Queue()
        queue_url.put("https://123")
        queue_url.put("https://456")
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            client = Client('test.txt', 5, 'localhost', 5000)
            self.assertEqual([client.host, client.port], ['localhost', 5000])
            self.assertEqual([client.url_queue.get(), client.url_queue.get()], [queue_url.get(), queue_url.get()])

    def test_init_server(self):
        server = Server(3, 5, 'localhost', 5000)
        self.assertEqual([server.host, server.port], ['localhost', 5000])
        self.assertTrue(server.url_queue.empty())
        self.assertEqual(server.thread_master.name, 'Master')
        self.assertEqual(server.num_top_words, 5)
        self.assertEqual(server.url_completed, 0)
        self.assertEqual(server.threads_workers[0].name, 'Worker_0')
