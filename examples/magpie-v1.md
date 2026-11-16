# Example Task Pack v1: Install the Local Gateway (Mac)

> Ran end to end. Target: bring up the local model gateway on the Mac,
> connect it to the local executor, run a smoke test.
> The gateway app itself was already open on the Mac (plugins page
> showed 8 installed, including the web provider plugin), so this pack
> starts from "confirm the state" and only fills gaps — nothing is
> installed twice.

## 0. Red lines (read first)

1. Any key / token / password comes only from the human (pasted by
   hand). Never write it into any file, never echo it to a log, never
   paste it into chat.
2. Review unofficial plugins before installing (the gateway app itself
   prompts this). Quick review checklist: read the repo README; read
   the entry script for key exfiltration, reads of unrelated local
   files, or pulling a remote black-box binary. If any is found, stop
   and report to the human.
3. Web-session providers (browser-login providers) are a fallback only.
   Do not promise stability for them, and do not put them in the main
   routing.
4. Smoke tests use only public synthetic text (for example, "Reply with
   the word ok."). Never test with real chat records, holdings, or
   cost data.
5. Install only from: the official gateway website, and the official
   gateway repo on GitHub.

## 1. Confirm the install state

- Check whether the app is in /Applications (or ~/Applications);
  `which magpie` / `magpie --version` should run.
- Not installed: run the official install script, then confirm with
  `magpie --version`.
- Already installed: note the version and skip the install.

## 2. Bring up the local gateway

- Start: `magpie serve` (or start inside the app). Confirm
  `127.0.0.1:3425` is listening: `lsof -i :3425`, or
  `curl -s http://127.0.0.1:3425/v1/models | head -c 300`.
- Expected: the models endpoint returns something (an empty list right
  after install is normal).

## 3. Wire up the local executor

- Install the officially recommended wiring plugin (`pi-antigravity`,
  from npm / the plugin source, following its README).
- Point the executor's model address at `http://127.0.0.1:3425`
  (back up the existing configuration first — copy before changing).
- This step only wires things up. Do not switch the executor's main
  model — switching waits for the human's decision.

## 4. Add a free model source (for the smoke test)

- Target plugin: the free-model-pool aggregator plugin (multi-account
  rotation).
- Do the code review from red line 2 first. Only then install it (via
  `magpie plugin add` or the plugin page's install method).
- Where a login or a key is needed, stop and ask the human for it.
  Never invent one, never skip it.

## 5. Smoke test

1. `curl -s http://127.0.0.1:3425/v1/models` — a model list comes back.
2. Call a chat completion once through a newly connected free model
   (content: "Reply with the word ok.", max_tokens 10) — HTTP 200 and
   normal text back.
3. From the executor side, send one minimal request through the gateway
   to confirm the link works (confirm only, no real task).

## 6. Receipt (reply in this format)

```
Gateway version:
Gateway status: listening on 127.0.0.1:3425 OK / NOT OK
Installed plugins:
Models count:
Smoke test result: model HTTP=xxx first 20 chars of reply
Executor wiring: connected (main model NOT switched) / not connected (reason)
Unfinished items:
```

## 7. Optional follow-ups (not in v1, noted here)

- Add the cloud model gateway as an upstream provider of the local
  gateway: needs the gateway key (ask the human) plus a network path
  from the Mac to the host (private mesh network or SSH — verify the
  path first).
- Main model switching, routing groups, usage / redaction settings:
  wait for the human's decision.

## 8. Rollback

- Stop the gateway: close the app or kill the process. Uninstall:
  delete the app + the gateway data directory (list it first to
  confirm).
- Restore all executor configuration changes from the backup.
