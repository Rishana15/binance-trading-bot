"""
client.py — Binance Futures Testnet API wrapper
Handles authentication, request signing, and raw HTTP communication.
"""

import hashlib
import hmac
import time
import logging
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sign(self, params: dict) -> str:
        """Generate HMAC-SHA256 signature for the given params dict."""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _request(self, method: str, path: str, params: dict = None, signed: bool = True):
        """
        Send an HTTP request to the Binance Futures Testnet.

        Args:
            method:  "GET" or "POST"
            path:    API path, e.g. "/fapi/v1/order"
            params:  query / body parameters
            signed:  whether to attach timestamp + signature

        Returns:
            Parsed JSON response (dict or list)

        Raises:
            requests.HTTPError: on 4xx/5xx responses
            requests.RequestException: on network failures
        """
        params = params or {}

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._sign(params)

        url = BASE_URL + path

        logger.debug("→ %s %s  params=%s", method, url, {k: v for k, v in params.items() if k != "signature"})

        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method == "POST":
                response = self.session.post(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.debug("← %s %s", response.status_code, response.text[:500])

            response.raise_for_status()
            return response.json()

        except requests.HTTPError as exc:
            # Try to surface the Binance error message
            try:
                body = exc.response.json()
                msg = body.get("msg", str(exc))
                code = body.get("code", "?")
                logger.error("Binance API error  code=%s  msg=%s", code, msg)
            except Exception:
                logger.error("HTTP error: %s", exc)
            raise

        except requests.RequestException as exc:
            logger.error("Network failure: %s", exc)
            raise

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------

    def get_exchange_info(self) -> dict:
        """Fetch exchange info (symbol rules, filters)."""
        return self._request("GET", "/fapi/v1/exchangeInfo", signed=False)

    def get_account(self) -> dict:
        """Fetch account balance and position information."""
        return self._request("GET", "/fapi/v2/account")

    def place_order(self, **kwargs) -> dict:
        """
        Place a futures order.

        Required kwargs (examples):
            symbol     = "BTCUSDT"
            side       = "BUY" | "SELL"
            type       = "MARKET" | "LIMIT"
            quantity   = "0.001"
            price      = "30000"   # LIMIT only
            timeInForce= "GTC"     # LIMIT only
        """
        return self._request("POST", "/fapi/v1/order", params=kwargs)

    def get_order(self, symbol: str, order_id: int) -> dict:
        """Query a specific order by its ID."""
        return self._request("GET", "/fapi/v1/order", params={"symbol": symbol, "orderId": order_id})

    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """Cancel an open order."""
        return self._request("DELETE", "/fapi/v1/order", params={"symbol": symbol, "orderId": order_id})

    def get_ticker_price(self, symbol: str) -> dict:
        """Get current mark price for a symbol."""
        return self._request("GET", "/fapi/v1/ticker/price", params={"symbol": symbol}, signed=False)
