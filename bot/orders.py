"""
orders.py — Order placement logic layer.
Sits between the CLI and the BinanceClient; handles formatting and output.
"""

import logging

from bot.client import BinanceClient
from bot.validators import validate_order_params

logger = logging.getLogger(__name__)


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None,
) -> dict:
    """
    Validate inputs, place the order, log results, and return the response.

    Args:
        client:     Authenticated BinanceClient instance
        symbol:     Trading pair, e.g. "BTCUSDT"
        side:       "BUY" or "SELL"
        order_type: "MARKET", "LIMIT", or "STOP_MARKET"
        quantity:   Order quantity as string
        price:      Limit / stop price (optional for MARKET)

    Returns:
        Binance order response dict

    Raises:
        ValueError:              on invalid inputs
        requests.HTTPError:      on Binance API errors
        requests.RequestException: on network failures
    """
    # --- Validate -------------------------------------------------------
    params = validate_order_params(symbol, side, order_type, quantity, price)

    # --- Summary --------------------------------------------------------
    print("\n" + "=" * 50)
    print("  ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol    : {params['symbol']}")
    print(f"  Side      : {params['side']}")
    print(f"  Type      : {params['type']}")
    print(f"  Quantity  : {params['quantity']}")
    if "price" in params:
        print(f"  Price     : {params['price']}")
    if "stopPrice" in params:
        print(f"  Stop Price: {params['stopPrice']}")
    print("=" * 50 + "\n")

    logger.info(
        "Placing order — symbol=%s side=%s type=%s qty=%s price=%s",
        params["symbol"],
        params["side"],
        params["type"],
        params["quantity"],
        params.get("price") or params.get("stopPrice", "N/A"),
    )

    # --- Place ----------------------------------------------------------
    response = client.place_order(**params)

    # --- Output ---------------------------------------------------------
    _print_response(response)
    logger.info("Order placed successfully — orderId=%s status=%s", response.get("orderId"), response.get("status"))

    return response


def _print_response(resp: dict) -> None:
    print("=" * 50)
    print("  ORDER RESPONSE")
    print("=" * 50)
    print(f"  Order ID     : {resp.get('orderId', 'N/A')}")
    print(f"  Status       : {resp.get('status', 'N/A')}")
    print(f"  Symbol       : {resp.get('symbol', 'N/A')}")
    print(f"  Side         : {resp.get('side', 'N/A')}")
    print(f"  Type         : {resp.get('type', 'N/A')}")
    print(f"  Orig Qty     : {resp.get('origQty', 'N/A')}")
    print(f"  Executed Qty : {resp.get('executedQty', 'N/A')}")
    avg = resp.get("avgPrice") or resp.get("price", "N/A")
    print(f"  Avg Price    : {avg}")
    print(f"  Time in Force: {resp.get('timeInForce', 'N/A')}")
    print("=" * 50)
    print("  ✅ Order placed successfully!\n")
