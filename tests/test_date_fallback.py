"""Deterministic tests for the real source of the v1.3 failure (HTTP 529)."""
from io import BytesIO
from urllib.error import HTTPError
from unittest.mock import patch
import unittest
import benchmark as b

class FakeResponse:
    def __init__(self, value):
        self.body=BytesIO(value)
    def __enter__(self):
        return self.body
    def __exit__(self,*a):
        return False

class DayResolutionTests(unittest.TestCase):
    def test_timestamp_529_retries_then_success(self):
        err=HTTPError('https://example.com',529,'overloaded',{'Retry-After':'1'},BytesIO(b'{"error":{"type":"rate_limit_error"}}'))
        with patch.object(b,'urlopen',side_effect=[err,FakeResponse(b'{"block_number":468210000}')]) as opener, \
             patch.object(b.time,'sleep') as pause:
            slot=b._timestamp_block(1794355200,timeout=2,attempts=3)
        self.assertEqual(slot,468210000)
        self.assertEqual(opener.call_count,2)
        pause.assert_called_once_with(1.)

    def test_fallback_brackets_whole_day_with_headers_only(self):
        day_start=1794355200
        anchor_slot=50000
        # Synthetic chain with exactly 2s/slot and 10,000 slots since midnight.
        anchor_ts=day_start+20000
        calls=[]
        def probe(slot,timeout=30,api_key=None):
            calls.append(slot)
            return (slot,anchor_ts+(slot-anchor_slot)*2)
        with patch.object(b,'_block_at_or_after',side_effect=probe):
            lo,hi,proof=b._fallback_date_slots(day_start,day_start+86400,anchor_slot=anchor_slot)
        self.assertLess(lo,40000)
        self.assertGreater(hi,83200)
        self.assertEqual(proof['method'],'sqd-header-fallback')
        self.assertLess(proof['edgeSamples']['from'][1],day_start)
        self.assertGreaterEqual(proof['edgeSamples']['to'][1],day_start+86400)
        self.assertLess(len(calls),100)

    def test_get_failure_uses_fallback_instead_of_failing(self):
        with patch.object(b,'_timestamp_block',side_effect=RuntimeError('HTTP 529')) as failing, \
             patch.object(b,'_fallback_date_slots',return_value=(468000000,468240000,{'method':'sqd-header-fallback'})):
            start,end,proof=b.resolve_utc_day('2026-11-11',return_details=True)
        self.assertEqual((start,end),(468000000,468240000))
        self.assertEqual(proof['method'],'sqd-header-fallback')
        self.assertEqual(failing.call_count,1)

if __name__=='__main__':unittest.main()


class DurableDateFailureTests(unittest.TestCase):
    def test_date_resolution_failure_writes_report(self):
        import json, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as temp, \
             patch.object(b,'resolve_utc_day',side_effect=RuntimeError('HTTP 529 forever')), \
             patch('sys.stderr'):
            with self.assertRaises(SystemExit):
                b.main(['--date-utc','2026-11-11','--out',temp+'/o'])
            report=json.loads((Path(temp)/'o'/'report.json').read_text())
        self.assertEqual(report['status'],'FAIL_OR_INCONCLUSIVE')
        self.assertEqual(report['stage'],'utc_date_resolution')
        self.assertIn('529',report['exception'])

    def test_one_day_slot_count_fits_cap(self):
        # Live 2026-11-11: 467914168..468316356 = 402,189 slots (~215 ms/slot).
        with patch.object(b,'resolve_utc_day',return_value=(467914168,468316356,{'method':'sqd-timestamp-api'})), \
             patch.object(b,'benchmark',return_value=0) as run:
            self.assertEqual(b.main(['--date-utc','2026-11-11','--out','unused']),0)
        run.assert_called_once()
