# Example Task Pack v4: Reconfigure the Gateway After a System Reinstall (Mac)

> Ran end to end. Target: after a macOS downgrade + reinstall, reconnect
> the free model sources to the local gateway, connect the local
> executor, and run a smoke test.
> This pack is the roll-up of v1 (install + gateway + executor wiring +
> free-model plugin), v2 (cloud gateway as upstream), and v3 (a second
> free-tier provider), redone for the post-reinstall state, with expired
> items removed.
> State: the gateway was reinstalled (the agent page shows the executor
> CLI is connected and the gateway has written its CLI shim into the
> shell profile). The Mac-side gateway configuration is treated as
> fresh / blank. The host side was untouched and verified healthy.
> This round connects free sources only. It does not switch the
> executor's main model.

## 0. Red lines (read first)

1. Any key / token / password comes only from the human (pasted by
   hand). Never write it into any file, never echo it to a log, never
   paste it into chat.
2. The gateway key: if the human does not have it, ask the coordinator
   (the coordinator hands it over through a secure channel). The task
   pack only ever says "ask the coordinator" — never the key itself,
   and never go looking through key files yourself.
3. Review unofficial plugins before installing (see v1 red line 2 for
   the checklist). The free-model plugin below has a reviewed record
   for the same version, so reinstalling the same version may take the
   fast lane — but the version and source must match the reviewed
   record, or the full review runs again.
4. Smoke tests use only public synthetic text. Never test with real
   chat records, holdings, or cost data.
5. Install only from: the official gateway website, and the official
   gateway repo on GitHub.
6. Only add providers and plugins. Do not switch the executor's main
   model, do not touch existing configuration; back up configuration
   before changing it (see step 4).
7. Web-session providers (browser-login providers) are a fallback only.
   Do not promise stability for them, and do not put them in the main
   routing.

## 1. Prerequisites (confirm before starting; if any is missing, stop and ask)

- The human has completed the Mac's private-mesh-network login
  (a reinstall may require logging in again — see step 2).
- Gateway key: ask the coordinator (the human pastes it).
- Second provider's API key: ask the human (pasted by hand; it can be
  found in that provider's dashboard).
- Sign-in for the free-tier provider is done for today.

## 2. Bring the Mac onto the private mesh network

- `tailscale status` to check the state. (The mesh client is the
  private-network tool; the commands below use its CLI.)
- Offline: start the mesh client app, wait 30 seconds, check again.
  Still down: stop, report to the human, and let the human open the
  client and log in by hand.
- Once online, verify the link: `curl -s -m 10 -o /dev/null -w
  "%{http_code}\n" http://<GATEWAY_HOST>:4000/v1/models`. A 401 or 500
  without a key still counts as connected (it reached the gateway).

## 3. Verify the gateway is reachable (with key)

- Ask the coordinator for the gateway key (the human pastes it).
- `curl -s -H "Authorization: Bearer <key>"
  http://<GATEWAY_HOST>:4000/v1/models` should return the model list.
- Not reachable → stop, report, do not continue.

## 4. Bring up the local gateway (confirm state after reinstall; fill gaps)

- Confirm the app is in /Applications (or ~/Applications);
  `magpie --version` to note the version.
- Not installed: run the official install script, then confirm with
  `magpie --version`. Already installed: skip the install.
- Back up configuration before changing it: list the data directory
  first to confirm it exists, then copy it to a `.bak-v4` backup.
  Do the same for any executor configuration before changing it.
- Start: `magpie serve` (or start inside the app). Confirm
  `127.0.0.1:3425` is listening (`lsof -i :3425`, or
  `curl -s http://127.0.0.1:3425/v1/models | head -c 300`).
- Expected: the models endpoint returns something (an empty list right
  after a fresh install is normal; providers are added next).

## 5. Add the cloud gateway provider (main free pool)

- In the gateway app: providers → add provider → OpenAI-compatible
  custom endpoint (or the CLI equivalent):
  - Name: `gateway-provider`
  - Base URL: `http://<GATEWAY_HOST>:4000/v1` (the mesh network
    encrypts the traffic, so plain HTTP is fine)
  - API key: the gateway key (the human pastes it)
- After adding, the gateway's model list should show the host models.

## 6. Add the second free-tier provider (backup / supplement, not the main pool)

- Ask the human for the provider's API key.
- Verify the provider endpoint is reachable first (direct from the
  Mac): a `curl` with the key against the provider's models endpoint
  should return a model list.
- Not reachable → stop, report, do not continue.
- In the gateway app: providers → add provider → OpenAI-compatible
  custom endpoint:
  - Name: `second-provider`
  - Base URL: the provider's API base URL
  - API key: the provider's key (the human pastes it)
- Register the free models currently available (use the list returned
  in the verification step).
- Position: backup / supplement, not the main pool — the free pool
  shrinks from time to time and the daily free allowance is small, so
  do not run bulk jobs through it.

## 7. Reinstall the free-model plugin (pool aggregator + multi-account rotation)

- Target plugin: the free-model-pool plugin.
- Review: this plugin was reviewed for the same version before;
  reinstalling the same version may skip the repeat review, but the
  version and source must match the reviewed record. If they do not
  match, run the full code review from red line 3 first.
- After passing, `magpie plugin add <plugin-name>` (or the plugin
  page's install method).
- Where a login or a key is needed, stop and ask the human for it.
  Never invent one, never skip it.

## 8. Confirm the executor wiring and CLI (verify only, do not reinstall)

- The agent page already shows the executor CLI is connected and the
  gateway wrote its CLI shim into the shell profile. This step does not
  reinstall the wiring plugin; it only verifies.
- Open a new terminal, run the executor CLI, confirm it starts and
  goes through the local gateway at `http://127.0.0.1:3425`, then quit.
  Do not run a real task.
- If the CLI does not start or does not go through the local gateway,
  stop and report. Do not change the wiring configuration yourself.

## 9. Smoke test

1. `curl -s http://127.0.0.1:3425/v1/models` — the list shows host
   models and second-provider models.
2. Call one chat completion through the gateway with any available
   model (content: "Reply with the word ok.", max_tokens 10) →
   HTTP 200 and normal text back.
3. From the executor side, send one minimal request through the
   gateway to confirm the link works (confirm only, no real task, do
   not switch the main model).

## 10. Receipt (reply in this format, fill in every item)

```
Gateway version:
Mesh network status:
Gateway reachability: HTTP code / models count
Local gateway: listening on 127.0.0.1:3425 OK / NOT OK
Upstream providers: gateway-provider added/not added (reason); second-provider added/not added (reason)
Installed plugins: free-model plugin installed/not installed (reason); executor wiring confirmed
Models count:
Smoke test result: model HTTP=xxx first 20 chars of reply
Executor wiring: connected (main model NOT switched) / not connected (reason)
Unfinished items:
```

## 11. Rollback

- In the gateway app, delete the `gateway-provider` and
  `second-provider` providers; uninstall the free-model plugin.
- Restore configuration from the backup (copy the `.bak-v4` backup
  back; restore all executor configuration changes from backup).
- Stop the gateway: close the app or kill the process. Uninstall:
  delete the app + the gateway data directory (list it first to
  confirm).
- The host side is untouched (gateway, forwarding, and keys stay as
  they are).
