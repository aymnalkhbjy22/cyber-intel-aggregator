import asyncio
import hashlib
import json
import locale
import os
from datetime import datetime
import aiohttp
from deep_translator import GoogleTranslator
import feedparser

DEVELOPER = "Ayman Al-Khubji"
DB_FILE = "processed_hashes.json"
OUTPUT_REPORT = "CYBER_FEED_REPORT.md"


def get_system_lang():
  try:
    loc = locale.getdefaultlocale()[0]
    return loc.split("_")[0] if loc else "ar"
  except Exception:
    return "ar"


def load_processed_hashes():
  if os.path.exists(DB_FILE):
    try:
      with open(DB_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))
    except Exception:
      return set()
  return set()


def save_processed_hashes(hashes):
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(list(hashes), f, ensure_ascii=False)


def generate_content_hash(title, link):
  raw_payload = f"{title.strip().lower()}{link.strip().lower()}"
  return hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()


class CyberIntelEngine:

  def __init__(self, sources):
    self.sources = sources
    self.target_lang = get_system_lang()
    self.translator = GoogleTranslator(
        source="auto", target=self.target_lang
    )
    self.processed_hashes = load_processed_hashes()
    self.new_reports = []

  async def fetch_feed(self, session, source_url):
    try:
      async with session.get(source_url, timeout=10) as response:
        if response.status == 200:
          data = await response.text()
          return feedparser.parse(data)
    except Exception:
      return None

  def process_article(self, entry, source_name):
    title = entry.get("title", "")
    link = entry.get("link", "")
    summary = entry.get("summary", "")[:200]

    if not title or not link:
      return

    article_hash = generate_content_hash(title, link)
    if article_hash in self.processed_hashes:
      return

    self.processed_hashes.add(article_hash)

    translated_title = title
    try:
      if self.target_lang != "en":
        translated_title = self.translator.translate(title)
    except Exception:
      pass

    self.new_reports.append({
        "source": source_name,
        "title": translated_title,
        "link": link,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    })

  async def run(self):
    headers = {"User-Agent": "CyberIntel-Aggregator-v1.0"}
    async with aiohttp.ClientSession(headers=headers) as session:
      tasks = [
          self.fetch_feed(session, url) for url in self.sources.values()
      ]
      results = await asyncio.gather(*tasks, return_exceptions=True)

      for (source_name, _), feed in zip(self.sources.items(), results):
        if feed and hasattr(feed, "entries"):
          for entry in feed.entries:
            self.process_article(entry, source_name)

    save_processed_hashes(self.processed_hashes)
    self.generate_markdown_report()

  def generate_markdown_report(self):
    if not self.new_reports:
      print("No new unique reports found.")
      return

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
      f.write("# 🛡️ Real-Time Global Cyber Threats & Intelligence Feed\n\n")
      f.write(f"- **Lead Developer:** {DEVELOPER}\n")
      f.write(
          f"- **Updated At:**"
          f" {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
      )
      f.write(
          "- **Engine:** SHA-256 Deduplication (Zero Redundancy Guarantee)\n\n"
      )
      f.write("| Source | News Title (Auto-Localized) | Read Details |\n")
      f.write("|---|---|---|\n")

      for item in self.new_reports:
        clean_title = item["title"].replace("|", "-")
        f.write(
            f"| **{item['source']}** | {clean_title} | [Direct"
            f" Link]({item['link']}) |\n"
        )

    print(f"Generated {len(self.new_reports)} articles successfully.")


GLOBAL_SOURCES = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Bleeping Computer": "https://www.bleepingcomputer.com/feed/",
    "SecurityWeek": "https://feeds.feedburner.com/securityweek",
    "Dark Reading": "https://www.darkreading.com/rss.xml",
    "Cisco Talos": "https://blog.talosintelligence.com/rss/",
}

if __name__ == "__main__":
  engine = CyberIntelEngine(GLOBAL_SOURCES)
  asyncio.run(engine.run())
