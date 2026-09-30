# How the police actually locate a vehicle in India (state capability map)

Purpose: when a citizen calls with a plate and a description, what can police realistically do to find the vehicle now or trace where it last was — and what does it take to get them to do it. Worked example referenced throughout: plate `MH04FF4050` (Thane-registered), incident Nashik, 27 Sep 2026.

This is research only. No automation of OTP/Aadhaar/login flows. Official/licensed sources only.

## 1. ANPR / CCTV networks

**What it is:** Automatic Number Plate Recognition cameras feeding a city or state command-and-control centre, matched against watchlists or searched retrospectively.

- **Nashik**: Nashik Municipal Smart City Development Corporation Ltd (NMSCDCL) runs an Integrated Command and Control Centre (ICCC) with city CCTV/ANPR feeds, expanded for Kumbh Mela 2027 crowd/traffic monitoring (public RFP confirms a large CCTV/ANPR buildout). Control room access sits with the ICCC and Nashik City/Rural Police jointly; a citizen cannot query it directly.
- **State highways / NHAI toll plazas**: toll-plaza cameras capture plate images per FASTag transaction (see §2) — these are financial system logs, not a general surveillance search, but timestamped and geo-fixed to a specific plaza.
- **Maharashtra/Mumbai/Thane traffic ANPR**: used for e-challan (speeding, signal, no-helmet) and, in Mumbai, integrated into the traffic police control room; feeds are city-specific and not federated into one national real-time plate search.
- **Real-time cross-camera plate search**: exists as vendor capability (e.g. the Bengaluru ICCC case study confirms this class of system), but it is **NOT a self-service or even a standing province-wide search** — a control room operator runs it only against an active case/FIR, per that city's or state's own ANPR deployment. There is no single portal covering Nashik + Mumbai + Thane + NHAI as one system.
- **Retention**: typically 30–90 days of raw footage depending on the operator's storage policy (NMSCDCL RFP specifies retention tiers); requests older than that likely fail.

**Bottom line**: ANPR is real and growing, but it is jurisdiction-by-jurisdiction, requires a police officer to query it against a logged case, and is not something a citizen or this pipeline can query directly — so the "ask" is to get the plate entered into the local ANPR watchlist / cross-checked against recent plaza and city camera logs, fast, while footage is still retained.

## 2. FASTag / NETC toll data

**What it is:** Every toll transaction records plate (OCR + RFID tag ID), plaza, timestamp — a coarse but nationwide trail of highway movement.

- Operated by **NPCI (NETC scheme owner)**, with **IHMCL/NHAI** as the highway-toll authority and the vehicle's linked bank as tag issuer.
- MoRTH already fuses FASTag transaction data with VAHAN registration data operationally (confirmed use: automated e-Notices for toll evasion) — meaning the FASTag↔VAHAN pipe already exists administratively, it isn't hypothetical.
- **Access route for police**: a formal written requisition (station-level, typically under CrPC/BNSS production-of-document powers — see §5) sent to the vehicle's toll-tag-issuing bank or to NHAI/IHMCL/NPCI's law-enforcement liaison; it is not self-serve or instant. In practice this is used mainly in follow-up investigation ("where did this vehicle go after the incident"), not live tracking, because transaction records are polled/settled in batches, not streamed in real time to police consoles.
- **What it gives**: plaza name + GPS + timestamp for each toll crossing — useful for reconstructing a route and rough timeline, not current live location.

**Bottom line**: strong for "which highway did it take and when," weak for "where is it right now." Needs a written police requisition, not a phone call.

## 3. Vahan / Sarathi / CCTNS / ICJS — what police see for a plate

- **VAHAN** (MoRTH vehicle registry) gives registered owner name, address, engine/chassis number, registration date, fitness/insurance/PUC validity, and class of vehicle. Police access VAHAN through their own departmental login (not the public parivahan.gov.in citizen portal), typically integrated into state police systems.
- **CCTNS** (Crime and Criminal Tracking Network & Systems, run by NCRB/MHA) is the case-management backbone every police station uses to register FIRs, and cross-search prior cases/MO. It is *not* itself a vehicle registry — it's where a plate gets logged against a new or existing case so it surfaces to other stations and (via ICJS) courts/prisons/forensics.
- **ICJS** (Interoperable Criminal Justice System) links CCTNS with courts (e-Courts), prisons (e-Prisons), prosecution (ePrisecution) and forensics — relevant once a complaint becomes an FIR; it is not the fast-lookup layer.
- **e-Challan / traffic portals** (state Parivahan-linked) show pending challans and RC status but do NOT show owner PII to the public.

**What a citizen can request**: once the station logs an FIR/NC, the plate goes into CCTNS and the investigating officer pulls VAHAN owner details directly — this is routine and same-day in most stations, no court order needed for basic ownership lookup by police.

**Bottom line**: this is the fastest, most reliable step — get the incident logged as an FIR or at minimum an NC (non-cognizable) entry immediately, because VAHAN owner lookup by the IO happens the same day, no separate legal process required.

## 4. Dial-112 ERSS (Maharashtra)

- Maharashtra runs its own Dial-112 Command and Control Centre (dial112.mahapolice.gov.in) under the national ERSS-112 framework (112.gov.in / ERSS).
- Call flow: caller → state CCC call-taker → incident logged with GPS of caller's phone → dispatcher assigns nearest Emergency Response Vehicle (ERV/PCR van) → unit responds and files ground report, which can trigger an FIR.
- ERSS also supports a panic trigger (power button x3, or app) that auto-shares live GPS — relevant if René or a witness is still near the vehicle and can trigger this live, not after the fact.
- **CCC does not itself run ANPR searches** — but if the caller gives a clean plate + description + last-seen direction within the call, the CCC can radio it to patrol units and request the relevant local control room (Nashik ICCC, traffic police) to flag the plate — this is an operational ask, not a database button.

**60-second call script** (for §7): plate number spelled letter-by-digit, vehicle make/model/colour, last-seen location + direction of travel + time, description of persons (if any), and the incident location for FIR purposes. Explicitly ask the call-taker to (a) dispatch the nearest unit, (b) flag the plate to local traffic/ANPR control rooms, and (c) register it as a cognizable incident so a formal complaint number is issued.

## 5. Mobile / app tracking (CDR, tower dumps, vehicle telematics)

- **Legal basis**: Section 94 BNSS 2023 (replaces Section 91 CrPC) lets a court or a police officer in charge of a station formally require any person/entity (a telecom operator, an insurer, a manufacturer's telematics unit) to produce a document or thing relevant to an investigation — this is the standard route used to obtain Call Detail Records (CDR), IPDR (internet session data), and cell-tower dumps.
- **CDR** identifies calls/SMS to/from a number and the serving cell tower at each event — useful if the vehicle's driver/owner phone number is known.
- **Tower dumps** list every device that connected to a given tower in a time window — broader, used when the phone number is unknown but the location/time is (e.g. an incident spot); requires a formal request to the telecom operator's nodal officer, usually via the investigating officer, often with a magistrate's order for tower dumps given privacy sensitivity (case law leans that direction; practice varies by state).
- **Vehicle telematics** (OEM connected-car apps, insurer black-box devices, fleet trackers) — only relevant if the vehicle owner uses one; access still requires the same Section 94 BNSS production request to the manufacturer/insurer, and only once there's a logged case.
- This tier all requires an FIR to exist first — it is a follow-up investigative step, not a same-day tool.

## 6. What a citizen can do that materially helps

- Timestamped photo/video of the plate and vehicle, taken at the time — strongest single piece of evidence to attach to the FIR/NC.
- Note direction of travel and approximate time to the minute.
- Ask neighbours/nearby shops for their CCTV footage before it's overwritten (most private DVRs cycle in 7–30 days) — this is often faster than any state system and should be pursued in parallel, same day.
- Dashcam networks: if any nearby vehicle has a dashcam, that footage also cycles fast — ask immediately.
- File the FIR/NC in person or via the Maharashtra e-FIR facility for applicable offence categories, so the plate is in CCTNS same day (this unlocks §3's VAHAN lookup and is the prerequisite for §5).

## 7. The 60-second 112 call script

"This is [name], calling from [location]. I want to report [brief incident — e.g. a roadside quarrel/threat] that happened at [address], at approximately [time]. The vehicle involved is plate number [M-H-0-4-F-F-4-0-5-0], a [colour/make/model], last seen heading [direction] on [road] about [X] minutes ago. I have [a photo/video of the plate] I can share. Please dispatch the nearest unit, flag this plate to the local ANPR/traffic control room, and register this as a formal complaint so I get a complaint number."

Keep this short and factual — specificity (plate spelled digit-by-digit, direction, time) is what lets the CCC forward something actionable to ANPR/traffic control rather than just log a report.

## 8. Worked example: MH04FF4050, 27 Sep 2026, Nashik

- E-challan lookup showed "not found" for this plate on 27 Sep — consistent with §3: the public e-challan portal only returns *violation* records, not ownership, and a clean record there proves nothing about the vehicle's identity or reachability.
- No OTP/login flow was attempted for this plate, per project boundary (autonomy requirement) — VAHAN owner lookup can only happen through police-side access once an FIR/NC exists (§3), not through a public/citizen channel.
- Practical path for this case: file the NC/FIR in Nashik (fastest unlock for VAHAN lookup) referencing the 112 call timestamp if one was made; separately pursue nearby shop/dashcam footage (§6) in parallel since it degrades fastest.

## Sources

- NMSCDCL Nashik Kumbh 2027 CCTV RFP (ICCC/ANPR scope): https://www.scribd.com/document/937968366/Vol1
- ICCC ANPR use-case reference (Bengaluru, illustrative of control-room capability): https://iccc.niua.org/iccc/sector/use-case/815e6212def15fe76ed27cec7a393d59
- NETC/FASTag official: https://www.netc.org.in/check-fastag-status
- IHMCL NETC Procedural Guidelines: https://ihmcl.co.in/wp-content/uploads/2023/02/NETC_PG_V1.9_.pdf
- FASTag–VAHAN data fusion for e-Notices, explainer: https://internetfreedom.in/data-highways-rights-roadblocks-an-explainer-on-the-national-transport-repository/
- NHAI FASTag FAQ: https://nhai.gov.in/nhai/sites/default/files/mix_file/FAQ-FASTag.pdf
- MHA on CCTNS/ICJS: https://www.mha.gov.in/en/divisionofmha/women-safety-division/cctns
- Digital Police Portal (CCTNS/NCRB): https://digitalpolice.gov.in/
- ICJS portal: https://icjs.gov.in/ICJS/login
- Maharashtra Dial 112: http://dial112.mahapolice.gov.in/CitizenPortal-Maharashtra/dial-112
- ERSS-112 national: https://112.gov.in/faq
- Section 94 BNSS / CDR-IPDR-tower dump investigator guide: https://ministryofcyberaffairs.com/news/cdr-ipdr-and-tower-dumps-an-investigator-s-guide-to-telecom-data-requests-0c43f90e-77ee-47e5-87bf-8e6d309ebdc8
- CDR admissibility under BSA 2023 / Section 94 BNSS: https://jurigram.com/advocates/resources/new-laws/cdr-admissibility-under-bsa

## Limitations / what this doc does not cover

- No leaked/grey-market lookup services were used or should be used — all sources above are official or credentialed-investigator process descriptions.
- State-by-state ANPR coverage is uneven; Nashik's specific real-time query capability at the ICCC was inferred from the public Kumbh 2027 RFP scope, not confirmed via a direct operational source — flag as an assumption if precision matters for an actual complaint.
- This document does not itself perform any lookup, log any FIR, or contact any authority — it is reference material for the complaint-pack tooling in `tool/`.
