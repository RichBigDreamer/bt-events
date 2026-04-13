"""
Bridge and Tunnel Brewery - Email Sender with Base64 Inline Images
------------------------------------------------------------------
Uses base64 data URIs instead of CID references for maximum compatibility.
Images appear inline in all major email clients including Network Solutions webmail.

Usage:
  python send_email.py --to "recipient@email.com" --subject "Subject" --body "Message"
  python send_email.py --bcc "a@b.com,c@d.com" --subject "Blast" --body "Hello!" --images "flyer1.jpg,flyer2.jpg"
"""

import smtplib
import argparse
import sys
import os
import base64
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image

SMTP_SERVER = "netsol-smtp-oxcs.hostingplatform.com"
SMTP_PORT = 587
FROM_EMAIL = "rich@bridgeandtunnelbrewery.com"
FROM_PASSWORD = "YOUR_EMAIL_PASSWORD_HERE"
FROM_NAME = "Bridge and Tunnel Brewery"

MAX_WIDTH = 600
MAX_HEIGHT = 900
JPEG_QUALITY = 72


def compress_image_to_base64(path):
    """Compress image and return base64 data URI string."""
    try:
        img = Image.open(path)
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        w, h = img.size
        if w > MAX_WIDTH or h > MAX_HEIGHT:
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        compressed = buf.getvalue()
        original_size = os.path.getsize(path)
        print(f"  {os.path.basename(path)}: {original_size//1024}KB -> {len(compressed)//1024}KB")
        b64 = base64.b64encode(compressed).decode()
        return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        print(f"  WARNING: Could not compress {path}: {e} — skipping")
        return None


def build_html_body(text, image_data_uris):
    html_text = text.replace("\n", "<br>")
    image_tags = ""
    for uri in image_data_uris:
        image_tags += f'<br><img src="{uri}" style="max-width:600px;width:100%;display:block;margin:10px 0;">'
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;color:#333;max-width:650px;margin:0 auto;padding:20px;">
  <p style="font-size:14px;line-height:1.6;">{html_text}</p>
  {image_tags}
  <br>
  <p style="font-size:12px;color:#888;border-top:1px solid #eee;padding-top:10px;margin-top:20px;">
    Bridge and Tunnel Brewery<br>
    Ridgewood, Queens | Liberty, NY Catskills<br>
    <a href="https://www.bridgeandtunnelbrewery.com" style="color:#888;">bridgeandtunnelbrewery.com</a>
  </p>
</body>
</html>"""


def send_email(to=None, bcc=None, subject="", body="", image_paths=None):
    to_list = [e.strip() for e in to.split(",")] if to else []
    bcc_list = [e.strip() for e in bcc.split(",")] if bcc else []
    all_recipients = to_list + bcc_list

    if not all_recipients:
        print("ERROR: No recipients specified.")
        sys.exit(1)

    # Compress and encode images
    image_data_uris = []
    if image_paths:
        print(f"\nCompressing {len(image_paths)} image(s)...")
        for path in image_paths:
            path = path.strip()
            if not os.path.isabs(path):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(script_dir, path)
            if not os.path.exists(path):
                print(f"  WARNING: Not found: {path} — skipping")
                continue
            uri = compress_image_to_base64(path)
            if uri:
                image_data_uris.append(uri)

    # Build HTML
    html_body = build_html_body(body, image_data_uris)
    plain_body = body

    # Estimate size
    total_kb = len(html_body.encode()) // 1024
    print(f"  Total email size: ~{total_kb}KB ({total_kb//1024}MB)")
    if total_kb > 8000:
        print("  WARNING: Email is very large (>8MB) — may be filtered")

    # Build message — simple multipart/alternative, no attachments
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["Subject"] = subject
    msg["List-Unsubscribe"] = f"<mailto:{FROM_EMAIL}?subject=unsubscribe>"
    if to_list:
        msg["To"] = ", ".join(to_list)

    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    # Send
    print(f"\nConnecting to {SMTP_SERVER}:{SMTP_PORT}...")
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            print("Logging in...")
            server.login(FROM_EMAIL, FROM_PASSWORD)
            print(f"Sending to {len(all_recipients)} recipient(s)...")
            server.sendmail(FROM_EMAIL, all_recipients, msg.as_string())
            print(f"Email sent successfully! ({len(image_data_uris)} inline images)")
            return True
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Authentication failed.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", help="Recipient email(s), comma-separated")
    parser.add_argument("--bcc", help="BCC email(s), comma-separated")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--images", help="Image paths, comma-separated")
    args = parser.parse_args()
    image_list = [i.strip() for i in args.images.split(",")] if args.images else []
    send_email(to=args.to, bcc=args.bcc, subject=args.subject, body=args.body, image_paths=image_list)
