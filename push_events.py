"""
Bridge and Tunnel Brewery - GitHub Events Page Updater
"""
import os, sys, base64, subprocess
from datetime import datetime, date
from pathlib import Path
from openpyxl import load_workbook

CALENDAR_PATH = r"C:\Users\ADmin2\Desktop\BT_Events_Calendar.xlsx"
FLYERS_FOLDER = r"C:\Users\ADmin2\Desktop\Flyers"
REPO_PATH = r"C:\Users\ADmin2\Desktop\bt-events"
INDEX_PATH = os.path.join(REPO_PATH, "index.html")

def load_events():
    print("Reading events calendar...")
    wb = load_workbook(CALENDAR_PATH)
    ws = wb.active
    events = []
    today = date.today()

    headers = [str(c or "").strip().lower() for c in next(ws.iter_rows(min_row=4, max_row=4, values_only=True))]

    def col(*names):
        for name in names:
            key = name.strip().lower()
            if key in headers:
                return headers.index(key)
        return None

    date_col = col("date")
    venue_col = col("venue")
    act_col = col("act / event name")
    bands_col = col("bands", "bands (all acts on the bill)")
    flyer_col = col("flyer filename")
    ticket_col = col("ticket link")
    notes_col = col("notes")

    for row in ws.iter_rows(min_row=5, values_only=True):
        if date_col is None or date_col >= len(row) or not row[date_col]:
            continue
        raw_date = row[date_col]
        venue = str(row[venue_col] or "").strip() if venue_col is not None and venue_col < len(row) else ""
        act_name = str(row[act_col] or "").strip() if act_col is not None and act_col < len(row) else ""
        bands = str(row[bands_col] or "").strip() if bands_col is not None and bands_col < len(row) else ""
        flyer_filename = str(row[flyer_col] or "").strip() if flyer_col is not None and flyer_col < len(row) else ""
        ticket_link = str(row[ticket_col] or "").strip() if ticket_col is not None and ticket_col < len(row) else ""
        notes = str(row[notes_col] or "").strip() if notes_col is not None and notes_col < len(row) else ""
        event_date = None
        try:
            if isinstance(raw_date, datetime):
                event_date = raw_date.date()
            elif isinstance(raw_date, date):
                event_date = raw_date
            elif isinstance(raw_date, str):
                for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y"]:
                    try:
                        event_date = datetime.strptime(raw_date.strip(), fmt).date()
                        break
                    except:
                        continue
        except:
            continue
        if not event_date or event_date < today:
            continue
        if not flyer_filename:
            continue
        flyer_path = Path(FLYERS_FOLDER) / flyer_filename
        if not flyer_path.exists():
            print(f"  Skipping {act_name} - flyer not found: {flyer_filename}")
            continue
        date_display = event_date.strftime("%A, %B %d, %Y").replace(" 0", " ")
        events.append({
            "date": event_date,
            "date_display": date_display,
            "venue": venue,
            "act_name": act_name,
            "bands": bands,
            "flyer_path": str(flyer_path),
            "ticket_link": ticket_link,
            "notes": notes,
        })
    events.sort(key=lambda x: x["date"])
    print(f"Found {len(events)} upcoming events with flyers")
    return events

def build_event_card(event):
    flyer_path = Path(event["flyer_path"])
    ext = flyer_path.suffix.lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}
    mime = mime_map.get(ext, "image/jpeg")
    if ext == ".pdf":
        img_html = '<div class="event-placeholder">PDF Flyer</div>'
    else:
        with open(flyer_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        img_html = f'<img class="event-img" src="data:{mime};base64,{img_data}" alt="{event["act_name"]}">'
    bands_html = ""
    if event["bands"]:
        band_list = [b.strip() for b in event["bands"].split("/") if b.strip()]
        bands_html = '<div class="event-bill">' + "".join([f"• {b}<br>" for b in band_list]) + "</div>"
    ticket_link = event["ticket_link"].strip() if event["ticket_link"] else ""
    notes_lower = event["notes"].lower() if event["notes"] else ""
    if ticket_link.startswith("http"):
        btn = f'<a href="{ticket_link}" target="_blank" class="btn btn-tickets">GET TICKETS</a>'
    elif "free" in notes_lower:
        btn = '<span class="btn btn-free">FREE ADMISSION</span>'
    else:
        btn = '<span class="btn btn-door">ADMISSION AT DOOR</span>'
    notes_html = f'<div class="event-notes">{event["notes"]}</div>' if event["notes"] else ""
    return f"""<div class="event-card">{img_html}<div class="event-details"><div class="event-date">{event["date_display"]}</div><div class="event-name">{event["act_name"]}</div>{bands_html}{notes_html}{btn}</div></div>"""

def build_section(events):
    if not events:
        return '<div class="no-events">No upcoming events - check back soon!</div>'
    return "\n".join([build_event_card(e) for e in events])

def update_index(events):
    ridgewood = [e for e in events if "ridgewood" in e["venue"].lower()]
    liberty = [e for e in events if "liberty" in e["venue"].lower()]
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    r_start = html.index("<!-- RIDGEWOOD_START -->") + len("<!-- RIDGEWOOD_START -->")
    r_end = html.index("<!-- RIDGEWOOD_END -->")
    html = html[:r_start] + "\n" + build_section(ridgewood) + "\n" + html[r_end:]
    l_start = html.index("<!-- LIBERTY_START -->") + len("<!-- LIBERTY_START -->")
    l_end = html.index("<!-- LIBERTY_END -->")
    html = html[:l_start] + "\n" + build_section(liberty) + "\n" + html[l_end:]
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html updated")

def push_to_github():
    print("Pushing to GitHub...")
    os.chdir(REPO_PATH)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Update events {date.today()}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"\nDone! Live at: https://richbigdreamer.github.io/bt-events")

if __name__ == "__main__":
    print("\nBridge and Tunnel Brewery - Events Page Updater")
    print("=" * 50)
    events = load_events()
    if not events:
        print("\nNo upcoming events with flyers found.")
        sys.exit(0)
    print(f"\nBuilding page with {len(events)} event(s)...")
    update_index(events)
    push_to_github()
