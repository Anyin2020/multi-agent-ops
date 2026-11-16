# ADR-004: Council as Files, Not a Chat System

- Date: 2026-11-01
- Status: Accepted

## Context

Decisions that need a second opinion were being made in passing, in
chat, with no record of who said what and no clear point where the
human decides.

## Decision

Deliberation runs on files, not on a realtime chat system. A topic is
a markdown file in a shared directory; each party appends its signed
contribution; a render script turns the file into a group-chat-style
page; a pending-decision queue tells the human what is waiting for a
call. The human decides; the council only advises.

## Consequences

- Good: the whole discussion is a durable, readable record. Nothing is
  lost when a session ends.
- Good: no new infrastructure — files, a cron job, and a render script.
  Rollback is deleting the directory.
- Bad: it is not realtime. Parties that are not resident processes
  (the local executor agent) only join when the human asks them to.
- Bad: a file-based protocol needs discipline — no small talk, one
  topic per file, conclusions that are executable.
- The four-party extension (a fourth agent called automatically through
  the gateway API) is a design only, documented in
  `council/four-party-design.md`. It is not implemented.
