# Department Operating Rules (20 rules)

> Approved by the human, effective 2026-11-02.
> Applies to every department. The rules are equal for everyone.
> If a direct instruction from the human conflicts with any rule here,
> the human's instruction wins.

## 1. Dispatch

1. **Ask on the spot.** If a task is unclear, out of scope, or you do not
   know how to do it, ask when the task is assigned. Accepting a task is a
   commitment. Saying "I can't do this" after the fact counts as a failure
   to perform.
2. **ETA to the hour.** An ETA must be exact, e.g. "Nov 3, 15:00". Vague
   ETAs ("afternoon", "tonight") are not accepted. The coordinator may
   correct an unreasonable ETA based on the size of the work.
3. **Priority tiers.** Every dispatched task is tagged P0, P1, or P2:
   P0 = fault, jumps the queue; P1 = main line, in order; P2 = improvement,
   done when idle.

## 2. Execution

4. **Report within 2 hours.** If there is no substantial progress 2 hours
   after accepting a task, report the reason and a new ETA on your own
   initiative. Do not wait to be asked.
5. **Escalate after two failures.** If the same task fails twice, it is
   automatically handed to another department or escalated to the
   coordinator. No approval from the human is needed for the escalation.
6. **No added scope.** Execute the task pack literally. Do not add
   requirements of your own (for example, adding a database to a script
   that did not ask for one). Ask first if you want to add something.
7. **Code standards.** Standard library first; no heavy dependencies.
   No hardcoded IPs or secrets. A secret is recorded by its location only,
   never by its value.

## 3. Reporting (progress receipts)

8. **Four reporting points.** Within 10 minutes of starting, at milestones,
   immediately when blocked, and immediately when done. Start receipts with
   `[progress]`, `[done]`, or `[blocked]` followed by one sentence on the
   state; details go separately.
9. **Two copies for milestones.** A milestone receipt is sent twice: once
   in the department channel and once to the coordinator (marked
   `[sync to coordinator]`).
10. **Report good news and bad news alike.** Report when the work is done
    either way. Never give up lightly: a failure report must list which
    approaches were tried, where it got stuck, and what alternatives remain.

## 4. Acceptance (three lines)

11. **It runs** (the floor, not the finish line): the service is reachable,
    the interface responds, the tests pass.
12. **The data is real**: displayed data must come from a real source, not
    hardcoded values, placeholders, or a fudged "unknown". If something
    cannot be computed, say so honestly instead of making it up.
13. **The experience is smooth**: copy is consistent, front end and back
    end agree, no hardcoded hazards, nothing confusing to the user.
14. **Acceptance checklist.** After each acceptance, the coordinator sends
    the human a checklist of what was verified (the human spot-checks it).
    Anything that fails is sent back. Nothing ships with a known defect.
15. **A receipt is complete only when synced.** A milestone receipt is
    complete only when both copies exist (department channel + coordinator).
    A missing copy means the milestone is incomplete and acceptance fails.
    This is a hard gate, not a suggestion.

## 5. Escalation

16. **Failure record.** A serious failure (for example, 11 hours with zero
    output, or three missed ETAs) is written up once: what was tried, where
    it got stuck, and what changes. The write-up is kept as a reference so
    the next attempt does not repeat it.
17. **Escalation path.**
    ```
    Agent fails → retry once with the same agent
    Still fails → escalate to another department or the coordinator
    Coordinator cannot fix it → mark it for a human decision
    ```
18. **Cross-model review.** Every script, wrapper, and configuration change
    goes through three quality gates (author self-test → review by a
    different model → coordinator acceptance). A model never reviews its
    own work. See `review/`.

## 6. Notes

19. **The human is final.** If a direct instruction from the human
    conflicts with any rule here, the human's instruction wins.
20. **Rules change.** The human may add, remove, or change rules at any
    time. The coordinator is responsible for syncing the change to every
    department and updating this document.
