from pyparsing import C
import database
from collections import OrderedDict

class Cache():
    def __init__(self, size) -> None:
        self.size = size
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
        
    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.size:
            self.cache.popitem(last = False)

search_results = Cache(50)
terms = Cache(100)
kanji = Cache(150)
