# Stream Ingestion Demo

A 30-line script that consumes Wikipedia's real-time edit stream. Run
it in your terminal during the streaming session — edits scroll by
live.

This is **real streaming**: the server pushes events to us over a
long-lived HTTP connection (Server-Sent Events). We don't poll. We
hold the line open and the server tells us.

Contrast with the batch session: there, the script pulled a snapshot
once. Here, the script holds a connection forever and reacts to events
as they arrive.

## Setup

```bash
pip install requests sseclient-py
```

## Run live (preferred)

```bash
python stream_demo.py
```

You should see edits scrolling past — `[enwiki] edit   Climate change — by SomeUser` etc.

## Run from mock data (fallback)

If conference wifi blocks the stream (rare but possible — Wikipedia's
SSE endpoint uses a persistent connection some firewalls drop), use:

```bash
python stream_demo.py --mock
```

This replays `mock_events.jsonl` with realistic pacing. Visually
identical to the live demo.

## Teaching notes

- **Don't dwell on the code.** It's 30 lines. Show it for 30 seconds.
  The point is the *output*, not the implementation.
- **Let it run for 60–90 seconds** while you talk. The output is
  hypnotic and reinforces the concept while you explain.
- **Filter live to make a point.** Mid-demo, Ctrl+C, edit the script
  to add `if wiki != "enwiki": continue` and re-run. Suddenly only
  English Wikipedia edits. Teaching moment: in real streaming, you
  filter on the consumer side. There is no "give me only English"
  query — you get everything and filter.
- **Talk about what's NOT happening.** No retries on connection drop.
  No durability if your laptop crashes mid-stream — those events are
  gone forever. That's why Kafka exists: it sits between the producer
  and the consumer, holds events durably, lets you replay.
