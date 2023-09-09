
from unittest import TestCase
from unittest.mock import MagicMock, patch

from scraper.scraper import scrape_api

RESPONSE_DATA = {"status": "OK",
                 "result": {
                     "problems": [
                         {"contestId": 1872,
                          "index": "G",
                          "name": "Replace With Product",
                          "type": "PROGRAMMING",
                          "rating": 1800,
                          "tags": ["brute force", "greedy", "math"]
                          },
                         {"contestId": 1872,
                          "index": "F",
                          "name": "Selling a Menagerie",
                          "type": "PROGRAMMING",
                          "rating": 2500,
                          "tags": ["dfs and similar", "dsu", "graphs", "implementation"]
                          }],
                     "problemStatistics": [
                         {"contestId": 1872, "index": "G", "solvedCount": 1829},
                         {"contestId": 1872, "index": "F", "solvedCount": 3007}
                     ]
                 }}


class TestScraper(TestCase):
    @patch('scraper.scraper.requests')
    def test_scrape_api(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = RESPONSE_DATA
        mock_requests.get.return_value = mock_response

        self.assertEqual(scrape_api(), {"1872G": {"name": "Replace With Product",
                                                  "difficulty": 1800,
                                                  "tags": ["brute force", "greedy", "math"],
                                                  "solutions": 1829},
                                        "1872F": {"name": "Selling a Menagerie",
                                                  "difficulty": 2500,
                                                  "tags": ["dfs and similar", "dsu", "graphs", "implementation"],
                                                  "solutions": 3007}})
