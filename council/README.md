# Council

The council is the deliberation mechanism for decisions that need a
second opinion. It is not a realtime chat system. It is a blackboard:
topics are files, discussion is written into the files, the discussion
is rendered as a group-chat-style page, and the human makes the final
call.

## How it works

```
Any party writes topics/ ──► a cron job detects changes ──► render
    (a topic file)              (every 5 min)                  (group-chat HTML)
                                                              │
                                              status becomes "awaiting decision"
                                                              │
                                              pending-decision queue (notify-queue.json)
                                                              │
                                              the coordinator pushes a digest to the human
```

Storage (on the host):

```
council/
├── topics/                 # Topic files: YYYYMMDD-NNN-slug.md
├── archive/                # Decided topics
├── html/                   # Rendered output: same name, .html
└── notify-queue.json       # Pending-push queue
```

## Topic file protocol

```markdown
# Topic #007 · Title
- Status: discussing | awaiting decision | archived
- Started by: Coordinator · 2026-11-02 09:00
- Participants: Coordinator, Local Executor, Ops Agent

## Background
(why this is being discussed, the current state in one sentence)

## Options
- A: ...
- B: ...

## Discussion
### Coordinator · 09:00
...
### Local Executor · 09:17
...

## Conclusion
- Conclusion: ...
- Awaiting decision: ... (write "none, awaiting confirmation" if there is no disagreement)

## Decision record
- Human · 2026-11-02 10:05: chose A
```

## Governance rules (in the protocol header, binding on all parties)

1. The human decides. Deliberation produces advice only; the decision
   is always the human's.
2. No small talk: do not speak without new information. Agreement,
   politeness, and repetition count as violations.
3. One topic per file: if the discussion drifts, open a new topic.
4. A conclusion must be executable: who does what, and when it is
   verified.

## Roles

| Party | How it participates |
|-------|---------------------|
| Coordinator (personal agent) | Writes topic files directly; renders and pushes digests; accepts and verifies. |
| Ops agent | A scheduled job scans topics every 30 minutes; replies to topics addressed to it; pushes a digest when a topic becomes "awaiting decision". |
| Local executor agent | Reads and writes topic files directly over SSH. It is not a resident process, so it does not poll: when a topic addresses it, the ops agent's digest reminds the human, and the human asks it to look. |

## Rollout (as it actually happened)

- Phase 1: blackboard directory + protocol file.
- Phase 2: render script (standard library only), re-rendering only on
  change; idempotent — re-running never sends a duplicate push.
- Phase 3: ops agent participation on a 30-minute schedule, plus digest
  pushes for new "awaiting decision" topics.
- Phase 4: coordinator checks the pending-decision queue every 30
  minutes and pushes to the human.
- Phase 5: trial run — one real topic through the full chain: start,
  three-party discussion, conclusion, two-channel push, human decision,
  archive.

## What it is not

- Not a realtime chat or group-chat system.
- Not a web admin panel.
- Not a replacement for the human's decision.

## Rollback

Stop the cron jobs and delete the council directory. Topic files are
plain markdown and stay readable at any time; nothing is locked in.
