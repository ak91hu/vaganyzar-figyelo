import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "3600"))
DATA_PATH = os.getenv("DATA_PATH", "/data")
SEEN_FILE = os.path.join(DATA_PATH, "seen_links.json")
URL = "https://www.mavcsoport.hu/mav-szemelyszallitas/belfoldi-utazas/vaganyzar?field_line_lock_relation_value=1"


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    os.makedirs(DATA_PATH, exist_ok=True)
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=2)


def fetch_pdfs():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    pdf_links = soup.find_all("a", href=lambda h: h and h.endswith(".pdf"))

    results = []
    for link in pdf_links:
        results.append({"pdf": link["href"]})
    return results


def post_to_discord(item):
    pdf = item["pdf"]
    embed = {
        "title": "🚧 Új vágányzár",
        "description": "A MÁV új vágányzárat jelentett be.",
        "color": 15158332,
        "fields": [
            {"name": "📄 Részletek", "value": f"[Megnyitás]({pdf})", "inline": False}
        ],
        "footer": {"text": f"MÁV automatikus figyelő • {datetime.now().strftime('%Y.%m.%d %H:%M')}"},
    }
    payload = {"embeds": [embed]}
    r = requests.post(DISCORD_WEBHOOK, json=payload)
    if r.status_code not in (200, 204):
        print(f"⚠️ Discord hiba: {r.status_code} - {r.text}")
    else:
        print(f"✅ Új vágányzár elküldve Discordra: {pdf}")


def check_and_post(seen):
    items = fetch_pdfs()
    new_items = [i for i in items if i["pdf"] not in seen]

    if new_items:
        print(f"📢 {len(new_items)} új PDF található!")
        for item in new_items:
            post_to_discord(item)
            seen.add(item["pdf"])
        save_seen(seen)
    else:
        print("🔎 Nincs új PDF.")


def main():
    if not DISCORD_WEBHOOK:
        raise SystemExit("❌ DISCORD_WEBHOOK nincs beállítva!")

    print("🚆 MÁV vágányzár figyelő elindult...")
    seen = load_seen()
    check_and_post(seen)


if __name__ == "__main__":
    main()

