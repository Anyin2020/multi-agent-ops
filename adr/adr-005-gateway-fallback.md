# ADR-005: Model Gateway with a Fallback Chain

- Date: 2026-11-01
- Status: Accepted

## Context

The system depends on free-tier model APIs. Free tiers change without
notice: models disappear, quotas tighten, endpoints go down. A single
hardcoded model is a single point of failure, and every agent would
have to be reconfigured each time a provider changes something.

## Decision

All model calls go through one gateway on the host. The gateway holds
a fallback chain: if the first model in the chain fails (error,
rate limit, or payment wall), the request automatically retries on the
next model in the chain. Agents talk to the gateway, never to providers
directly.

## Consequences

- Good: a provider outage degrades the system instead of stopping it.
  The fallback has fired in practice and the work continued.
- Good: switching models is a gateway configuration change, not a
  change in every agent.
- Good: cost and usage are recorded in one place (the gateway logs),
  which the cost ledger builds on.
- Bad: the gateway is itself a single point of failure, so it runs as
  a supervised service with a restart policy, and its configuration is
  backed up before every change.
- Bad: fallback can mask a degraded model — a model that answers but
  answers badly does not trigger a retry. That is why the review chain
  (ADR-003) checks results, not just HTTP status.
- Keys for the gateway live in a 600-permission file on the host and
  never leave it. The gateway listens on the loopback and private
  network interfaces only, never on a public IP.
