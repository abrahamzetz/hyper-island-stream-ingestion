"""
stream_demo.py — consume Wikipedia's real-time edit stream.

This is real streaming, not polling. We open one HTTP connection and
the server pushes each Wikipedia edit to us as it happens (Server-Sent
Events). Each event is also appended to captures/<timestamp>.jsonl.
Ctrl+C to stop.
"""

import json
import os
from datetime import datetime

import requests
from sseclient import SSEClient

URL = "https://stream.wikimedia.org/v2/stream/recentchange"
CAPTURE_DIR = "captures"


def show(change):
    wiki = change.get("wiki", "?")
    kind = change.get("type", "?")
    title = change.get("title", "?")
    user = change.get("user", "anon")
    print(f"[{wiki:8s}] {kind:6s}  {title}  —  by {user}")


def live():
    # stream=True keeps the connection open so the server can push.
    # Wikimedia requires a descriptive User-Agent.
    response = requests.get(URL, stream=True, headers={
        "User-Agent": "stream-demo/0.1 (teaching example)",
    })

    os.makedirs(CAPTURE_DIR, exist_ok=True)
    path = f"{CAPTURE_DIR}/{datetime.now():%Y%m%d-%H%M%S}.jsonl"
    print(f"→ saving to {path}")

    with open(path, "a") as out:
        for event in SSEClient(response).events():
            if event.data:
                out.write(event.data + "\n")
                out.flush()  # so Ctrl+C doesn't lose buffered lines
                show(json.loads(event.data))


if __name__ == "__main__":
    try:
        live()
    except KeyboardInterrupt:
        print("\n→ Stream closed.")
