# Incident Pack Template

Template only — not an automation. Fill it in by hand (or paste into whatever tool assembles
the pack later) after an incident, then use the **Structured Summary** section as the starting
text for a Maharashtra Police Citizen Portal complaint, an e-FIR (where eligible), or the local
police WhatsApp line. Nothing in this file is submitted anywhere by itself.

Field set and phrasing follow `docs/01-lawful-lookup-and-complaint-routes.md` (evidence
template, complaint routes, BNS 2023 sections) and the complaint-draft conventions used for the
project's first real case (plain factual language, `[PLACEHOLDER]` for anything only the
reporting person can confirm, no speculation about who anyone is or what they intended).

No personal data lives in this file. `MH04FF4050` appears only as the project's standing worked
example (see `docs/02-how-police-locate-a-vehicle-india.md` and
`docs/03-no-login-data-sources.md`); replace every field before using this for a real report.

---

## 1. Core Fields

| Field | Value |
| --- | --- |
| **Plate number** | `[PLATE NUMBER, e.g. MH04FF4050]` |
| **Date & time of incident** | `[DD/MM/YYYY, HH:MM AM/PM]` |
| **Location** | `[Street / landmark / area, city]` |
| **Reporting person** | `[Name — filled by the person filing, never pre-filled]` |
| **Contact number** | `[Phone number]` |

## 2. Free-Text Notes

Plain, chronological, factual. What was observed, in the order it happened. No speculation about
identity or intent — only what was directly seen or heard.

```
[FREE-TEXT NOTES]

- What happened, in order:
- What was said/done (as close to verbatim as possible):
- Whether it was directed at the reporting person/household or among others present:
- Number and brief description of people involved (only what was actually seen):
- Vehicle description (colour, type, parked/moving, arrived/left in it):
```

## 3. Photo / Evidence Slots

Capture these where safe to do so; leave a slot blank and note why if it isn't possible.

- [ ] Plate — close-up, clearly readable
- [ ] Vehicle — multiple angles
- [ ] Scene — wide shot showing location/context
- [ ] Any damage or injury, if applicable
- [ ] CCTV still(s), if obtained — note source and preservation status below
- [ ] Video of the incident, if safely captured

| Evidence item | File reference | Source | Preserved? |
| --- | --- | --- | --- |
| `[e.g. plate-01.jpg]` | `[path/link]` | `[own phone / neighbour / shop camera]` | `[yes/no — request preservation same day; footage is often overwritten in 7–30 days]` |

**Witnesses**

| Name | Contact | What they saw |
| --- | --- | --- |
| `[PLACEHOLDER]` | `[PLACEHOLDER]` | `[PLACEHOLDER]` |

## 4. Structured Summary — for the Complaint (English)

Suitable to paste into the Maharashtra Police Citizen Portal (citizen.mahapolice.gov.in), an
e-FIR form where the offence category is eligible, or to read out at a police station.

```
Subject: Complaint regarding [PLACEHOLDER: brief nature, e.g. "an intimidation/nuisance incident"]
on [DATE] at [LOCATION].

I wish to report an incident that occurred at [LOCATION] at approximately [TIME] on [DATE].

[FREE-TEXT NOTES SUMMARY — chronological, factual, as captured in Section 2]

A vehicle bearing registration number [PLATE NUMBER] was present at the scene.
[Vehicle description — colour/type, parked/moving].

[Description of people involved, only what was directly observed. If none reliable, state
"No reliable description available."]

[Evidence available: photos/video/CCTV — list what exists, per Section 3.]

[If applicable: "I attempted to contact the police control room at [100/112] at approximately
[TIME] but could not get through."]

I am filing this for the incident to be on record and request that it be investigated and the
area monitored. I am available to provide further information or evidence as required.

Name: [PLACEHOLDER]
Contact: [PLACEHOLDER]
Date: [PLACEHOLDER]
```

**Likely classification (per `docs/01-lawful-lookup-and-complaint-routes.md` §3.3–3.4):**
verbal intimidation/abuse without weapon or assault is usually a **Non-Cognizable (NC)**
complaint under BNS 2023 Sections 351 (criminal intimidation), 352/356 (insult / intentional
annoyance) or 270 (public nuisance); it escalates toward an **FIR** if there is assault, a
weapon, or rash/dangerous driving (BNS Section 281). State the facts and let the police station
classify it — do not assert a section yourself in the complaint text.

## 5. Structured Summary — तक्रार (मराठी)

```
विषय: दिनांक [तारीख] रोजी [ठिकाण] येथे झालेल्या [PLACEHOLDER: घटनेचे स्वरूप, उदा. "धमकावणे/त्रास"]
याबाबत तक्रार.

मी आपणास कळवू इच्छितो की दिनांक [तारीख] रोजी अंदाजे [वेळ] वाजता [ठिकाण] येथे एक घटना घडली.

[विभाग २ मधील टिपांचा घटनाक्रमानुसार, तथ्यात्मक सारांश]

घटनास्थळी [वाहन क्रमांक] या क्रमांकाचे वाहन उपस्थित होते. [वाहनाचे वर्णन — रंग/प्रकार, उभे/फिरते].

[प्रत्यक्ष पाहिलेल्या व्यक्तींचे वर्णन. विश्वासार्ह वर्णन नसल्यास "विश्वासार्ह वर्णन उपलब्ध नाही" असे नमूद करावे.]

[उपलब्ध पुरावा: फोटो/व्हिडिओ/सीसीटीव्ही — विभाग ३ प्रमाणे नमूद करावे.]

[लागू असल्यास: "मी अंदाजे [वेळ] वाजता पोलीस नियंत्रण कक्षाला [१००/११२] वर संपर्क करण्याचा प्रयत्न
केला, परंतु संपर्क होऊ शकला नाही."]

ही तक्रार नोंदीसाठी दाखल करत आहे व विनंती करतो की याची चौकशी करून परिसराचे निरीक्षण करण्यात यावे.
आवश्यक ती अतिरिक्त माहिती किंवा पुरावा पुरवण्यास मी तयार आहे.

नाव: [PLACEHOLDER]
संपर्क: [PLACEHOLDER]
तारीख: [PLACEHOLDER]
```

## 6. WhatsApp-Length Version (5 lines each)

**English**

1. Complaint: [nature of incident] at [LOCATION] on [DATE] at approx. [TIME].
2. [Number] people involved; [what was said/done — only what was observed].
3. Vehicle [PLATE NUMBER] present at the scene ([parked/moving, colour/type]).
4. [If applicable] Tried calling [100/112] at approx. [TIME] but could not get through.
5. [Evidence available: yes/no, what kind]. Requesting this be recorded and the area monitored. — [Name, phone].

**मराठी**

१. तक्रार: [घटनेचे स्वरूप] दि. [तारीख] रोजी [ठिकाण] येथे अंदाजे [वेळ] वाजता.
२. [संख्या] व्यक्ती सहभागी; [जे प्रत्यक्ष दिसले/ऐकले तेवढेच].
३. [वाहन क्रमांक] क्रमांकाचे वाहन घटनास्थळी उपस्थित होते ([उभे/फिरते, रंग/प्रकार]).
४. [लागू असल्यास] अंदाजे [वेळ] वाजता [१००/११२] वर फोन करण्याचा प्रयत्न केला पण संपर्क होऊ शकला नाही.
५. [पुरावा उपलब्ध: होय/नाही, कोणता]. कृपया नोंद घ्यावी व परिसराचे निरीक्षण करावे. — [नाव, फोन नंबर].

## 7. Filing Reference (per `docs/01-lawful-lookup-and-complaint-routes.md`)

- Maharashtra Police Citizen Portal: https://citizen.mahapolice.gov.in (Citizen's Corner →
  Online Complaint/e-FIR). Not all offence types are e-FIR-eligible — harassment/intimidation
  usually requires an in-person visit to the police station.
- Emergency / control room: 112 (unified) or 100 (police control room). Both route to the same
  response system as of this project's research.
- CCTV footage is often overwritten in 7–30 days — request preservation from the camera owner
  the same day.
- Vehicle owner identity is not available to a private citizen from a public lookup (see
  `docs/01-lawful-lookup-and-complaint-routes.md` §2). Police obtain it via Vahan once a
  complaint/FIR exists; do not attempt to obtain it yourself outside that process.

## 8. What This Template Deliberately Does Not Do

- It does not look anything up automatically — no e-challan, PUC, insurance or RC query runs
  from filling this in. See `docs/03-no-login-data-sources.md` for the (separate, KYC-gated)
  no-login lookup pipeline design.
- It does not file, send or submit anything. A human reviews and submits every complaint
  produced from this template.
- It does not automate OTP, Aadhaar or any login flow on anyone's behalf.
