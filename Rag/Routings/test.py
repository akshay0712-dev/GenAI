import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict


def topic_links() :
    BASE_INDEX = "https://docs.chaicode.com/youtube/getting-started/"
    BASE_DOCS = "https://docs.chaicode.com"
    def get_all_links_from_page(url):
        """Fetch all absolute URLs from a given page."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = {
                urljoin(BASE_DOCS, a['href'])
                for a in soup.find_all('a', href=True)
                if a['href'].startswith('/youtube/chai-aur-')  # Ensure relevant links only
            }
            return list(links)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []

    def group_links_by_topic(welcome_links):
        """From welcome links, extract topics and gather full lesson links per topic."""
        topic_urls = defaultdict(list)

        for welcome_url in welcome_links:
            # Get topic root: remove '/welcome/' from the end
            if not welcome_url.endswith('/welcome/'):
                continue
            topic_base = welcome_url.rsplit('welcome/', 1)[0]
            topic_slug = topic_base.strip("/").split("/")[-1]  # e.g., chai-aur-html
            topic = topic_slug.replace("chai-aur-", "")

            # Fetch lesson links under this topic
            topic_lessons = get_all_links_from_page(welcome_url)
            # Filter only links starting with the base (e.g., chai-aur-html/)
            full_lesson_links = [
                link for link in topic_lessons if link.startswith(topic_base)
            ]

            topic_urls[topic] = sorted(set(full_lesson_links))  # Deduplicate + sort

        return dict(topic_urls)

    # === Main ===
    welcome_links = get_all_links_from_page(BASE_INDEX)
    topic_urls = group_links_by_topic(welcome_links)
    return(topic_urls)


topic_urls = topic_links()
# Output or use it
for topic, urls in topic_urls.items():
    print(f"\n📚 {topic.upper()} ({len(urls)} lessons)")
    for url in urls:
        print(" =>", url)
        
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        extracted_text = soup.get_text(separator="\n")
        with open("scraped_text.txt", "a", encoding="utf-8") as f:
            # Write text to file
            f.write(f"URL: {url}\n")
            f.write(extracted_text + "\n")
        
        # Print text output
        print(extracted_text)
