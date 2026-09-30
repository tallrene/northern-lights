# Incident Pack Template

Used by the `tool/incident_pack.py` CLI (HOU-152) to assemble a single PDF from a plate
number, free-text notes and photo attachments. This defines the field structure; the CLI
renders it into a PDF cover page + notes page + one page per photo.

Personal incident material filled into this template belongs in `output/` (gitignored)
or a private repo — never committed here with real data. Only the blank structure below,
and any fully synthetic sample, belong in the public repo.

---

## Cover page

- **Plate number:** [PLATE]
- **Date:** [DATE]
- **Time:** [TIME]
- **Location:** [LOCATION — free text, e.g. "outside residence, Nashik"]

### Structured summary

| Field | Value |
| --- | --- |
| Reporting person | [PLACEHOLDER — René fills before any filing] |
| Vehicle plate | [PLATE] |
| Date / time | [DATE] [TIME] |
| Location | [LOCATION] |
| Number of people involved | [PLACEHOLDER] |
| Nature of incident | [PLACEHOLDER — e.g. "verbal altercation / abusive language"] |
| Directed at reporting person? | [PLACEHOLDER — yes/no] |
| CCTV / footage available? | [PLACEHOLDER — yes/no, where] |
| Police contacted at the time? | [PLACEHOLDER — e.g. "yes, line busy" / "no"] |

## Notes

Free-text narrative, in the reporting person's own words. No speculation about who the
other party is; state only what was observed. (See HOU-143 for what a lawful complaint
needs and HOU-144 for phrasing conventions used in actual complaint drafts.)

[NOTES]

## Photo pages

One page per attached photo, each with:

- The image, fitted to the page.
- A caption line: **Photo N — [free-text caption, filled at capture time if provided]**

## Filing note (not part of the PDF)

This pack is a **local artifact only**. It is not sent anywhere automatically. Filing a
complaint (Maharashtra Police Citizen Portal, e-FIR, WhatsApp line, or in person) is a
separate, deliberate human action — see HOU-143 for the lawful routes and HOU-144 for a
worked complaint-draft example.
