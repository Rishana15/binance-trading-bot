"""
validators.py — CLI input validation for the trading bot.
All functions raise ValueError with a human-readable message on failure.
"""

from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s:
        raise ValueError("Symbol cannot be empty.")
    if not s.isalnum():
        raise ValueError(f"Symbol '{s}' contains invalid characters. Example: BTCUSDT")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValueError(f"Side must be one of {sorted(VALID_SIDES)}, got '{side}'.")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be one of {sorted(VALID_ORDER_TYPES)}, got '{order_type}'.")
    return t


def validate_quantity(quantity: str) -> str:
    try:
        q = Decimal(quantity)
    except InvalidOperation:
        raise ValueError(f"Quantity '{quantity}' is not a valid number.")
    if q <= 0:
        raise ValueError(f"Quantity must be positive, got {q}.")
    return str(q)


def validate_price(price: str) -> str:
    try:
        p = Decimal(price)
    except InvalidOperation:
        raise ValueError(f"Price '{price}' is not a valid number.")
    if p <= 0:
        raise ValueError(f"Price must be positive, got {p}.")
    return str(p)


def validate_order_params(symbol: str, side: str, order_type: str, quantity: str, price: str = None) -> dict:
    """
    Validate all order parameters together and return a cleaned params dict
    ready to pass to BinanceClient.place_order().

    Raises ValueError for any invalid input.
    """
    params = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
    }

    if params["type"] == "LIMIT":
        if not price:
            raise ValueError("Price is required for LIMIT orders.")
        params["price"] = validate_price(price)
        params["timeInForce"] = "GTC"  # Good-Till-Cancelled

    elif params["type"] == "STOP_MARKET":
        if not price:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        params["stopPrice"] = validate_price(price)

    elif params["type"] == "MARKET" and price:
        raise ValueError("Price should not be provided for MARKET orders.")

    return params
