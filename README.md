# Stream Ingestion Demo

A ~30-line script that consumes Wikipedia's real-time edit stream. Run
it in your terminal during the streaming session — edits scroll by
live.

This is **real streaming**: the server pushes events to us over a
long-lived HTTP connection (Server-Sent Events). We don't poll. We
hold the line open and the server tells us.

Contrast with the batch session: there, the script pulled a snapshot
once. Here, the script holds a connection forever and reacts to events
as they arrive.

## Setup

Requires Python 3.13+. Either:

```bash
# with uv (recommended)
uv sync

# or with pip
pip install -r requirements.txt
```

## Run

Firehose — every change from every wiki, every language, bots and all:

```bash
python wikipedia.py
```

Filtered — English Wikipedia only:

```bash
python wikipedia.py --filter-on
```

You should see edits scrolling past — `[enwiki  ] edit    Climate change  —  by SomeUser` etc.

Each run also appends every event to `captures/<timestamp>.jsonl` so
you have a replayable record. `captures/` is gitignored.
