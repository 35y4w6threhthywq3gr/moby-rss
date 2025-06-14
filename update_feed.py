import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

# Config
book_url_base = 'https://www.gutenberg.org/cache/epub/2701/pg2701-images.html'
chapter_file = 'moby_chapters.txt'
progress_file = 'moby_progress.txt'
feed_file = 'feed.xml'

# Load chapter URLs
with open(chapter_file, 'r') as f:
    chapters = [line.strip() for line in f.readlines()]

# Load progress
if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        idx = int(f.read().strip())
else:
    idx = 0

if idx >= len(chapters):
    print("All chapters read!")
    exit()

chapter_url = chapters[idx]

# Fetch chapter page
response = requests.get(chapter_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract chapter anchor id from URL (e.g. #link2HCH0001)
anchor_id = chapter_url.split('#')[-1] if '#' in chapter_url else None

# Extract first 2 paragraphs after anchor
snippet_html = "<p>Content not found.</p>"
if anchor_id:
    anchor = soup.find(id=anchor_id)
    if anchor:
        paragraphs = []
        for sibling in anchor.next_siblings:
            if sibling.name == 'p':
                paragraphs.append(str(sibling))
                if len(paragraphs) >= 2:
                    break
        if paragraphs:
            snippet_html = ''.join(paragraphs)

# Prepare new RSS item
chapter_title = f"Chapter {idx + 1}"
pub_date = (datetime.utcnow() + timedelta(days=idx)).strftime('%a, %d %b %Y %H:%M:%S GMT')

new_item = f"""
  <item>
    <title>{chapter_title}</title>
    <link>{chapter_url}</link>
    <description><![CDATA[
      {snippet_html}
    ]]></description>
    <pubDate>{pub_date}</pubDate>
  </item>
"""

# Read existing feed.xml or create basic if not exists
if os.path.exists(feed_file):
    with open(feed_file, 'r', encoding='utf-8') as f:
        feed_content = f.read()
else:
    feed_content = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>Moby Dick Feed</title>
  <link>https://yourdomain.com/moby</link>
  <description>A chapter of Moby Dick every day</description>
  <language>en-us</language>
</channel>
</rss>
"""

# Insert new item before closing </channel> tag
feed_content = feed_content.replace('</channel>', new_item + '\n</channel>')

# Save updated feed.xml
with open(feed_file, 'w', encoding='utf-8') as f:
    f.write(feed_content)

# Update progress
with open(progress_file, 'w') as f:
    f.write(str(idx + 1))

print(f"Added Chapter {idx + 1} to feed.xml")