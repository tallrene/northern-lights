# No-login data sources for a plate → vehicle data pipeline

Research for HOU-147. Goal: identify every **lawful** source that returns vehicle data from a
registration plate using either no authentication at all, or a machine API key (no human login,
no OTP, no CAPTCHA-solving) — so the pipeline can run unattended once René completes a one-time
KYC sign-up. This document does not sign up for anything, spend money, or bypass any CAPTCHA; it
is the research and recommendation only.

Researched 30 Sep 2026. Primary sources: MoRTH/Parivahan public pages, provider docs/marketing
pages, and legal/policy commentary (Internet Freedom Foundation, The Wire, ORF, Medianama,
Lexology). Some provider pages (pricing tiers specifically) were not directly fetchable from this
sandbox and are marked **unverified — confirm at sign-up** below; nothing here should be treated
as a quoted price until checked on the provider's own dashboard.

## TL;DR recommendation

Build the pipeline on **one licensed RC-verification reseller API** for the core RC/owner/insurer
lookup (no-login, API-key, unattended after KYC), plus **two genuinely public no-login checks**
that need no sign-up at all (e-challan status, PUC status). Do **not** build on Parivahan's "Know
Your Vehicle Details" (it is login-gated) and do not add a CAPTCHA-solving step anywhere — treat
that as a legal red line, not an engineering problem (see §2.1).

Recommended provider to KYC with first: **Surepass** (see §4 ranking) — best combination of
no-login API access, clear per-call pricing model, and broad field coverage (RC + challan + PUC in
one vendor, reducing integration surface). Cashfree Verification Suite is the strongest backup if
Surepass's onboarding stalls, because it is already a known-KYB entity (a payments company) with
a fast business-account approval path.

## 1. Ranking criteria

Each source scored on:

- **Legality for a private citizen** — is a private individual/small business permitted to query
  this, per the source's own terms and the applicable Indian data-sharing policy?
- **No-login feasibility** — can it be called unattended with an API key / no auth at all, with
  zero CAPTCHA-solving or OTP-relay?
- **Cost** — free, or roughly what per lookup (see per-source caveats on unverified pricing).
- **Fields returned** — how much of what Northern Lights needs (owner name, address, chassis/engine
  no., RTO, insurer, PUC, challans, blacklist/NOC) does one call return?

## 2. Government sources

| Source | No-login? | What it returns | Verdict |
| --- | --- | --- | --- |
| e-Challan public lookup (`echallan.parivahan.gov.in`) | Public page, **but CAPTCHA-gated** | Pending/paid challan list for a given RC/DL/challan no. | Legal to query manually or via a licensed reseller that has solved the CAPTCHA problem on the backend under its own agreement — **not** legal/acceptable for Northern Lights to automate a CAPTCHA solve itself (§2.1). |
| PUC status (`puc.parivahan.gov.in` / state PUCC portals) | Public page, typically needs application/certificate number or RC + CAPTCHA | Pollution certificate validity + expiry | Same CAPTCHA constraint as e-challan. Several resellers (Surepass, idspay) offer a "PUC by vehicle number" API that removes the CAPTCHA step on their side under their own agreement — use via reseller, not direct automation. |
| Parivahan "Know Your Vehicle Details" (`vahan.parivahan.gov.in/nrservices`) | **No** — confirmed login-gated | Full RC detail after citizen login (mobile OTP) or account creation | Out of scope for an unattended pipeline. Do not build against this; it requires a human's OTP every time. |
| Vahan open data / MoRTH data portal (`data.gov.in` / Vahan dashboards) | Yes, fully public, no login | **Aggregate statistics only** (registrations by state/RTO/fuel/category) — no per-plate owner lookup | Not usable for single-vehicle lookups; useful only for RTO/series decoding reference tables (see README goal 1). |
| NHAI/IHMCL FASTag/NETC endpoints | No public per-vehicle API found. IHMCL's NETC Interface Control Document describes acquirer-bank-to-NPCI integration only, gated by program membership, not open to the public | N/A | Not usable. No further action. |
| CCTNS vehicle-matching / NOC search (`eseva.csccloud.in/cctns`) | **Yes — public, no login found**, registration/chassis/engine number search | Confirms whether a vehicle is flagged in CCTNS (stolen/blacklisted/NOC records) | Promising lead for the "blacklist/NOC status" requirement — needs a live test against a non-personal plate before relying on it (its access model and rate limits were not independently confirmed this pass; flag for a follow-up spike). |

### 2.1 CAPTCHA assessment (explicit, per the task's instruction to assess legality)

The e-challan and PUC portals put a CAPTCHA in front of the query specifically to stop automated,
unattended bulk queries — this is the site's own access-control mechanism, not an accidental
obstacle. The IT Act 2000 §43/§66 (unauthorised access / computer-related offences) and most
government portals' own terms of use treat deliberate circumvention of an access control as
unauthorised access, independent of whether the underlying data itself is public. Solving the
CAPTCHA programmatically (OCR, a solving service, or a headless browser scripted around it) is a
circumvention of that control, so Northern Lights should **not** build a CAPTCHA-solving step, full
stop — this is a legal-risk red line, not a "can we make it work" engineering question, consistent
with the issue's explicit instruction ("assess whether... acceptable/legal" and "No... captcha
bypass in this issue"). The lawful path to the same data is a **licensed reseller** who has a
separate commercial/technical arrangement with the government system (several of the API vendors
below explicitly advertise "Challan" and "PUC" lookups as part of their product, meaning they have
solved this access problem under their own agreement, not by scripting around the citizen-facing
CAPTCHA).

## 3. MoRTH Bulk Data Sharing Policy — what's actually still lawful

- **March 2019**: MoRTH published a Bulk (Vehicle/Driver) Data Sharing Policy that allowed
  bulk licensing of Vahan/Sarathi data to private companies for a fee, via a formal application
  and licence agreement.
- **June 2020**: MoRTH's Apex Committee scrapped the 2019 bulk policy after public backlash over a
  bulk sale to an overseas analytics firm (reported by outlets including The Wire and covered by
  Internet Freedom Foundation) — bulk commercial reselling of the full database is no longer
  authorised under that mechanism.
- **2025 successor policy** (MoRTH's new National Transport Repository data-sharing framework,
  covered by Medianama and Lexology Aug–Sept 2025): replaces outright bulk sale with **controlled,
  parameter-level access** — third parties can be authorised for **per-vehicle RC/DL verification**
  (exactly the "is this RC real, who is it registered to at a masked/limited level" use case) under
  DPDP Act 2023 consent obligations, rather than buying the whole database. This is the legal basis
  the RC-verification resellers below actually operate under today — not the scrapped 2019 bulk
  deal.
- **Practical takeaway for Northern Lights**: a licensed reseller with an active agreement under
  the current (2025) controlled-access framework is the lawful route to per-plate RC data. Directly
  scraping Vahan, buying an old "full database" dump, or reviving anything modelled on the 2019
  bulk-sale approach is not — and several such offers exist informally online; avoid them.
- DPDP Act 2023 also matters independently of the MoRTH policy: any provider handling vehicle
  owner personal data (name, address) must have a lawful basis to process/disclose it. Legitimate
  resellers publish a consent/purpose framework (e.g. "verification purpose" disclosures) —
  treat a provider that doesn't as a red flag.

## 4. Licensed RC-verification reseller APIs

All of these query Vahan data under a backend agreement (the 2025 controlled-access framework,
§3) and expose it as a metered REST API with an API key — i.e. exactly the no-login, unattended
shape Northern Lights needs. Fields and pricing below are what the vendor's own marketing/docs
pages state; **treat exact price-per-call and full field lists as unverified until confirmed on
the vendor's live dashboard at sign-up**, since list pricing on these sites changes often and
several require a sales conversation for the real rate.

| Provider | Product | Fields advertised | KYC to sign up | Price per lookup | Private individual? |
| --- | --- | --- | --- | --- | --- |
| **Surepass** | Vehicle RC Verification API, RC-with-Financer-Details, Mobile↔RC linking, PUC-by-vehicle-number, Challan API (separate products) | Owner name (as held in RC — typically the registered name, not separately masked per vendor docs), registration date, RTO, chassis/engine no., vehicle class, fuel type, insurer + policy validity, PUC validity, fitness/tax validity, financer (if hypothecated) | Business sign-up flow (email verification, dashboard-based); GST/PAN requirement not confirmed as mandatory for the lowest tier — **confirm at sign-up** | Tiered "price per transaction" plans (seen referenced as a formal proposal document, not a public price list) — **unverified, get quote at sign-up** | Signup appears self-serve for a business account; a sole proprietor / individual-with-GST setup is the likely path for René — **confirm** |
| **Cashfree (Secure ID / Verification Suite)** | Vehicle RC Verification API (part of its KYC/Secure ID stack, alongside PAN/Bank/GSTIN) | Registration/ownership, chassis, insurance detail (per product page) | Cashfree is primarily a payments company; verification-suite account creation is self-serve on their dashboard, separate from a full payment-gateway KYB | Dashboard credits model ("use credits to do free verifications via dashboard or API"); exact per-call RC price not listed publicly — **confirm at sign-up** | Yes — Cashfree explicitly states a Verification Suite account can be created independently of the payment gateway, which is normally the harder KYB path |
| **Attestr** | Vehicle RC Check API | RC status + owner/registration detail (doc page confirms the API exists and is documented) | Self-signup flow described in their own docs ("Create Free Business Account" — email OTP, then app registration/whitelisting for API access) | Credit-purchase model ("Purchase Credits" doc page) — **unverified rate** | Free-tier self-signup exists per their own docs; likely usable by an individual/small business |
| **Signzy** | Vehicle RC check (bundled under their "India Stack"/KYB verification suite, not a standalone dedicated product page) | Not independently confirmed this pass — bundled with other KYB products | Enterprise-oriented sales-assisted onboarding (typical for Signzy's positioning toward banks/NBFCs) | Not published — sales quote only | Likely enterprise-oriented; less suited to a solo sign-up than Surepass/Cashfree/Attestr |
| **IDfy** | Registration Certificate Verification (listed on their RapidAPI marketplace page as well as their own API suite docs) | Not independently confirmed this pass | RapidAPI marketplace listing suggests a lower-friction sign-up path (RapidAPI account) alongside their enterprise direct API; worth checking the RapidAPI route specifically for a no-KYC-call path | RapidAPI listings are typically metered/subscription, pricing visible on the RapidAPI page — **check the RapidAPI listing directly, not just idfy.com** | RapidAPI route plausibly the easiest solo-developer path of this group — flag as worth a closer look |
| **Invincible Ocean** | Vehicle Registration RC Check API — markets "40+ data points" (per their LinkedIn copy) | Broadest field claim seen this pass (40+ data points: make/model/variant, registration trends, RTO/regional data) but the detailed field list wasn't independently confirmed from their own docs this pass | Enterprise dashboard (`dashboard.invincibleocean.com`), client logos suggest mid/large-enterprise focus | Not published | Unconfirmed — dashboard exists but individual-tier sign-up not verified |

Ranking of the five (best → least fit for a solo/small-business, no-login, unattended use case,
given what's confirmed):

1. **Surepass** — broadest confirmed field set across RC + PUC + Challan in one vendor (reduces
   integration surface to one key), clear self-serve dashboard signup.
2. **Cashfree** — fast KYB path because it's a payments company already built for self-serve
   business onboarding; credits model is simple to reason about; RC is one of several products so
   less of a vehicle-data specialist.
3. **Attestr** — confirmed free self-signup flow in its own docs, good for a low-commitment first
   test once René is ready to KYC, but credit pricing and full field breadth unverified.
4. **IDfy (via RapidAPI)** — worth a closer look specifically through the RapidAPI marketplace
   listing (lower friction than their enterprise doc suite implies), but unverified this pass.
5. **Signzy / Invincible Ocean** — both read as enterprise/sales-assisted onboarding; lowest
   priority for a solo sign-up unless the others fall through.

## 5. Insurance status, accident history, blacklist/NOC

- **IIB (Insurance Information Bureau) / IRDAI direct access**: `iib.gov.in`'s own SUDARSHANA page
  states explicitly **"IIB works only with IRDAI, Insurers & Government Agencies"** — there is no
  public or private-citizen API path into IIB directly. Not usable for Northern Lights under any
  sign-up.
- **Insurance status in practice**: comes bundled as a field inside the RC-verification resellers'
  response (Surepass and others return current insurer name + policy validity as part of the RC
  check) — this is the realistic path, not a direct IIB integration.
- **Accident history**: no public or licensed-reseller API was found that exposes vehicle-level
  accident history to a private party. IIB holds this data but restricts it to insurers/regulators
  (see above). Treat as **not obtainable** through any lawful no-login channel for a private
  citizen; do not pursue.
- **Blacklist / NOC status**: the CCTNS vehicle-matching/NOC search (`eseva.csccloud.in/cctns`,
  §2 table) is the one public-looking lead found this pass. It needs a live functional check
  (does it actually return data without login for a test plate, what's its rate limit / ToS) before
  the pipeline can rely on it — flagged as a follow-up spike, not yet confirmed.

## 6. What this means for the pipeline design

- **No CAPTCHA-solving, ever** — treat this as fixed per §2.1, independent of any future
  engineering convenience.
- **No automation of Parivahan's OTP-gated "Know Your Vehicle"** — confirmed login-gated, out of
  scope for unattended use.
- **One RC-verification reseller carries the core lookup** (owner name as registered, RTO,
  chassis/engine, insurer, PUC/fitness/tax validity) via a plain API key once René completes a
  one-time KYC. This is the only unattended, lawful path to owner-linked detail.
- **Accident history is not obtainable** lawfully by a private citizen through any channel found —
  design the incident pack to note this as a known gap the police can fill, not something the
  pipeline should promise.
- **Blacklist/NOC via CCTNS** is a promising but unverified lead — needs a small functional spike
  before being wired into the pipeline.

## 7. Open follow-ups (not part of this issue's scope)

1. Live functional test of `eseva.csccloud.in/cctns` vehicle-matching search against a
   non-personal test plate, to confirm no-login access actually works and check its terms/rate
   limits.
2. Confirm IDfy's RapidAPI listing terms (price, individual sign-up) directly, since its own docs
   site reads enterprise-oriented but the RapidAPI route may be materially easier.
3. At KYC time, get the real per-call price and exact field list from whichever provider René
   picks — the table above states what's published, not a confirmed quote.

## Recommendation for René (decision needed)

René should pick **one** provider to complete the one-time KYC sign-up with; after that, the API
key runs unattended with no further human action:

- **Option A — Surepass (recommended)**: broadest field coverage in one vendor (RC + PUC + Challan),
  clear self-serve business dashboard signup. Best fit if he wants the fewest vendors to manage.
- **Option B — Cashfree Verification Suite**: fastest KYB path since Cashfree already does
  self-serve payments onboarding; simple credits pricing; RC is one product among several so
  slightly less vehicle-data depth than Surepass.
- **Option C — Attestr**: lowest-commitment first test — has a documented free self-signup flow —
  good if René wants to try one provider cheaply before committing, at the cost of unverified
  pricing/field depth.

No payment or signup has been started; this issue is research-only per its own scope.
