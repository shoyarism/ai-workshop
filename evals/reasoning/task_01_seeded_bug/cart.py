from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any
from .tax import calculate_sales_tax

class CartItem:
    def __init__(self, item_id: str, price: Any, quantity: int):
        self.item_id = item_id
        self.price = Decimal(str(price))
        self.quantity = quantity

class ShoppingCart:
    def __init__(self, region: str = "DEFAULT"):
        self.items: List[CartItem] = []
        self.region = region

    def add_item(self, item: CartItem):
        self.items.append(item)

    def subtotal(self) -> Decimal:
        return sum((i.price * i.quantity for i in self.items), Decimal("0.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def discount_rate(self) -> Decimal:
        st = self.subtotal()
        if st >= Decimal("200.00"):
            return Decimal("0.20")
        elif st >= Decimal("100.00"):
            return Decimal("0.10")
        return Decimal("0.00")

    def total(self) -> Dict[str, Any]:
        st = self.subtotal()
        rate = self.discount_rate()
        discount_amount = (st * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        net_subtotal = st - discount_amount
        # SEEDED BUG: calculates sales tax on gross subtotal instead of net subtotal
        tax = calculate_sales_tax(float(st), self.region)
        grand_total = (net_subtotal + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "subtotal": float(st),
            "discount": float(discount_amount),
            "discounted_subtotal": float(net_subtotal),
            "tax": tax,
            "total": float(grand_total)
        }
