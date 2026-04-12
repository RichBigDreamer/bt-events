---
name: events-website
description: >
  Use this skill whenever Rich sends a flyer image on Telegram, asks to update
  the events website, asks to add or remove a show, or asks Lena to run the
  website updater. This skill covers the full workflow: extracting event info
  from flyers, confirming with Rich, updating the Excel calendar, and updating
  the events website via GitHub.
---

# Events Website Skill

Lena manages Bridge and Tunnel Brewery events page at:
- https://richbigdreamer.github.io/bt-events
- Embedded at: bridgeandtunnelbrewery.com/events

---

## Key Locations

| What | Where |
|---|---|
| Events Calendar | C:\Users\Admin2\Desktop\BT_Events_Calendar.xlsx |
| Flyers Folder | C:\Users\Admin2\Desktop\Flyers |
| Website Repo | C:\Users\Admin2\Desktop\bt-events |
| Update Script | C:\Users\Admin2\Desktop\bt-events\push_events.py |

---

## Excel Calendar Column Structure

| Column | Field | Notes |
|---|---|---|
| A | Date | MM/DD/YYYY format |
| B | Venue | Must be exactly "Ridgewood" or "Liberty" |
| C | Show Description | ALL extracted info from flyer |
| D | Promotor Name | Admin only - never shown publicly |
| E | Promotor Phone | Admin only - never shown publicly |
| F | Promotor Email | Admin only - never shown publicly |
| G | Flyer Filename | Must match file in Flyers folder exactly |
| H | Ticket Link | Full URL or leave blank |
| I | Blast Sent? | yes or no |
| J | Website Updated? | yes or no |

### Show Description column C - what to include:
Extract ALL of the following from the flyer:
- All band/act names performing that night
- Door time and show/music time
- Ticket price or FREE
- Age restriction (21+, All Ages, 18+)
- Any special notes ("respect the space", etc.)
- Promotor or presenter name if listed on flyer

Example:
Still Burning / Outlaws No Values / 50 Days at Ilam / Daisies Taller Than Trees
Doors: 7PM | Music: 8PM
$15 | 21+

---

## Critical Rules for Excel Entry

- NEVER skip rows. Add new shows on the very next empty row immediately after the last entry.
- No blank rows between entries.
- Venue must be exactly "Ridgewood" or "Liberty" - spelling matters.
- Flyer filename must match exactly what is saved in the Flyers folder including extension.
- Promotor info (columns D, E, F) stays private - never shown on website.
- Do not delete old rows. Rich keeps contact info for future bookings.

---

## Workflow 1 - Rich Forwards a Flyer

Step 1: Extract from flyer using AI vision:
- Date, Venue, All bands/acts, Door time, Show time, Price, Age restriction, Special notes, Ticket URL

Step 2: Present to Rich for confirmation:
"Got the flyer! Here's what I extracted:
Date: [date]
Venue: [Ridgewood or Liberty]
Description: [all extracted show info]
Ticket Link: [URL or none]
Reply YES to update the calendar and website, or correct anything."

Wait for Rich's YES before proceeding.

Step 3: Save flyer to C:\Users\Admin2\Desktop\Flyers\
Name format: [venue]_[date]_[showname].jpg

Step 4: Update Excel calendar on next empty row - no skipping rows.

Step 5: Run website updater:
python "C:\Users\Admin2\Desktop\bt-events\push_events.py"

Step 6: Confirm to Rich and update Website Updated = yes in calendar.

---

## Workflow 2 - Manual Website Update

Run: python "C:\Users\Admin2\Desktop\bt-events\push_events.py"

Past events are NOT automatically removed. Lena must manually update the calendar when Rich asks to remove a show. This protects promotor contact info.

---

## Venue Rules

| Flyer says | Assign to |
|---|---|
| 1535 Decatur / Ridgewood / Queens | Ridgewood |
| 50 Lake / Liberty / Catskills | Liberty |
| Bridge and Tunnel only | Ridgewood (default) |
| Unclear | Ridgewood + flag for Rich |

---

## Ticket Button Rules

| Situation | Button |
|---|---|
| Ticket URL in column H | GET TICKETS (red) |
| "free" in description | FREE ADMISSION (green) |
| No URL, not free | ADMISSION AT DOOR (dark) |

---

## Website Layout

Desktop: Flyer left | Description middle | Ticket button right
Mobile: Flyer full width, description below, button below
Navigation: Sticky bar - Ridgewood, Liberty, Home links
Anchors: #ridgewood and #liberty for homepage button links

---

## Principles

- Always confirm before acting - never update without Rich's YES
- No flyer = no website listing
- Never show promotor info publicly
- Never skip rows in Excel calendar
- Never delete old calendar rows
- Both venue sections always show even when one has no events

---

## Auto-Expiry

Past events are automatically removed from the website display when push_events.py runs. Lena does NOT need to manually remove past events from the website. The script handles this automatically based on today's date.

The Excel calendar is NEVER touched by the script — it only reads from it. All historical show data, band names, and promotor contact info stays in the Excel sheet permanently.

---

## Critical Data Protection Rules

- NEVER delete any rows from BT_Events_Calendar.xlsx without explicit permission from Rich.
- NEVER clear or overwrite the Show Description, Promotor Name, Promotor Phone, or Promotor Email columns for any show.
- Rich uses historical band and promotor contact information for future in-house show bookings. This data must be preserved.
- If Rich asks to "clean up" the calendar, clarify whether he means the website (handled automatically) or the Excel file (requires his explicit confirmation before touching anything).
- When in doubt — ask Rich before deleting or modifying any existing calendar data.
