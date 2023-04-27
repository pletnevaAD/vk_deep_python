import argparse
import json
import queue
import socket
import sys
import threading

import requests


class Server:
    def __init__(self, num_workers, num_top_words, host, port):
        self.thread_master = threading.Thread(target=self.master_function, name="Master")
        self.threads_workers = [threading.Thread(target=self.worker_fun, name=f'Worker_{i}') for i in
                                range(num_workers)]
        self.num_top_words = num_top_words
        self.url_queue = queue.Queue()
        self.url_completed = 0
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(num_workers)
        self._client = None
        self.running = False

    def start_server(self):
        self.running = True
        self.thread_master.start()

    def master_function(self):
        while self.running:
            self._client, addr = self.socket.accept()
            for worker in self.threads_workers:
                worker.start()
            while True:
                try:
                    url = self._client.recv(1024).decode('utf-8')
                except Exception:
                    continue
                self.url_queue.put(url)
        self.thread_master.join()
        self._client.close()
        self.socket.close()

    def worker_fun(self):
        while self.running:
            try:
                url = self.url_queue.get()
            except Exception:
                continue
            self.url_queue.task_done()
            text = requests.get(url, timeout=5)
            words = {i: text.text.count(i) for i in set(text.text.split())}
            self._client.send(bytes(f"{url}: " + json.dumps(
                dict(sorted(words.items(), key=lambda item: item[1], reverse=True)[:self.num_top_words]),
                ensure_ascii=False),
                                    "utf-8"))
            self.url_completed += 1
            print(f'Обработано ссылок: {self.url_completed}')
        for worker in self.threads_workers:
            worker.join()

    def stop_server(self):
        if self.running:
            self.running = False



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', default=0, type=int)
    parser.add_argument('-k', default=0, type=int)
    server_input = parser.parse_args(sys.argv[1:])
    server = Server(5, 7, 'localhost', 14000)
    server.start_server()
