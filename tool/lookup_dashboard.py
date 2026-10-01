#!/usr/bin/env python3
"""Northern Lights lookup dashboard (HOU-162).

CLI tool: enter a vehicle plate number, get back e-Challan status, PUC
validity, and (once a Surepass API key exists) basic RC fields with the
owner name masked to initials only.

IMPORTANT -- read docs/04-hou-153-echallan-insurance-decision.md and
docs/05-hou-162-lookup-dashboard.md before changing this file.

HOU-153 (sibling issue, in_review) already researched e-Challan and PUC
public lookups and found NO lawful no-login source exists for either: both
government portals require solving a CAPTCHA to submit the query itself --
not an extra anti-bot step layered on top of a free lookup, but a gate on
the lookup itself -- and HOU-147's legal assessment treats automating that
CAPTCHA as an IT Act S43/S66 unauthorised-access risk: a fixed legal red
line, not an engineering problem to solve around.

So, unlike HOU-162's own framing (which describes e-Challan/PUC as a
separately-buildable "public-check path" distinct from the Surepass-gated
RC lookup), there is in practice no live check available for ANY of the
three fields -- e-Challan, PUC, or RC -- until Rene completes Surepass KYC
and an API key exists. All three are therefore implemented as stubs gated
behind the same SUREPASS_API_KEY env var / --surepass-key flag, with call
sites ready to wire to Surepass's real Challan/PUC/RC endpoints the moment
a key exists and the exact endpoint paths + response field names are
confirmed from Surepass's own live dashboard docs (not independently
verified yet -- see docs/03-no-login-data-sources.md section 7).

No scraping, no CAPTCHA automation, and no login/OTP flow is implemented
here, per HOU-147 / HOU-153 / HOU-162's own scope.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Optional

# Loose Indian plate shape check (e.g. MH15AB1234, DL3CAB1234, MH-15-AB-1234).
# Not authoritative RTO validation -- just enough to catch obvious typos
# before spending an API call.
_PLATE_RE = re.compile(r"^[A-Z]{2}[0-9]{1,2}[A-Z]{0,3}[0-9]{3,4}$")


def normalise_plate(raw: str) -> str:
    """Upper-case and strip spaces/hyphens so 'mh 15 ab 1234' == 'MH15AB1234'."""
    return raw.strip().upper().replace(" ", "").replace("-", "")


def validate_plate(plate: str) -> bool:
    return bool(_PLATE_RE.match(plate))


def mask_owner_name(name: str) -> str:
    """Return initials only, never the full registered name.

    Per HOU-162 scope: "masked owner name only, no full identity lookup."
    """
    if not name:
        return ""
    parts = [p for p in name.strip().split() if p]
    return " ".join(f"{p[0].upper()}***" for p in parts)


def surepass_configured(api_key: Optional[str]) -> bool:
    return bool(api_key)


_NO_PUBLIC_SOURCE = (
    "No lawful no-login public source exists for {field} (see "
    "docs/04-hou-153-echallan-insurance-decision.md). Set SUREPASS_API_KEY "
    "once Rene completes Surepass KYC (HOU-147's chosen provider) to enable "
    "this check via the licensed reseller API."
)

_STUB_NOT_WIRED = (
    "SUREPASS_API_KEY is set but the Surepass {product} call is not yet "
    "wired -- confirm the live endpoint path and response field names on "
    "Surepass's own dashboard first (see docs/03-no-login-data-sources.md "
    "section 7), then implement the call here. Do not fabricate a response."
)


def check_echallan(plate: str, api_key: Optional[str]) -> dict:
    if not surepass_configured(api_key):
        return {
            "field": "echallan",
            "status": "not_configured",
            "reason": _NO_PUBLIC_SOURCE.format(field="e-Challan status"),
        }
    return {
        "field": "echallan",
        "status": "stub_not_implemented",
        "reason": _STUB_NOT_WIRED.format(product="Challan API"),
    }


def check_puc(plate: str, api_key: Optional[str]) -> dict:
    if not surepass_configured(api_key):
        return {
            "field": "puc",
            "status": "not_configured",
            "reason": _NO_PUBLIC_SOURCE.format(field="PUC validity"),
        }
    return {
        "field": "puc",
        "status": "stub_not_implemented",
        "reason": _STUB_NOT_WIRED.format(product="PUC-by-vehicle-number API"),
    }


def check_rc(plate: str, api_key: Optional[str]) -> dict:
    if not surepass_configured(api_key):
        return {
            "field": "rc",
            "status": "not_configured",
            "reason": (
                "RC lookup requires a licensed reseller (Surepass, per Rene's "
                "HOU-147 decision) -- no public no-login source exists. Set "
                "SUREPASS_API_KEY once Rene completes KYC."
            ),
            "owner_name_masked": None,
        }
    return {
        "field": "rc",
        "status": "stub_not_implemented",
        "reason": _STUB_NOT_WIRED.format(product="RC Verification API"),
        "owner_name_masked": None,
    }


def run_checks(plate: str, api_key: Optional[str]) -> dict:
    return {
        "plate": plate,
        "echallan": check_echallan(plate, api_key),
        "puc": check_puc(plate, api_key),
        "rc": check_rc(plate, api_key),
    }


def format_text(result: dict) -> str:
    lines = [f"Plate: {result['plate']}", ""]
    for field in ("echallan", "puc", "rc"):
        r = result[field]
        lines.append(f"[{field.upper()}] {r['status']}")
        lines.append(f"  {r['reason']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Northern Lights vehicle lookup dashboard (HOU-162)"
    )
    parser.add_argument("plate", help="Vehicle registration plate, e.g. MH15AB1234")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    parser.add_argument(
        "--surepass-key",
        default=None,
        help="Surepass API key override (else SUREPASS_API_KEY env var)",
    )
    args = parser.parse_args(argv)

    plate = normalise_plate(args.plate)
    if not validate_plate(plate):
        print(
            f"error: '{args.plate}' does not look like a valid Indian plate number",
            file=sys.stderr,
        )
        return 2

    api_key = args.surepass_key or os.environ.get("SUREPASS_API_KEY")
    result = run_checks(plate, api_key)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
