print("Script started")

import requests
from bs4 import BeautifulSoup

# URL of the Moby Dick page with chapters and anchors
book_url = 'https://www.gutenberg.org/cache/epub/2701/pg2701-images.html'

# Get the webpage content
response = requests.get(book_url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links in the page that start with '#link2HCH' (these are chapter anchors)
toc_links = []
for link in soup.find_all('a'):
    href = link.get('href', '')
    if href.startswith('#link2HCH'):
        # Build full URL to the chapter by appending the anchor to the page URL
        full_url = book_url + href
        toc_links.append(full_url)

# Save all chapter URLs to a text file, one per line
with open('moby_chapters.txt', 'w') as f:
    for link in toc_links:
        f.write(link + '\n')

print(f"Saved {len(toc_links)} chapter URLs to moby_chapters.txt")