# Northern Lights

From "I have a number plate" to "the police have a complete, actionable complaint" — fast,
hands-free, and lawful.

Started 27 September 2026 after a quarrel outside the author's home in Nashik, India: a few men,
shouting, a vehicle with a visible plate, and a police line that was busy. This project asks:
what can a citizen legitimately find out, what can the police find out that a citizen cannot, and
how do you hand them a complaint they can act on — without spending the night on portals.

Developed in the open. Personal incident files (complaints, footage, addresses) are **never** in
this repo; only the method, the tooling and the research are.

## Goals

1. **Zero-login pipeline** — given a plate and a few notes, assemble everything obtainable without
   a human logging in: RTO/series decoding, e-challan history (public), insurance/PUC status via
   licensed RC-verification APIs where lawful, and a formatted incident pack.
2. **Complaint generator** — English + Marathi drafts for the Maharashtra Police Citizen Portal,
   e-FIR (where eligible), and the Nashik Police WhatsApp line, with the right BNS sections.
3. **Know what the state can do** — document how Indian police actually locate a vehicle
   (ANPR/CCTV networks, FASTag logs, CCTNS, Dial-112 ERSS, Vahan) so a caller can ask for the
   right thing in the first minute.

## Boundaries

- Official or licensed sources only. No leaked databases, no grey-market lookup sites.
- No automation of OTP / Aadhaar / login flows on anyone's behalf.
- Nothing is sent to the police or any third party without a human click.
- Owner identity beyond what an official service shows a citizen is the police's to obtain, not ours.

## Layout

```
docs/       research and playbooks (published as they are reviewed)
tool/       the incident-pack CLI / service (coming)
templates/  complaint and evidence-pack templates (EN + MR)
```

## Status

Discovery in progress. Track: Paperclip project "Northern Lights" (private board).

## Licence

MIT — see LICENSE.
