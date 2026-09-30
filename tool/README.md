# Incident-pack CLI

Takes a plate number, free-text notes, and photo attachments and assembles them into a
single PDF incident pack, using the fields and structure of the repo's incident-pack
template (`templates/incident-pack-template.md`, see HOU-151).

## Scope and boundaries (read before using)

- **No automated lookups of any kind.** This tool does not call Vahan, Parivahan, any
  RC-verification reseller, e-challan, PUC, or any other API. HOU-147's research
  identified *lawful* no-login sources for a future phase, but wiring one in requires
  René's own one-time KYC sign-up and an explicit follow-up task — this CLI intentionally
  stays offline/local-only until that is approved.
- **No login-gated scraping, no OTP automation.** There is nothing in this tool that
  logs in anywhere or solves a CAPTCHA.
- **Output is local only.** The PDF is written to `output/` in this repo checkout (or a
  path you pass with `--out`). Nothing is emailed, uploaded, posted to WhatsApp, or sent
  to the police or any third party. Filing a complaint is always a deliberate, separate
  human action.
- **Personal incident data does not belong in the public repo.** Use `output/` (already
  gitignored) for real incidents, or point `--out` at a path outside this checkout
  entirely (e.g. the private `houseof3d.store` repo's `docs/northern-lights/private/`).
  Only synthetic/sample packs should ever be committed here.

## Install

```bash
cd tool
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### CLI (interactive-free, scriptable)

```bash
python3 incident_pack.py \
  --plate "MH04FF4050" \
  --date "2026-09-27" \
  --time "01:40" \
  --location "Outside residence, Nashik (Thane-registered vehicle)" \
  --notes "Free text: what happened, in your own words. Multiple lines are fine." \
  --photo photo1.jpg --photo photo2.jpg \
  --out ../output/incident-pack-sample.pdf
```

Flags:

- `--plate` (required) — vehicle registration number, as seen.
- `--date`, `--time` — when it happened (any text; not parsed/validated against an
  external source).
- `--location` — free text description of where.
- `--notes` (required) — free-text narrative. Read from `--notes-file` instead if long.
- `--notes-file` — path to a text file with the narrative (overrides `--notes` if both given).
- `--photo` — repeatable; path to a photo to embed (jpg/png/webp/heic-not-supported).
  Each photo gets its own page with a caption slot.
- `--out` — output PDF path (default `output/incident-pack-<plate>-<timestamp>.pdf`).
- `--json` — optional path to a JSON file with the same fields (`plate`, `date`, `time`,
  `location`, `notes`, `photos`: [list of paths]) as an alternative to flags, for
  n8n/form integration (see below).

### n8n form option

`n8n-form-workflow.json` is a minimal exported n8n workflow: a Form Trigger (plate,
notes, date/time, location, photo upload) that writes the submission to a JSON file and
photo files to disk, then shells out to `incident_pack.py --json ...` to produce the PDF
in the same workspace. Import it into n8n, point the "Write JSON" and "Write photos"
nodes at a local path the n8n container can reach, and adjust the `Execute Command` node
path to your checkout. It does not call any external API and does not send the result
anywhere — the produced PDF sits in the configured output folder for a human to pick up.

## Output

A single PDF: cover page (plate, date/time, location, a structured summary block) +
notes page(s) + one page per photo with a caption placeholder, mirroring
`templates/incident-pack-template.md`.
