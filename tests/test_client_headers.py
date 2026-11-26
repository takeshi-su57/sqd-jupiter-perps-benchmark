"""Verify public SQD query uses an explicitly identified API client."""
import unittest
from unittest.mock import patch
import benchmark


class _FakeResponse:
    status = 200
    headers = {}
    body = b'{"header":{"number":468300000}}\n'

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def __iter__(self):
        return iter([b'{"header":{"number":468300000}}\n'])


class HeadersTests(unittest.TestCase):
    def test_explicit_sqd_client_headers(self):
        with patch.object(benchmark, 'urlopen', return_value=_FakeResponse()) as urlopen:
            result = benchmark.request_stream({"type":"solana", "fromBlock":468300000, "toBlock":468300000})
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(request.get_header('User-agent'), 'LuckyPlans-SQD-AccuracyBenchmark/1.4')
        self.assertEqual(request.get_header('Accept'), 'application/jsonl')
        self.assertEqual(request.get_header('Content-type'), 'application/json')
        self.assertEqual(request.get_header('Accept-encoding'), 'gzip')
        self.assertEqual(len(result), 1)

    def test_gzip_body_is_decoded_and_key_uses_bearer(self):
        import gzip
        lines = b'{"header":{"number":1}}\n{"header":{"number":2}}\n'
        fake = _FakeResponse(); fake.body = gzip.compress(lines); fake.headers = {'Content-Encoding': 'gzip'}
        with patch.object(benchmark, 'urlopen', return_value=fake) as urlopen:
            result = benchmark.request_stream({"type": "solana", "fromBlock": 1, "toBlock": 2}, api_key='k')
        self.assertEqual(b''.join(result), lines)
        self.assertEqual(len(result), 2)
        self.assertEqual(urlopen.call_args.args[0].get_header('Authorization'), 'Bearer k')

    def test_lean_query_filters_events_server_side(self):
        q = benchmark.build_query(1, 2)
        self.assertEqual(q['instructions'][0]['d8'], ['0xe445a52e51cb9a1d'])
        self.assertIs(q['instructions'][0]['isCommitted'], True)
        self.assertNotIn('d8', benchmark.build_query(1, 2, mode='full')['instructions'][0])

if __name__ == '__main__':
    unittest.main()
