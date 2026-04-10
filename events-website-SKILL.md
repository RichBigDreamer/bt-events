---
name: events-website
description: >
  Use this skill whenever Rich sends a flyer image on Telegram, asks to update
  the events website, asks to add or remove a show, or asks Lena to run the
  website updater. This skill covers the full workflow: extracting event info
  from flyers, confirming with Rich, updating the Excel calendar, updating the
  events website via GitHub, and keeping everything in sync.
---

# Events Website Skill

This skill governs how Lena manages Bridge and Tunnel Brewery's events page
at https://richbigdreamer.github.io/bt-events (also embedded at
bridgeandtunnelbrewery.com/events).

---

## Key Locations

| What | Where |
|---|---|
| Events Calendar | `C:\Users\Admin2\Desktop\BT_Events_Calendar.xlsx` |
| Flyers Folder | `C:\Users\Admin2\Desktop\Flyers` |
| Website Repo | `C:\Users\Admin2\Desktop\bt-events` |
| Update Script | `C:\Users\Admin2\Desktop\bt-events\push_events.py` |
| Live Website | https://richbigdreamer.github.io/bt-events |

---

## Excel Calendar Column Structure

| Column | Field |
|---|---|
| A | Date (MM/DD/YYYY) |
| B | Venue (Ridgewood or Liberty) |
| C | Act / Event Name |
| D | Bands (all acts, separated by /) |
| E | Promotor Name (admin only, not shown publicly) |
| F | Promotor Email (admin only, not shown publicly) |
| G | Flyer Filename (must match file in Flyers folder exactly) |
| H | Ticket Link (URL or leave blank) |
| I | Blast Sent? (yes/no) |
| J | Website Updated? (yes/no) |
| K | Notes (door time, price, age, special notes) |

---

## Workflow 1 — Rich Forwards a Flyer

**Trigger:** Rich sends an image on Telegram.

### Step 1 — Extract from flyer using AI vision
Read the flyer and extract:
- **Date** — convert to MM/DD/YYYY format. If no year, use current or next upcoming year.
- **Venue** — Ridgewood or Liberty:
  - Ridgewood: "1535 Decatur", "Ridgewood", "Queens"
  - Liberty: "50 Lake", "Liberty", "Catskills"
  - Default to Ridgewood if unclear — flag it
- **Act / Event Name** — headliner or show title (largest/topmost text)
- **Bands** — ALL acts listed, separated by /
- **Notes** — door time, show time, price, age restriction, "respect the space", etc.
- **Ticket Link** — any URL found on flyer
- **Admission type** — if FREE, note it in Notes column

### Step 2 — Present to Rich for confirmation
Always confirm before doing anything. Use this format:

```
Got the flyer! Here's what I extracted:

📅 Date: [date]
📍 Venue: [Ridgewood or Liberty]
🎤 Show: [act/event name]
🎸 Bands: [band1 / band2 / band3]
📋 Notes: [door time, price, age, etc.]
🎟 Tickets: [URL or "Admission at Door" or "Free"]

Reply YES to update the calendar and website, or correct anything above.
```

**Wait for Rich's reply before proceeding.**

### Step 3 — Save flyer file
Save the flyer to:
```
C:\Users\Admin2\Desktop\Flyers\
```
Name it clearly:
```
[venue]_[date]_[showname].jpg
```
Example: `ridgewood_apr19_sawed_offs.jpg`

### Step 4 — Update Excel calendar
Add a new row with all extracted fields. Set:
- Blast Sent = no
- Website Updated = no

### Step 5 — Update website
Run:
```
python "C:\Users\Admin2\Desktop\bt-events\push_events.py"
```

After running, confirm to Rich:
```
✅ [Show name] on [date] is now live on the events page.
Check it at: bridgeandtunnelbrewery.com/events
```

Update Website Updated column to "yes" in the calendar.

---

## Workflow 2 — Manual Website Update

**Trigger:** Rich says "update the website", "refresh the events page", or "clean up past events."

Just run:
```
python "C:\Users\Admin2\Desktop\bt-events\push_events.py"
```

The script automatically:
- Removes past events
- Shows all upcoming events that have flyers
- Pushes to GitHub Pages

---

## Workflow 3 — Promotor Reminder

**Trigger:** Rich asks "remind promotors about flyers" or Lena notices a show is coming up without a flyer.

Check the calendar for shows within the next 14 days where Flyer Filename is empty.
For each one, send a reminder email to the promotor using:

```
python "C:\Users\Admin2\.openclaw\workspace\send_email.py"
  --to "[promotor email]"
  --subject "Flyer needed for [show name] on [date]"
  --body "Hi [promotor name], just a reminder that we still need the flyer for [show name] on [date] at Bridge and Tunnel Brewery. Please send it over as soon as possible so we can promote the show. Thanks! Rich"
```

---

## Admission Display Rules

| Flyer says | Show on website as |
|---|---|
| Ticket URL present | GET TICKETS button (red) |
| FREE / Free Admission | FREE ADMISSION button (green) |
| Price ($10, $15, etc.) | ADMISSION AT DOOR button (dark) |
| Nothing listed | ADMISSION AT DOOR button (dark) |

---

## Venue Rules

| Flyer says | Assign to |
|---|---|
| 1535 Decatur / Ridgewood / Queens | Ridgewood |
| 50 Lake / Liberty / Catskills | Liberty |
| "Bridge and Tunnel" only | Ridgewood (default) |
| Unclear | Ridgewood + flag for Rich |

---

## Principles

**Always confirm before acting.** Never update the calendar or website without Rich's explicit YES.

**No flyer = no website listing.** A show only appears on the website once a flyer file exists in the Flyers folder.

**Promotor info stays private.** Never show promotor name or email publicly on the website.

**Past events auto-remove.** The script handles this — no manual cleanup needed.

**One command updates everything.** `python push_events.py` reads the calendar, builds the page, and pushes to GitHub in one shot.
