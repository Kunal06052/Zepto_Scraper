# src/utils/proxy_manager.py
import random

class ProxyManager:
    def __init__(self, proxy_list_file):
        with open(proxy_list_file, "r") as f:
            self.proxies = [line.strip() for line in f if line.strip()]
        self.index = 0

    def get_next_proxy(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.index]
        self.index = (self.index + 1) % len(self.proxies)
        return proxy

    def get_random_proxy(self):
        return random.choice(self.proxies) if self.proxies else None
