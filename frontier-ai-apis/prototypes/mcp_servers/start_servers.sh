#!/usr/bin/env bash
# Start all 3 MCP servers from toolscout (for levels that need them)
# Server 1: General (users, weather, email) — port 8000
# Server 2: Library management — port 9000
# Server 3: Stock trading — port 10000

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting MCP servers..."
python "$DIR/server1.py" &
echo "  Server 1 (General)  → http://localhost:8000"

python "$DIR/server2.py" &
echo "  Server 2 (Library)  → http://localhost:9000"

python "$DIR/server3.py" &
echo "  Server 3 (Stocks)   → http://localhost:10000"

echo ""
echo "All servers started. Press Ctrl+C to stop."
wait
