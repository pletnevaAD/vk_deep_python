import argparse
import queue
import sys
import threading
import socket


class Client:
    def __init__(self, file, M, host, port):
        self.url_queue = self._get_urls(file)
        self.threads = [threading.Thread(target=self.send_url, name=f"client_thread_{i}") for i in range(M)]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def start_client(self):
        self.server.connect((self.host, self.port))
        for thread in self.threads:
            thread.start()

    def _get_urls(self, file):
        url_queue = queue.Queue()
        with open(file, 'r') as f:
            urls = f.readlines()
            for url in urls:
                url_queue.put(url.strip())
        return url_queue

    def send_url(self):
        while True:
            try:
                url = self.url_queue.get()
            except Exception:
                continue
            self.server.sendall(url.encode('utf-8'))
            data = self.server.recv(1024)
            result = data.decode('utf-8')
            print(result)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', default=0, type=int)
    parser.add_argument('-f', default=0, type=str)
    client_input = parser.parse_args(sys.argv[1:])
    client = Client(client_input.f, client_input.m, 'localhost', 14000)
    client.start_client()
