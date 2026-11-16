# Four-Party Council — Design Only

> Status: design only. Not implemented. Blocked on the fourth
> participant's API access, which is still pending, and on the design
> being discussed and reviewed. Do not present this as a working system.

## What changes from the three-party council

A fourth participant joins: a fourth agent, called through the model
gateway API, so that discussion becomes fully automatic and the human
can watch it live on a dashboard.

```
┌─────────────────────────────────────────────────┐
│ Unified dashboard (human's browser, live view)  │
│  ├── Monitoring panel                           │
│  ├── Token usage                                │
│  └── Council panel (topic list + discussions)   │
└─────────────────────────────────────────────────┘
         ▲
         │ render script, every 5 minutes
┌────────┴────────────────────────────────────────┐
│ council/ (host)                                 │
│  ├── topics/          topic files (md)           │
│  ├── html/            rendered group-chat HTML   │
│  └── notify-queue.json pending-decision queue    │
└─────────────────────────────────────────────────┘
         ▲
         │ four parties write in
┌────────┴────────────────────────────────────────┐
│ Participants                                    │
│  ├── Coordinator: writes files directly          │
│  ├── Ops agent: writes files via cron / exec     │
│  ├── Local executor agent: bridged manually      │
│  └── Fourth agent: called automatically via the  │
│      gateway API                                 │
└─────────────────────────────────────────────────┘
```

## Planned phases

1. **Fourth agent access.** The human provides an API key for the
   fourth agent (time-limited, rotated on schedule). The gateway
   configuration gains the new model; the key lives in a 600-permission
   file on the host and never leaves it. Acceptance: a gateway call to
   the new model returns 200.
2. **Four-party protocol.** The protocol gains a fourth-agent section
   (speak only with new information, conclusion first, same language as
   the other parties). The render script supports four speakers. The
   topic template gains a fourth section.
3. **Dashboard embedding.** The unified dashboard gains a council tab
   showing the topic list; clicking a topic opens the group-chat page.
4. **Automatic participation.** When a new topic is created, the fourth
   agent is called automatically, its contribution is written into the
   topic file, and the page re-renders.

## Risks

| Risk | Countermeasure |
|------|---------------|
| The fourth agent's key expires | Remind the human to rotate it a week before expiry; the gateway config supports hot updates. |
| The fourth agent's API rate-limits | Topic-level calls (a few a day), not high frequency; on failure, fall back to manual bridging. |
| Two parties writing at the same time | File lock or serial writes; the coordinator arbitrates. |

## Open decisions

1. The fourth agent's standing: a peer of the coordinator, or an
   advisor role?
2. Does the local executor agent stay, or is it replaced over time?
3. If the free key lapses, renew it or switch to a paid plan?
