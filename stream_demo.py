"""
stream_demo.py — consume Wikipedia's real-time edit stream.

Wikipedia publishes a public, no-auth, push-based stream of every edit
happening on every Wikipedia in real time. We connect, listen, and
print each edit as it arrives.

This is real streaming — not polling. The server pushes events to us
over a long-lived HTTP connection (Server-Sent Events / SSE). We don't
ask "anything new?" every N seconds. We hold the line open and the
server tells us.

Run this and edits will scroll past your terminal live. Ctrl+C to stop.

Install:
    pip install requests sseclient-py

Run:
    python stream_demo.py             # connect to the real stream
    python stream_demo.py --mock      # replay from mock_events.jsonl
                                       # (use if conference wifi blocks SSE)
"""

import argparse
import json
import time

import requests
from sseclient import SSEClient

URL = "https://stream.wikimedia.org/v2/stream/recentchange"
MOCK_FILE = "mock_events.jsonl"


def format_event(change: dict) -> str:
    """Format one Wikipedia change event into a readable line."""
    wiki = change.get("wiki", "?")           # e.g. "enwiki", "dewiki"
    change_type = change.get("type", "?")    # "edit", "new", "log", ...
    title = change.get("title", "?")
    user = change.get("user", "anon")
    return f"[{wiki:8s}] {change_type:6s}  {title}  —  by {user}"


def stream_live() -> None:
    """Connect to the real Wikipedia EventStream and print events."""
    print(f"→ Connecting to {URL}")
    print("→ Press Ctrl+C to stop.\n")

    # stream=True keeps the connection open; the server pushes events.
    response = requests.get(URL, stream=True, headers={"Accept": "text/event-stream"})
    client = SSEClient(response)

    for event in client.events():
        if not event.data:
            continue
        try:
            change = json.loads(event.data)
        except json.JSONDecodeError:
            continue
        print(format_event(change))


def stream_mock() -> None:
    """Replay events from a local file with realistic-looking pacing.

    Use this if conference wifi blocks the live stream, or to demo
    offline. Each line in mock_events.jsonl is one event JSON.
    """
    print(f"→ Replaying from {MOCK_FILE} (mock mode)\n")
    with open(MOCK_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            change = json.loads(line)
            print(format_event(change))
            time.sleep(0.3)  # pace it like a real stream


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mock", action="store_true",
                        help="Replay from mock_events.jsonl instead of live stream")
    args = parser.parse_args()

    try:
        stream_mock() if args.mock else stream_live()
    except KeyboardInterrupt:
        print("\n→ Stream closed.")


if __name__ == "__main__":
    main()
