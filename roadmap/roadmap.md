# Roadmap

Each of these grows out of something already in the system. They are
written here as ideas, with the content stated directly.

## 1. Learning loop

After each run, reflect once and propose what to keep as a note or a
skill. A note or skill is stored only after an eight-question check:
is it general, is it not planted from outside content, does it carry no
secret, is it not a duplicate, does it conflict with anything, is it
risky, is it a standing rule in disguise, is the format right. A
validation script rejects secret shapes and invisible characters before
anything is stored.

The first step is in place: the check and local git versioning. Next:
repeat something a third time and it becomes a script or a scheduled
job; a skill used three times is promoted to a workflow.

## 2. Department trust score

The current rulebook only has a demerit system for serious failures.
A score makes it continuous: ETA accuracy, receipt completeness, review
closure, and whether failures escalate after two attempts as the rules
require. Higher scores get P0 work first; lower scores get a narrower
scope. The score is a routing input, not a punishment.

## 3. Cost ledger

The task queue already records token use and cost per run. A ledger
turns that record into budgets per task and per department, with a
fallback to a cheaper model or a pause to ask the human when a budget
is hit, plus a weekly summary. The point is that the system gets
cheaper to run as it learns, not more expensive.

## 4. Attention inbox

The task queue already has an attention table. An inbox formalises it
as the human's pending-decision queue: each item has a deadline, no
reply within the window means it is cancelled or escalated rather than
left hanging, and the council's pending-decision queue feeds into it.

## 5. Permission tiers

Read-only work (L1) runs freely; write operations (L2) need a second
confirmation; the highest tier (L3) is never executed automatically —
only drafted. This tiers the blast radius, so a routine job cannot make
an irreversible change by accident.
