import unittest
import time
from search import search_database, sort_results

class SortTestCase(unittest.TestCase):

    def __init__(self, methodName: str = "sortTest") -> None:
        self.search_results = search_database(["weird", "funny", "hello"])
        super().__init__(methodName)

    def setUp(self) -> None:
        self.time_start = time.time()

    def tearDown(self) -> None:
        time_elapsed = time.time() - self.time_start
        print('{} ({}s)'.format(self.id(), round(time_elapsed, 8)))

    
    def test_weird(self) -> None:
        self.assertNotEqual(sort_results(search_result=self.search_results["weird"] , keyword="weird"), None)

    def test_funny(self) -> None:
        self.assertNotEqual(sort_results(search_result=self.search_results["funny"] , keyword="funny"), None)
    
    def test_hello(self) -> None:
        self.assertNotEqual(sort_results(search_result=self.search_results["hello"] , keyword="hello"), None)

if __name__ == "__main__":
    unittest.main()