from decimal import Decimal
from .cart import ShoppingCart, CartItem

def test_tiered_discount_and_net_tax():
    cart = ShoppingCart("US-CA")  # Rate is 0.0825
    cart.add_item(CartItem("widget", 50.0, 2))  # Subtotal 100.0
    res = cart.total()
    
    assert res["subtotal"] == 100.0
    assert res["discount"] == 10.0
    assert res["discounted_subtotal"] == 90.0
    # Sales tax MUST be a Decimal instance and equal to Decimal("7.43"):
    # (Decimal('7.43') == 7.43 evaluates to False in Python)
    assert isinstance(res["tax"], Decimal), f"Tax must be a Decimal instance, got {type(res['tax'])}"
    assert res["tax"] == Decimal("7.43"), f"Expected tax to be Decimal('7.43'), got {res['tax']}"

def test_half_up_boundary_case_tx():
    """
    Discriminates Decimal ROUND_HALF_UP from naive float banker's rounding.
    10.00 * 0.0625 = 0.625.
    - Decimal ROUND_HALF_UP -> Decimal('0.63')
    - Naive float round(0.625, 2) -> 0.62 (round-half-to-even)
    """
    cart = ShoppingCart("US-TX")  # Rate is 0.0625
    cart.add_item(CartItem("gadget", 10.0, 1))  # Subtotal 10.0, no discount
    res = cart.total()
    
    assert res["subtotal"] == 10.0
    assert res["discount"] == 0.0
    assert res["discounted_subtotal"] == 10.0
    assert isinstance(res["tax"], Decimal), f"Tax must be a Decimal instance, got {type(res['tax'])}"
    assert res["tax"] == Decimal("0.63"), f"Expected tax under Decimal ROUND_HALF_UP to be Decimal('0.63'), got {res['tax']}"

def test_large_tier_discount_and_net_tax():
    cart = ShoppingCart("US-NY")  # Rate is 0.08875
    cart.add_item(CartItem("laptop", 250.0, 1))  # Subtotal 250.0
    res = cart.total()
    
    assert res["subtotal"] == 250.0
    assert res["discount"] == 50.0  # 20%
    assert res["discounted_subtotal"] == 200.0
    # Sales tax on $200.0 at 0.08875 = 17.75
    assert isinstance(res["tax"], Decimal), f"Tax must be a Decimal instance, got {type(res['tax'])}"
    assert res["tax"] == Decimal("17.75"), f"Expected tax on discounted subtotal $200.0 to be Decimal('17.75'), got {res['tax']}"
