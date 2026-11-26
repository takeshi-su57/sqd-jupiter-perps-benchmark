"""Offline tests for summarize.consistency() using field shapes seen in real 2026-11-11 data."""
import unittest
import summarize as s

def cand(action, fields, size, name='InstantDecreasePositionEvent'):
    return ({'action':action,'eventName':name,'isExecutedSizeChange':True,'sizeUsdDeltaRaw':str(size),
             'signature':'5'*88,'allEventFields':{k:str(v) if isinstance(v,int) and not isinstance(v,bool) else v
                                                 for k,v in fields.items()}},[])

class ConsistencyTests(unittest.TestCase):
    def test_real_shaped_long_close_in_profit_passes(self):
        # Long, entry 80.00, exit 84.00, $1,000 closed -> +$50 PnL.
        f={'positionPrice':80_000_000,'price':84_000_000,'pnlDelta':50_000_000,'hasProfit':True,
           'positionSide':1,'positionSizeUsd':0,'feeUsd':700_000,'positionFeeUsd':600_000,'fundingFeeUsd':100_000}
        checks,fails,info=s.consistency([cand('DECREASE',f,1_000_000_000)])
        self.assertFalse(fails)
        self.assertEqual(checks['pnl_matches_entry_exit_formula_1pct_ok'],1)
        self.assertEqual(checks['pnl_sign_matches_side_and_price_ok'],1)
        self.assertEqual(checks['fee_eq_position_fee_plus_funding_ok'],1)

    def test_wrong_sign_or_scale_fails(self):
        f={'positionPrice':80_000_000,'price':84_000_000,'pnlDelta':5_000_000,'hasProfit':False,
           'positionSide':1,'feeUsd':1,'positionFeeUsd':1,'fundingFeeUsd':1}
        checks,fails,info=s.consistency([cand('DECREASE',f,1_000_000_000)])
        self.assertEqual(checks['pnl_sign_matches_side_and_price_FAIL'],1)
        self.assertEqual(checks['pnl_matches_entry_exit_formula_1pct_FAIL'],1)
        self.assertEqual(checks['fee_eq_position_fee_plus_funding_FAIL'],1)

    def test_liquidation_protocol_zero_pnl_is_informational(self):
        f={'positionPrice':83_058_110,'price':82_838_341,'pnlDelta':0,'hasProfit':True,'positionSide':2,
           'feeUsd':1_860_611,'positionFeeUsd':1_860_502,'fundingFeeUsd':109,'originalPositionCollateralUsd':9615}
        checks,fails,info=s.consistency([cand('LIQUIDATE',f,2_657_859_520,'LiquidateFullPositionEvent')])
        self.assertFalse(fails)
        self.assertEqual(checks['liquidation_pnl_protocol_adjusted_info'],1)
        self.assertEqual(len(info),1)

if __name__=='__main__':unittest.main()
