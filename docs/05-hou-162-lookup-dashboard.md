# HOU-162: lookup dashboard — public vehicle checks (e-Challan, insurance, PUC)

## Scope correction against the issue's own framing

HOU-162 describes two independent pieces: an "e-Challan/PUC public-check
path" buildable now, and an "RC-lookup call" to be stubbed behind a flag
until Rene provides a Surepass key. In practice this split does not exist.

HOU-153 (sibling issue, in_review, closed informational) already researched
exactly this question and found: **no lawful no-login public source exists
for e-Challan or PUC lookups, full stop** — not "exists but needs a flag",
not "exists in degraded form". Both `echallan.parivahan.gov.in` and
`puc.parivahan.gov.in` require solving a CAPTCHA to submit the query
itself; the CAPTCHA guards the lookup, not an optional anti-bot layer on
top of a free one. HOU-147's legal assessment (carried forward by HOU-153)
treats automating that CAPTCHA as an IT Act S43/S66 unauthorised-access
risk — a fixed legal red line, not an engineering trade-off this issue can
make differently. See `docs/04-hou-153-echallan-insurance-decision.md` for
the full source-by-source table.

So all three fields this issue asks for — e-Challan status, PUC validity,
and RC basic fields — wait on exactly the same prerequisite: Rene
completing Surepass's one-time business KYC and an API key existing. There
is no portion of this dashboard that can return live data today without
either (a) automating a CAPTCHA, which is out of scope by this issue's own
instruction, or (b) a paid licensed-reseller key that does not exist yet.

## What was built instead

`tool/lookup_dashboard.py` — a CLI (`python3 tool/lookup_dashboard.py
<plate>`) that validates/normalises an Indian plate number and runs three
checks (e-Challan, PUC, RC), each returning a clear, honest status instead
of a fabricated result:

- No `SUREPASS_API_KEY` set → `not_configured`, with a reason naming the
  HOU-153 finding and the dependency on Rene's KYC.
- `SUREPASS_API_KEY` set → `stub_not_implemented` for all three fields —
  the call sites exist (`check_echallan`, `check_puc`, `check_rc` in
  `tool/lookup_dashboard.py`) and are ready to wire to Surepass's real
  Challan / PUC-by-vehicle-number / RC Verification endpoints the moment a
  key exists and the live endpoint paths + response field names are
  confirmed on Surepass's own dashboard (HOU-147 marked exact pricing and
  field lists as unverified — see `docs/03-no-login-data-sources.md`
  section 7).
- RC's owner name is only ever returned masked to initials
  (`mask_owner_name`, e.g. `R*** G***`) — never the full registered name,
  per this issue's own scope ("masked owner name only, no full identity
  lookup"). This masking is unconditional and applies even once the real
  Surepass call is wired in; it is not itself part of the stub.

No scraping, no CAPTCHA automation, no OTP/login flow anywhere in this
tool. 15 unit tests cover plate normalisation/validation, name masking,
both the no-key and with-key code paths for all three checks, and the CLI
itself (`python3 -m unittest tool/test_lookup_dashboard.py -v`).

## Why no live code lands against a government portal

Per HOU-147 §2.1 (restated in HOU-153): the e-Challan and PUC portals use
a CAPTCHA as their own access-control mechanism specifically to prevent
unattended automated queries. Treat this as a fixed legal boundary, not
a technical obstacle to route around — consistent with HOU-162's own
instruction to treat CAPTCHA-solving as out of scope.

## What's left for the next picked-up task

1. **Rene**: complete Surepass business KYC/sign-up (surepass.io dashboard)
   and provide the API key as a Paperclip secret / env var
   `SUREPASS_API_KEY`.
2. **Root** (follow-on, once a key exists): confirm the live endpoint
   paths, auth header shape, and exact response field names for Surepass's
   Challan, PUC-by-vehicle-number, and RC Verification products on their
   own dashboard docs (do not trust third-party summaries); implement
   `check_echallan` / `check_puc` / `check_rc` against the real API; keep
   the unconditional owner-name masking; re-run the test suite with a
   mocked HTTP layer before calling it done.
3. Optional, not part of this issue: wrap `run_checks()` in a tiny local
   web form (the function boundary is already there — a form just needs to
   call `run_checks(plate, api_key)` and render `format_text`/the dict).
