import requests
import os

chapter_file = 'moby_chapters.txt'
progress_file = 'moby_progress.txt'

with open(chapter_file, 'r') as f:
    chapters = [line.strip() for line in f.readlines()]

if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        idx = int(f.read().strip())
else:
    idx = 0

if idx >= len(chapters):
    print("All chapters read!")
    exit()

chapter_url = chapters[idx]
print(f"Reading Chapter {idx + 1}: {chapter_url}")

chapter_html = requests.get(chapter_url).text
with open(f'chapter_{idx + 1}.html', 'w', encoding='utf-8') as f:
    f.write(chapter_html)

with open(progress_file, 'w') as f:
    f.write(str(idx + 1))