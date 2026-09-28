import math
from typing import Dict, Any

class BondDurationConvexity:
    @classmethod
    def evaluate(cls, face_value: float, coupon_rate: float, ytm: float, maturity_years: int, freq: int = 2) -> Dict[str, Any]:
        c = (face_value * coupon_rate) / freq
        y = ytm / freq
        n = maturity_years * freq
        pvs = []
        wt = []
        conv_terms = []
        for t in range(1, n + 1):
            cf = c if t < n else c + face_value
            pv = cf / math.pow(1.0 + y, t)
            pvs.append(pv)
            wt.append(t * pv)
            conv_terms.append(t * (t + 1) * pv)
        bond_price = sum(pvs)
        mac_dur_years = (sum(wt) / bond_price) / freq
        mod_duration = mac_dur_years / (1.0 + y)
        convexity = sum(conv_terms) / (bond_price * math.pow(1.0 + y, 2) * (freq * freq))
        return {
            "bond_price": round(bond_price, 2), "macaulay_duration_years": round(mac_dur_years, 3),
            "modified_duration": round(mod_duration, 3), "convexity": round(convexity, 3)
        }

    def benchmark_bond_analytics(self) -> Dict[str, Any]:
        return self.evaluate(1000.0, 0.05, 0.04, 10)
