#!/usr/bin/env python3
"""Incident-pack CLI (Northern Lights, HOU-152).

Takes a plate number, free-text notes and photo attachments and assembles them into a
single PDF incident pack, following templates/incident-pack-template.md.

Scope (see tool/README.md for the full statement):
  - No network calls. No lookups, no Vahan/Parivahan/RC-verification API calls, no
    login, no OTP/CAPTCHA automation of any kind. This tool only formats what you give
    it.
  - Output is a local PDF file. Nothing is sent anywhere by this tool.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plate", help="Vehicle registration number, as seen")
    p.add_argument("--date", default="", help="Date of incident (free text)")
    p.add_argument("--time", default="", help="Time of incident (free text)")
    p.add_argument("--location", default="", help="Where it happened (free text)")
    p.add_argument("--notes", default="", help="Free-text narrative")
    p.add_argument("--notes-file", help="Path to a text file with the narrative (overrides --notes)")
    p.add_argument("--photo", action="append", default=[], dest="photos",
                    help="Path to a photo to embed; repeatable")
    p.add_argument("--photo-caption", action="append", default=[], dest="captions",
                    help="Caption for the matching --photo, by position; repeatable, optional")
    p.add_argument("--out", help="Output PDF path")
    p.add_argument("--json", help="Path to a JSON file with plate/date/time/location/notes/photos "
                                   "(fields from flags override JSON fields when both given)")
    p.add_argument("--reporting-person", default="", help="Name of the person reporting (optional)")
    args = p.parse_args(argv)

    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
        for field in ("plate", "date", "time", "location", "notes", "reporting_person"):
            flag_name = field if field != "reporting_person" else "reporting_person"
            attr = "reporting_person" if field == "reporting_person" else field
            if not getattr(args, attr, None) and data.get(field):
                setattr(args, attr, data[field])
        if not args.photos and data.get("photos"):
            args.photos = data["photos"]
        if not args.captions and data.get("photo_captions"):
            args.captions = data["photo_captions"]

    if args.notes_file:
        with open(args.notes_file, "r", encoding="utf-8") as f:
            args.notes = f.read()

    if not args.plate:
        p.error("--plate is required (directly or via --json)")
    if not args.notes:
        p.error("--notes or --notes-file is required (directly or via --json)")

    return args


def wrap_text(text: str, max_chars: int):
    """Simple word-wrap for canvas.drawString (reportlab has no built-in paragraph flow here)."""
    lines = []
    for raw_line in text.splitlines() or [""]:
        if not raw_line.strip():
            lines.append("")
            continue
        words = raw_line.split()
        current = ""
        for w in words:
            candidate = (current + " " + w).strip()
            if len(candidate) > max_chars:
                if current:
                    lines.append(current)
                current = w
            else:
                current = candidate
        if current:
            lines.append(current)
    return lines


def draw_header(c: canvas.Canvas, title: str):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, PAGE_H - MARGIN, "Incident Pack")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.grey)
    c.drawString(MARGIN, PAGE_H - MARGIN - 14, title)
    c.setFillColor(colors.black)
    c.line(MARGIN, PAGE_H - MARGIN - 20, PAGE_W - MARGIN, PAGE_H - MARGIN - 20)


def draw_footer(c: canvas.Canvas, page_num: int, total_pages: int):
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    c.drawString(MARGIN, 12 * mm, f"Generated {generated} · Northern Lights incident-pack CLI · local artifact, not sent anywhere")
    c.drawRightString(PAGE_W - MARGIN, 12 * mm, f"Page {page_num} of {total_pages}")
    c.setFillColor(colors.black)


def build_cover_page(c: canvas.Canvas, args, page_num, total_pages):
    draw_header(c, "Cover")
    y = PAGE_H - MARGIN - 45

    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Plate number:")
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 95, y, args.plate)
    y -= 18

    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Date / time:")
    c.setFont("Helvetica", 12)
    dt_str = " ".join(x for x in [args.date, args.time] if x) or "[not provided]"
    c.drawString(MARGIN + 95, y, dt_str)
    y -= 18

    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Location:")
    c.setFont("Helvetica", 12)
    for line in wrap_text(args.location or "[not provided]", 70):
        c.drawString(MARGIN + 95, y, line)
        y -= 14
    y -= 10

    # Structured summary table
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN, y, "Structured summary")
    y -= 18
    rows = [
        ("Reporting person", args.reporting_person or "[PLACEHOLDER]"),
        ("Vehicle plate", args.plate),
        ("Date / time", dt_str),
        ("Location", args.location or "[PLACEHOLDER]"),
        ("Number of people involved", "[PLACEHOLDER]"),
        ("Nature of incident", "[PLACEHOLDER]"),
        ("Directed at reporting person?", "[PLACEHOLDER]"),
        ("CCTV / footage available?", "[PLACEHOLDER]"),
        ("Police contacted at the time?", "[PLACEHOLDER]"),
    ]
    c.setFont("Helvetica", 10)
    row_h = 16
    col1_w = 70 * mm
    for label, value in rows:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN, y, label)
        c.setFont("Helvetica", 10)
        for i, line in enumerate(wrap_text(str(value), 48)):
            c.drawString(MARGIN + col1_w, y - i * 12, line)
        y -= max(row_h, 12 * len(wrap_text(str(value), 48)))
        if y < MARGIN + 30:
            break

    draw_footer(c, page_num, total_pages)


def build_notes_pages(c: canvas.Canvas, notes: str, start_page, total_pages):
    lines = []
    for block in notes.splitlines() or [""]:
        lines.extend(wrap_text(block, 95) or [""])

    page_num = start_page
    lines_per_page_first = 40
    idx = 0
    first = True
    while idx < len(lines) or first:
        draw_header(c, "Notes")
        y = PAGE_H - MARGIN - 45
        c.setFont("Helvetica", 10)
        count = 0
        max_lines = lines_per_page_first
        while idx < len(lines) and count < max_lines:
            c.drawString(MARGIN, y, lines[idx])
            y -= 13
            idx += 1
            count += 1
        draw_footer(c, page_num, total_pages)
        first = False
        if idx < len(lines):
            c.showPage()
            page_num += 1
        else:
            break
    return page_num


def build_photo_page(c: canvas.Canvas, photo_path: str, caption: str, page_num, total_pages, photo_index):
    draw_header(c, f"Photo {photo_index}")
    y_top = PAGE_H - MARGIN - 45
    max_w = PAGE_W - 2 * MARGIN
    max_h = y_top - MARGIN - 30

    try:
        img = ImageReader(photo_path)
        iw, ih = img.getSize()
        scale = min(max_w / iw, max_h / ih)
        draw_w, draw_h = iw * scale, ih * scale
        x = MARGIN + (max_w - draw_w) / 2
        y = y_top - draw_h
        c.drawImage(img, x, y, width=draw_w, height=draw_h, preserveAspectRatio=True, mask="auto")
        caption_y = y - 18
    except Exception as e:  # noqa: BLE001 - we want the pack to still render with an error note
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(colors.red)
        c.drawString(MARGIN, y_top - 20, f"[Could not embed image: {os.path.basename(photo_path)} — {e}]")
        c.setFillColor(colors.black)
        caption_y = y_top - 40

    c.setFont("Helvetica-Bold", 10)
    label = f"Photo {photo_index} — {caption}" if caption else f"Photo {photo_index}"
    c.drawString(MARGIN, caption_y, label)

    draw_footer(c, page_num, total_pages)


def main(argv=None):
    args = parse_args(argv)

    if args.out:
        out_path = Path(args.out)
    else:
        safe_plate = "".join(ch for ch in args.plate if ch.isalnum()) or "plate"
        ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = Path(__file__).resolve().parent.parent / "output" / f"incident-pack-{safe_plate}-{ts}.pdf"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # total_pages is computed after the fact for reportlab (footer needs it), so do a
    # first pass to count notes pages, then render for real.
    dummy_buf_pages = 1  # cover
    lines = []
    for block in (args.notes or "").splitlines() or [""]:
        lines.extend(wrap_text(block, 95) or [""])
    notes_pages = max(1, -(-len(lines) // 40))
    total_pages = 1 + notes_pages + len(args.photos)

    c = canvas.Canvas(str(out_path), pagesize=A4)

    build_cover_page(c, args, 1, total_pages)
    c.showPage()

    build_notes_pages(c, args.notes, 2, total_pages)
    c.showPage()

    page_num = 2 + notes_pages
    for i, photo in enumerate(args.photos, start=1):
        caption = args.captions[i - 1] if i - 1 < len(args.captions) else ""
        build_photo_page(c, photo, caption, page_num, total_pages, i)
        if i < len(args.photos):
            c.showPage()
        page_num += 1

    c.save()

    print(f"Incident pack written to: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
