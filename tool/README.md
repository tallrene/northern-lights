# Northern Lights tools

## `incident_pack.py` (HOU-151 / HOU-152)

Lives on branch `feat/incident-pack-cli` (PR #4, not yet merged to `main`
as of this writing, same as `templates/incident-pack-template.md` on PR #3
and the `docs/0*-...md` research notes on PR #1/#2). Takes a plate, notes,
and photos and renders a single incident-pack PDF. Zero network calls. See
that branch's own docstring and PR #4/#3 for details.

## `lookup_dashboard.py` (HOU-162)

```
python3 tool/lookup_dashboard.py MH15AB1234
python3 tool/lookup_dashboard.py MH15AB1234 --json
SUREPASS_API_KEY=... python3 tool/lookup_dashboard.py MH15AB1234
```

Enter a plate number, get back e-Challan status, PUC validity, and RC basic
fields (owner name masked to initials only, no full identity lookup).

**Current state: all three checks are stubs.** HOU-153 (sibling issue)
already established that no lawful no-login public source exists for
e-Challan or PUC -- both government portals gate the query itself behind a
CAPTCHA, and solving that programmatically is an IT Act S43/S66 risk, a
fixed legal red line per HOU-147/HOU-153. RC lookup has never had a public
source; it has always required a licensed reseller. So all three fields
wait on the same prerequisite: Rene completing Surepass KYC and providing
an API key (`SUREPASS_API_KEY` env var or `--surepass-key`). Without a key,
each check returns `not_configured` with a clear reason. With a key
present, each check returns `stub_not_implemented` -- the call sites are
there, ready to wire to Surepass's real Challan / PUC / RC endpoints once
the key exists and the live endpoint paths + response field names are
confirmed on Surepass's own dashboard (never fabricate a response).

Tests: `python3 -m unittest tool/test_lookup_dashboard.py -v`

No scraping, no CAPTCHA automation, no OTP/login flow. Owner name is never
returned in full, only initials (`R*** G***`), per this issue's scope.

See `docs/05-hou-162-lookup-dashboard.md` for the full design note and the
scope correction against HOU-162's original framing.
