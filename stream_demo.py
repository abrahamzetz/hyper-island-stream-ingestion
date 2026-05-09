"""
stream_demo.py — consume Wikipedia's real-time edit stream.

This is real streaming, not polling. We open one HTTP connection and
the server pushes each Wikipedia edit to us as it happens (Server-Sent
Events). Each event is also appended to captures/<timestamp>.jsonl.
Ctrl+C to stop.
"""

import argparse
import json
import os
from datetime import datetime

import requests
from sseclient import SSEClient

URL = "https://stream.wikimedia.org/v2/stream/recentchange"
CAPTURE_DIR = "captures"


def show(stream_data):
    wiki = stream_data.get("wiki", "?")
    kind = stream_data.get("type", "?")
    title = stream_data.get("title", "?")
    user = stream_data.get("user", "anon")
    print(f"[{wiki:8s}] {kind:6s}  {title}  —  by {user}")


def keep(stream_data):
    # English Wikipedia only
    return (
        stream_data.get("wiki") == "enwiki"
    )


def live(filter_on):
    # stream=True keeps the connection open so the server can push.
    # Wikimedia requires a descriptive User-Agent.
    response = requests.get(URL, stream=True, headers={
        "User-Agent": "stream-demo/0.1 (teaching example)",
    })

    os.makedirs(CAPTURE_DIR, exist_ok=True)
    path = f"{CAPTURE_DIR}/{datetime.now():%Y%m%d-%H%M%S}.jsonl"
    print(f"→ saving to {path}")
    print(f"→ filter: {'enwiki articles only' if filter_on else 'off (firehose)'}")

    with open(path, "a") as out:
        for event in SSEClient(response).events():
            if not event.data:
                continue
            stream_data = json.loads(event.data)
            if filter_on and not keep(stream_data):
                continue
            out.write(event.data + "\n")
            out.flush()  # so Ctrl+C doesn't lose buffered lines
            show(stream_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--filter-on",
        action="store_true",
        help="filter to English Wikipedia articles only (default: show everything)",
    )
    args = parser.parse_args()

    try:
        live(filter_on=args.filter_on)
    except KeyboardInterrupt:
        print("\n→ Stream closed.")
