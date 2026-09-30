# HOU-153: e-challan/insurance public checks — decision

Optional add-on to the incident-pack CLI/n8n form (HOU-152/HOU-151): wire in a **no-login-only
public check** for e-challan history and insurance/PUC status, so the pack could show current
status for the plate. This document records why nothing was wired in, per the issue's own
instruction ("If no qualifying no-login public source exists, say so explicitly and close as
informational rather than building a stub").

## Finding: no qualifying no-login public source exists today

Re-checked against HOU-147's own research (`docs/03-no-login-data-sources.md`, §2, §2.1, §5) and
this issue's scope (**strictly no automated OTP or login flows**, and — by extension of §2.1 —
no automated CAPTCHA-solving, which HOU-147 already treats as a legal red line, not an
engineering choice):

| Candidate source | Status | Why it does not qualify |
| --- | --- | --- |
| e-Challan public lookup (`echallan.parivahan.gov.in`) | Public page | **CAPTCHA-gated.** Automating a CAPTCHA solve is unauthorised-access risk under IT Act §43/§66, per HOU-147 §2.1 — a fixed legal red line, not something this issue can build around. |
| PUC status (`puc.parivahan.gov.in` / state portals) | Public page | Same CAPTCHA gate as e-challan. |
| Parivahan "Know Your Vehicle Details" | — | Confirmed login-gated (mobile OTP). Explicitly out of scope by this issue's own instruction. |
| Vahan open data / MoRTH data portal | Fully public, no login | Aggregate statistics only — no per-plate lookup. Not usable for a single vehicle. |
| CCTNS vehicle-matching/NOC search (`eseva.csccloud.in/cctns`) | Looks public, no login found | **Unverified.** HOU-147 flagged this as a promising lead needing a live functional spike (does it actually return data without login, what are its rate limits/ToS) before anything relies on it. It is not a confirmed qualifying source; treating it as one without that verification would be building on an unproven claim, which is worse than building a stub. |
| Insurance status via IIB/IRDAI | — | IIB's own published scope is "works only with IRDAI, Insurers & Government Agencies" — no private-citizen path at all, no-login or otherwise. |
| Licensed reseller (Surepass, recommended in HOU-147) | Requires paid KYC sign-up | Not a public source — it is a metered commercial API gated behind a one-time business KYC that **René has not yet completed** (HOU-147 explicitly scoped the KYC and pipeline wiring as separate follow-on work, not part of that issue or this one). It does not use OTP/login at query time, but it is not "publicly queryable" either — it requires an account and a paid key that do not exist yet. Wiring against it now would mean either faking the response or blocking on a credential this issue does not have. |

Net: every source that is genuinely public and no-login (Vahan open data, the un-gated look of
CCTNS) either returns no per-plate data or is unverified; every source that returns real
per-plate e-challan/insurance/PUC data is gated by a mechanism this issue must not automate
(CAPTCHA, OTP/login) or by a KYC'd paid account that does not exist yet.

## Decision

**No code or n8n wiring added.** The incident-pack CLI (HOU-152) and n8n form draft
(`tool/n8n-form-workflow.json`) are left exactly as delivered — local-only, no network calls,
per `tool/README.md`'s own scope statement. Building a stub against CCTNS (unverified) or a
placeholder for Surepass (no key) would produce a feature that looks wired but either returns
unverified data or silently does nothing — worse than not building it, per this issue's own
instruction.

## What would change this

1. **CCTNS spike** (already named as HOU-147's own open follow-up #1): a small, separate,
   read-only functional test against `eseva.csccloud.in/cctns` with a non-personal test plate,
   confirming it genuinely needs no login and checking its rate limits/terms. If confirmed, it
   would be the one candidate worth wiring into the CLI/n8n form as an optional check — that is
   new scoped work, not part of this issue.
2. **Surepass KYC** (HOU-147's own next-step, owned by René): once René completes the one-time
   business sign-up and an API key exists, RC/PUC/challan lookup becomes available unattended —
   but that is a licensed paid API, not a "public" no-login source, and wiring it in is separate
   follow-on work for Root once the key exists.

Neither of these is "strictly no automated OTP or login flows" work this issue can absorb
silently; both are named here as explicit next steps for whoever picks them up next, not folded
into this issue's close.
