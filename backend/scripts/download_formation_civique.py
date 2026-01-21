"""
Download all pages from formation-civique.interieur.gouv.fr as PDFs.

This script:
1. Crawls the website to find all pages
2. Downloads each page as HTML
3. Converts to PDF using weasyprint or pdfkit

Requirements:
    pip install requests beautifulsoup4 weasyprint

Usage:
    python scripts/download_formation_civique.py
"""

import os
import sys
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import Set, List
import time

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system(f"{sys.executable} -m pip install beautifulsoup4")
    from bs4 import BeautifulSoup

try:
    from weasyprint import HTML
except ImportError:
    print("Installing weasyprint...")
    os.system(f"{sys.executable} -m pip install weasyprint")
    from weasyprint import HTML


class FormationCiviqueDownloader:
    def __init__(self, base_url: str, output_dir: str = "downloaded_pages"):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.visited_urls: Set[str] = set()
        self.found_urls: Set[str] = set()

    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and from the same domain."""
        parsed = urlparse(url)

        # Must be from the same domain
        if parsed.netloc and parsed.netloc != self.base_domain:
            return False

        # Skip non-HTML resources
        skip_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.css', '.js', '.ico']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False

        # Skip anchors
        if '#' in url:
            url = url.split('#')[0]

        return True

    def get_links_from_page(self, url: str, html: str) -> List[str]:
        """Extract all links from a page."""
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']

            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)

            # Remove fragments
            absolute_url = absolute_url.split('#')[0]

            if self.is_valid_url(absolute_url):
                links.append(absolute_url)

        return links

    def sanitize_filename(self, url: str) -> str:
        """Convert URL to safe filename."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')

        if not path or path == '':
            return 'index'

        # Replace slashes and special chars
        filename = path.replace('/', '_').replace('?', '_').replace('&', '_')

        # Limit length
        if len(filename) > 100:
            filename = filename[:100]

        return filename

    def download_page(self, url: str) -> bool:
        """Download a single page and convert to PDF."""
        try:
            print(f"📥 Downloading: {url}")

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Get filename
            filename = self.sanitize_filename(url)
            pdf_path = self.output_dir / f"{filename}.pdf"
            html_path = self.output_dir / f"{filename}.html"

            # Save HTML for reference
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            # Convert to PDF
            try:
                HTML(string=response.text, base_url=url).write_pdf(pdf_path)
                print(f"   ✅ Saved: {pdf_path}")
            except Exception as e:
                print(f"   ⚠️  PDF conversion failed: {e}")
                print(f"   💾 HTML saved instead: {html_path}")

            # Extract links for crawling
            links = self.get_links_from_page(url, response.text)
            for link in links:
                if link not in self.visited_urls and link not in self.found_urls:
                    self.found_urls.add(link)

            return True

        except Exception as e:
            print(f"   ❌ Error downloading {url}: {e}")
            return False

    def crawl(self, max_pages: int = 100):
        """Crawl the website and download all pages."""
        print(f"🕷️  Starting crawl of {self.base_url}")
        print(f"📂 Output directory: {self.output_dir.absolute()}\n")

        # Start with base URL
        self.found_urls.add(self.base_url)

        page_count = 0

        while self.found_urls and page_count < max_pages:
            # Get next URL to visit
            url = self.found_urls.pop()

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)

            # Download and process
            if self.download_page(url):
                page_count += 1

            # Be polite - don't hammer the server
            time.sleep(1)

            print(f"📊 Progress: {page_count} pages downloaded, {len(self.found_urls)} in queue\n")

        print(f"\n✅ Crawl complete!")
        print(f"   Downloaded: {page_count} pages")
        print(f"   Output: {self.output_dir.absolute()}")


def main():
    print("=" * 60)
    print("Formation Civique Website Downloader")
    print("=" * 60 + "\n")

    base_url = "https://formation-civique.interieur.gouv.fr/"
    output_dir = "formation_civique_pdfs"

    downloader = FormationCiviqueDownloader(base_url, output_dir)

    try:
        downloader.crawl(max_pages=100)
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        print(f"   Partial downloads saved in: {downloader.output_dir.absolute()}")


if __name__ == "__main__":
    main()
