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

## Teaching notes

- **Don't dwell on the code.** It's ~30 lines. Show it for 30 seconds.
  The point is the *output*, not the implementation.
- **Let it run for 60–90 seconds** while you talk. The output is
  hypnotic and reinforces the concept while you explain.
- **Show the firehose first, then flip the filter.** Run unfiltered,
  let students feel the volume, Ctrl+C, rerun with `--filter-on`. The
  drop in noise is the point: in real streaming you get *everything*
  and filter on the consumer side. There is no "give me only English"
  query to the server.
- **The filter is one function.** [wikipedia.py:30-34](wikipedia.py#L30-L34) — a
  three-line predicate. Open it live and tweak: `"dewiki"` for German,
  add `namespace == 0` for articles only, etc.
- **Talk about what's NOT happening.** No retries on connection drop.
  No durability if your laptop crashes mid-stream — those events are
  gone forever. That's why Kafka exists: it sits between the producer
  and the consumer, holds events durably, lets you replay.
