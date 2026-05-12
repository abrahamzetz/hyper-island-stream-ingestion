"""
stream_demo.py — consume Wikipedia's real-time edit stream.

This is real streaming, not polling. We open one HTTP connection and
the server pushes each Wikipedia edit to us as it happens (Server-Sent
Events). Each event is also appended to captures/<timestamp>.jsonl.
Ctrl+C to stop.
"""

import json
import os
import sys
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


def live(filter=False):
    # stream=True keeps the connection open so the server can push.
    # Wikimedia requires a descriptive User-Agent.
    response = requests.get(URL, stream=True, headers={
        "User-Agent": "stream-demo/0.1 (teaching example)",
    })

    os.makedirs(CAPTURE_DIR, exist_ok=True)
    path = f"{CAPTURE_DIR}/wiki_{datetime.now():%Y%m%d-%H%M%S}.jsonl"
    print(f"→ saving to {path}")
    print(f"→ filter: {'enwiki articles only' if filter else 'off (firehose)'}")

    with open(path, "a", encoding="utf-8") as out:
        for event in SSEClient(response).events():
            if not event.data:
                continue
            stream_data = json.loads(event.data)
            if filter and not keep(stream_data):
                continue
            out.write(event.data + "\n")
            out.flush()  # so Ctrl+C doesn't lose buffered lines
            show(stream_data)


if __name__ == "__main__":
    # Pass "--filter-on" on the command line to enable the filter:
    #   python stream_demo.py               → everything (firehose)
    #   python stream_demo.py --filter-on   → enwiki only
    filter_on = "--filter-on" in sys.argv

    try:
        live(filter_on)
    except KeyboardInterrupt:
        print("\n→ Stream closed.")
