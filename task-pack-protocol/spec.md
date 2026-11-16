# Task-Pack Protocol

A task pack is the written contract between the coordinator (the personal
agent) and the executor. Planning and execution are separated by this
document: the coordinator plans, the executor executes, and the
coordinator verifies the result against the pack. No verbal instructions,
no improvisation at the interface.

## What a task pack contains

1. **Red lines first.** The non-negotiable constraints, read before
   anything else. Typical red lines:
   - Keys, tokens, and passwords come only from the human (pasted by
     hand). They are never written into any file, never echoed to a log,
     never pasted into chat.
   - Smoke tests use only public synthetic text (for example, "Reply with
     the word ok."). Never test with real chat records, holdings, or
     cost data.
   - Install only from official sources. Unofficial plugins are code-
     reviewed before installing (read the README, read the entry script
     for key exfiltration, unrelated local file reads, or remote black-box
     binaries; stop and report if any is found).
   - Back up configuration before changing it, and know the rollback.
2. **Prerequisites.** Conditions to confirm before starting. If any one
   is missing, stop and report; do not work around it.
3. **Steps.** The exact commands to run, verified beforehand and written
   in full — no ellipses, no "and so on". The executor follows them
   literally.
4. **Smoke test.** A minimal check that the work actually works, run
   before reporting done.
5. **Receipt format.** A fixed template the executor fills in, item by
   item. Every field is answered; uncompleted items are listed, not
   hidden.
6. **Rollback.** How to undo the change, including where the backup lives.

## Rules of the protocol

- The executor follows the pack literally. If a step is wrong, the
  executor stops and reports; it does not improvise a fix.
- A step the executor cannot do is reported as uncompleted, with the
  reason. The pack is never marked complete with silent gaps.
- The coordinator verifies the result against the pack's hidden checks
  (checks the executor cannot see in advance). Verification is
  independent of execution.
- A task pack is versioned (v1, v2, ...). A later version supersedes the
  earlier one; the earlier version is kept for reference, not reused.

## History in this repo

- v1: install the local gateway on the Mac, bring up the local gateway,
  wire it to the local executor, add one free model source, smoke test.
  See `examples/magpie-v1.md`.
- v2: connect the cloud gateway as an upstream provider.
- v3: add a second free-tier provider as a backup source.
- v4: reconfiguration after a system reinstall — the roll-up of v1+v2+v3,
  adjusted to the post-reinstall state, with expired items removed.
  See `examples/magpie-v4-reinstall.md`.
