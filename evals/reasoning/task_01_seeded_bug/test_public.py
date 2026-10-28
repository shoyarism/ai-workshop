from .cart import ShoppingCart, CartItem

def test_empty_cart():
    cart = ShoppingCart("US-CA")
    res = cart.total()
    assert res["subtotal"] == 0.0
    assert res["discount"] == 0.0
    assert res["tax"] == 0.0
    assert res["total"] == 0.0

def test_basic_cart_no_discount():
    cart = ShoppingCart("DEFAULT")
    cart.add_item(CartItem("book", 20.0, 2))
    res = cart.total()
    assert res["subtotal"] == 40.0
    assert res["discount"] == 0.0
    assert res["tax"] == 2.0  # 5% of 40
    assert res["total"] == 42.0
