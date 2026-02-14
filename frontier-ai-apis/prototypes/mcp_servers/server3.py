"""Simple demo MCP server for stock trading and financial operations.

This server provides stock price queries, trading operations (buy/sell),
portfolio management, and market analysis capabilities.
"""

import random
from datetime import datetime, timedelta, timezone
import os
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field
from rich import print

mcp = FastMCP(
    name="Stock Trading MCP Server",
)

# Mock stock data
STOCK_DATA = {
    "AAPL": {"name": "Apple Inc.", "base_price": 178.50, "sector": "Technology"},
    "MSFT": {
        "name": "Microsoft Corporation",
        "base_price": 420.30,
        "sector": "Technology",
    },
    "GOOGL": {"name": "Alphabet Inc.", "base_price": 142.80, "sector": "Technology"},
    "AMZN": {
        "name": "Amazon.com Inc.",
        "base_price": 178.25,
        "sector": "Consumer Cyclical",
    },
    "TSLA": {"name": "Tesla Inc.", "base_price": 245.60, "sector": "Automotive"},
    "META": {
        "name": "Meta Platforms Inc.",
        "base_price": 490.15,
        "sector": "Technology",
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "base_price": 875.20,
        "sector": "Technology",
    },
    "JPM": {
        "name": "JPMorgan Chase & Co.",
        "base_price": 198.45,
        "sector": "Financial",
    },
    "V": {"name": "Visa Inc.", "base_price": 285.90, "sector": "Financial"},
    "WMT": {
        "name": "Walmart Inc.",
        "base_price": 165.30,
        "sector": "Consumer Defensive",
    },
}


def get_mock_price(symbol: str) -> float:
    """Generate a mock price with some random variation."""
    if symbol not in STOCK_DATA:
        return round(random.uniform(10.0, 500.0), 2)
    base = STOCK_DATA[symbol]["base_price"]
    variation = random.uniform(-0.05, 0.05)  # ±5% variation
    return round(base * (1 + variation), 2)


@mcp.tool(name="buy_stock", description="Buy shares of a stock.")
def buy_stock(
    symbol: Annotated[str, Field(description="Stock ticker symbol (e.g., AAPL, MSFT)")],
    quantity: Annotated[int, Field(description="Number of shares to buy")],
    order_type: Annotated[
        str, Field(description="Order type: market, limit, stop")
    ] = "market",
) -> dict:
    print(
        f"[green]invoking tool:buy_stock symbol={symbol}, quantity={quantity}[/green]"
    )
    price = get_mock_price(symbol)
    total_cost = price * quantity
    commission = round(total_cost * 0.001, 2)  # 0.1% commission

    return {
        "status": "executed",
        "order_id": f"ORD-{random.randint(100000, 999999)}",
        "symbol": symbol,
        "order_type": order_type,
        "quantity": quantity,
        "price_per_share": price,
        "total_cost": round(total_cost + commission, 2),
        "commission": commission,
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="sell_stock", description="Sell shares of a stock.")
def sell_stock(
    symbol: Annotated[str, Field(description="Stock ticker symbol (e.g., AAPL, MSFT)")],
    quantity: Annotated[int, Field(description="Number of shares to sell")],
    order_type: Annotated[
        str, Field(description="Order type: market, limit, stop")
    ] = "market",
) -> dict:
    print(f"[red]invoking tool:sell_stock symbol={symbol}, quantity={quantity}[/red]")
    price = get_mock_price(symbol)
    total_proceeds = price * quantity
    commission = round(total_proceeds * 0.001, 2)  # 0.1% commission

    return {
        "status": "executed",
        "order_id": f"ORD-{random.randint(100000, 999999)}",
        "symbol": symbol,
        "order_type": order_type,
        "quantity": quantity,
        "price_per_share": price,
        "total_proceeds": round(total_proceeds - commission, 2),
        "commission": commission,
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="get_stock_price", description="Get the current price of a stock.")
def get_stock_price(
    symbol: Annotated[str, Field(description="Stock ticker symbol (e.g., AAPL, MSFT)")],
) -> dict:
    print(f"[cyan]invoking tool:get_stock_price symbol={symbol}[/cyan]")
    price = get_mock_price(symbol)
    prev_close = price * random.uniform(0.97, 1.03)
    change = price - prev_close
    change_pct = (change / prev_close) * 100

    return {
        "symbol": symbol,
        "price": price,
        "currency": "USD",
        "previous_close": round(prev_close, 2),
        "change": round(change, 2),
        "change_percent": round(change_pct, 2),
        "day_high": round(price * 1.02, 2),
        "day_low": round(price * 0.98, 2),
        "volume": random.randint(10000000, 100000000),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="get_stock_info", description="Get detailed information about a stock.")
def get_stock_info(
    symbol: Annotated[str, Field(description="Stock ticker symbol (e.g., AAPL, MSFT)")],
) -> dict:
    print(f"[blue]invoking tool:get_stock_info symbol={symbol}[/blue]")

    if symbol in STOCK_DATA:
        stock_data = STOCK_DATA[symbol]
        name = stock_data["name"]
        sector = stock_data["sector"]
    else:
        name = f"{symbol} Corporation"
        sector = random.choice(["Technology", "Financial", "Healthcare", "Energy"])

    price = get_mock_price(symbol)

    return {
        "symbol": symbol,
        "company_name": name,
        "sector": sector,
        "current_price": price,
        "market_cap": f"${random.randint(100, 3000)}B",
        "pe_ratio": round(random.uniform(15, 35), 2),
        "dividend_yield": round(random.uniform(0, 3.5), 2),
        "52_week_high": round(price * random.uniform(1.1, 1.3), 2),
        "52_week_low": round(price * random.uniform(0.7, 0.9), 2),
        "avg_volume": random.randint(5000000, 50000000),
        "eps": round(random.uniform(5, 25), 2),
        "beta": round(random.uniform(0.8, 1.5), 2),
    }


@mcp.tool(name="list_portfolio", description="List all stocks in the portfolio.")
def list_portfolio() -> dict:
    print("[magenta]invoking tool:list_portfolio[/magenta]")

    portfolio_stocks = random.sample(list(STOCK_DATA.keys()), k=5)
    holdings = []
    total_value = 0

    for symbol in portfolio_stocks:
        quantity = random.randint(5, 100)
        current_price = get_mock_price(symbol)
        purchase_price = current_price * random.uniform(0.85, 1.15)
        current_value = quantity * current_price
        cost_basis = quantity * purchase_price
        gain_loss = current_value - cost_basis
        gain_loss_pct = (gain_loss / cost_basis) * 100

        holdings.append(
            {
                "symbol": symbol,
                "company_name": STOCK_DATA[symbol]["name"],
                "quantity": quantity,
                "purchase_price": round(purchase_price, 2),
                "current_price": current_price,
                "current_value": round(current_value, 2),
                "cost_basis": round(cost_basis, 2),
                "gain_loss": round(gain_loss, 2),
                "gain_loss_percent": round(gain_loss_pct, 2),
            }
        )
        total_value += current_value

    return {
        "holdings": holdings,
        "total_value": round(total_value, 2),
        "total_stocks": len(holdings),
        "currency": "USD",
        "as_of": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(
    name="get_portfolio_value",
    description="Get the total value of the portfolio.",
)
def get_portfolio_value() -> dict:
    print("[yellow]invoking tool:get_portfolio_value[/yellow]")

    total_value = random.uniform(50000, 500000)
    cash_balance = random.uniform(5000, 50000)
    total_assets = total_value + cash_balance

    return {
        "total_portfolio_value": round(total_value, 2),
        "cash_balance": round(cash_balance, 2),
        "total_assets": round(total_assets, 2),
        "currency": "USD",
        "daily_change": round(random.uniform(-5000, 5000), 2),
        "daily_change_percent": round(random.uniform(-3, 3), 2),
        "as_of": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(
    name="search_stocks",
    description="Search for stocks by name or symbol.",
)
def search_stocks(
    query: Annotated[str, Field(description="Search query for stock name or symbol")],
) -> dict:
    print(f"[cyan]invoking tool:search_stocks query={query}[/cyan]")

    # Filter stocks that match the query
    results = []
    query_lower = query.lower()

    for symbol, data in STOCK_DATA.items():
        if query_lower in symbol.lower() or query_lower in data["name"].lower():
            results.append(
                {
                    "symbol": symbol,
                    "name": data["name"],
                    "sector": data["sector"],
                    "current_price": get_mock_price(symbol),
                }
            )

    return {
        "results": results,
        "total": len(results),
        "query": query,
    }


@mcp.tool(
    name="get_stock_history",
    description="Get historical price data for a stock.",
)
def get_stock_history(
    symbol: Annotated[str, Field(description="Stock ticker symbol (e.g., AAPL, MSFT)")],
    days: Annotated[int, Field(description="Number of days of history")] = 30,
) -> dict:
    print(f"[blue]invoking tool:get_stock_history symbol={symbol}, days={days}[/blue]")

    current_price = get_mock_price(symbol)
    history = []

    for i in range(days, 0, -1):
        date = (datetime.now(timezone.utc) - timedelta(days=i)).date().isoformat()
        # Generate price with random walk
        price = current_price * random.uniform(0.95, 1.05)
        open_price = price * random.uniform(0.98, 1.02)
        high = max(price, open_price) * random.uniform(1.0, 1.02)
        low = min(price, open_price) * random.uniform(0.98, 1.0)

        history.append(
            {
                "date": date,
                "open": round(open_price, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(price, 2),
                "volume": random.randint(20000000, 80000000),
            }
        )

    return {
        "symbol": symbol,
        "history": history,
        "period_days": days,
    }


@mcp.tool(
    name="add_to_watchlist",
    description="Add a stock to your watchlist.",
)
def add_to_watchlist(
    symbol: Annotated[str, Field(description="Stock ticker symbol to watch")],
    notes: Annotated[
        str | None, Field(description="Optional notes about this stock")
    ] = None,
) -> dict:
    print(f"[green]invoking tool:add_to_watchlist symbol={symbol}[/green]")

    return {
        "status": "added",
        "symbol": symbol,
        "notes": notes or "",
        "current_price": get_mock_price(symbol),
        "added_at": datetime.now(timezone.utc).isoformat(),
        "watchlist_id": f"WL-{random.randint(1000, 9999)}",
    }


@mcp.tool(
    name="remove_from_watchlist",
    description="Remove a stock from your watchlist.",
)
def remove_from_watchlist(
    symbol: Annotated[str, Field(description="Stock ticker symbol to remove")],
) -> dict:
    print(f"[red]invoking tool:remove_from_watchlist symbol={symbol}[/red]")

    return {
        "status": "removed",
        "symbol": symbol,
        "removed_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(
    name="get_watchlist",
    description="Get all stocks in your watchlist.",
)
def get_watchlist() -> dict:
    print("[cyan]invoking tool:get_watchlist[/cyan]")

    watched_stocks = random.sample(list(STOCK_DATA.keys()), k=3)
    watchlist = []

    for symbol in watched_stocks:
        price = get_mock_price(symbol)
        prev_price = price * random.uniform(0.97, 1.03)
        change_pct = ((price - prev_price) / prev_price) * 100

        watchlist.append(
            {
                "symbol": symbol,
                "name": STOCK_DATA[symbol]["name"],
                "current_price": price,
                "change_percent": round(change_pct, 2),
                "added_at": (
                    datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))
                ).isoformat(),
            }
        )

    return {
        "watchlist": watchlist,
        "total": len(watchlist),
    }


@mcp.tool(
    name="get_market_status",
    description="Get the current market status and trading hours.",
)
def get_market_status() -> dict:
    print("[yellow]invoking tool:get_market_status[/yellow]")

    now = datetime.now(timezone.utc)
    hour = now.hour

    # US market hours: 9:30 AM - 4:00 PM EST (14:30 - 21:00 UTC)
    is_open = 14 <= hour < 21 and now.weekday() < 5

    return {
        "market": "NYSE",
        "status": "open" if is_open else "closed",
        "next_open": "2026-01-22T14:30:00Z",
        "next_close": "2026-01-21T21:00:00Z",
        "timezone": "America/New_York",
        "current_time": now.isoformat(),
        "is_trading_day": now.weekday() < 5,
    }


@mcp.tool(
    name="cancel_order",
    description="Cancel a pending stock order.",
)
def cancel_order(
    order_id: Annotated[str, Field(description="The order ID to cancel")],
) -> dict:
    print(f"[red]invoking tool:cancel_order order_id={order_id}[/red]")

    return {
        "status": "cancelled",
        "order_id": order_id,
        "cancelled_at": datetime.now(timezone.utc).isoformat(),
        "message": "Order successfully cancelled",
    }


@mcp.tool(
    name="get_order_status",
    description="Get the status of a stock order.",
)
def get_order_status(
    order_id: Annotated[str, Field(description="The order ID to check")],
) -> dict:
    print(f"[cyan]invoking tool:get_order_status order_id={order_id}[/cyan]")

    status = random.choice(["executed", "pending", "partially_filled", "cancelled"])

    return {
        "order_id": order_id,
        "status": status,
        "symbol": random.choice(list(STOCK_DATA.keys())),
        "order_type": "market",
        "side": random.choice(["buy", "sell"]),
        "quantity": random.randint(10, 100),
        "filled_quantity": random.randint(0, 100),
        "price": get_mock_price("AAPL"),
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "10000"))
    mcp.run(transport="http", host=host, port=port)
