"""
Tax calculation utility.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict

RATES: Dict[str, str] = {
    "US-CA": "0.0825",
    "US-NY": "0.08875",
    "US-TX": "0.0625",
    "DEFAULT": "0.05",
}

def calculate_sales_tax(subtotal: float, region: str) -> Decimal:
    rate_str = RATES.get(region, RATES["DEFAULT"])
    d_subtotal = Decimal(str(subtotal))
    d_rate = Decimal(rate_str)
    return (d_subtotal * d_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
