# src/network/proxy_manager.py
import random
class ProxyManager:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list
        self.current_proxy = None

    def get_random_proxy(self):
        self.current_proxy = random.choice(self.proxy_list)
        return self.current_proxy