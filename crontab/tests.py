
from django.test import TestCase
from unittest.mock import MagicMock, patch

from crontab.manager import scan, distrib
from problems.models import Problem, Tag, Belonging

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

class ScanCodeforcesTestCase(TestCase):
    @patch('scraper.scraper.requests')
    def test_scan_codeforces(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = RESPONSE_DATA
        mock_requests.get.return_value = mock_response

        scan()

        problem1 = Problem.objects.get(number="1872F")
        problem2 = Problem.objects.get(number="1872G")

        self.assertEqual(problem1.difficulty, 2500)
        self.assertEqual(problem2.difficulty, 1800)
        self.assertEqual(problem1.solutions, 3007)
        self.assertEqual(problem2.solutions, 1829)

class DistributeTestCase(TestCase):
    @patch('scraper.scraper.requests')
    def setUp(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = RESPONSE_DATA
        mock_requests.get.return_value = mock_response

        scan()

    def test_distribute(self):
        distrib()

        tag1 = Tag.objects.get(name="dfs and similar")
        tag2 = Tag.objects.get(name="dsu")
        tag3 = Tag.objects.get(name="graphs")
        tag4 = Tag.objects.get(name="implementation")
        tag5 = Tag.objects.get(name="brute force")
        tag6 = Tag.objects.get(name="greedy")
        tag7 = Tag.objects.get(name="math")

        problem1 = Problem.objects.get(number="1872F")
        problem2 = Problem.objects.get(number="1872G")

        self.assertTrue(Belonging.objects.filter(tag=tag1, problem=problem1).exists())
        self.assertFalse(Belonging.objects.filter(tag=tag2, problem=problem1).exists())
        self.assertFalse(Belonging.objects.filter(tag=tag3, problem=problem1).exists())
        self.assertFalse(Belonging.objects.filter(tag=tag4, problem=problem1).exists())
        self.assertTrue(Belonging.objects.filter(tag=tag5, problem=problem2).exists())
        self.assertFalse(Belonging.objects.filter(tag=tag6, problem=problem2).exists())
        self.assertFalse(Belonging.objects.filter(tag=tag7, problem=problem2).exists())
