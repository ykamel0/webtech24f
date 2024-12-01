import os
import feedparser
from datetime import datetime

def fetch_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    if feed.bozo:
        print(f"Error parsing feed from {feed_url}: {feed.bozo_exception}")
        return []
    articles = []
    for entry in feed.entries:
        article = {
            "title": entry.get("title", "No title"),
            "summary": entry.get("summary", "No summary"),
            "link": entry.get("link", "No URL"),
        }
        articles.append(article)
    return articles

def fetch_from_multiple_feeds(feed_urls):
    all_articles = []
    for url in feed_urls:
        articles = fetch_rss_feed(url)
        all_articles.extend(articles)
    return all_articles

def filter_articles_by_keywords(articles, keywords):
    filtered_articles = []
    for article in articles:
        if any(keyword.lower() in (article['title'] + article['summary']).lower() for keyword in keywords):
            filtered_articles.append(article)
    return filtered_articles

def inject_articles_into_html(articles, html_file):
    """
    Injects articles into the news container of the HTML file.
    """
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Generate the HTML for the news items
    news_items_html = ""
    for i, article in enumerate(articles):
        odd_or_even = "odd" if i % 2 == 0 else "even"
        news_items_html += f"""
        <div class="news-item {odd_or_even}">
            <h3 class="news-title">{article['title']}</h3>
            <p>{article['summary']}</p>
            <a href="{article['link']}" target="_blank">Read more</a>
        </div>
        """

    # Replace the existing news container content
    updated_html = html_content.replace(
        '<div class="news-container">',
        f'<div class="news-container">{news_items_html}'
    )

    # Write the updated HTML back to the file
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(updated_html)
    print(f"News content updated in {html_file}")

def main_script():
    # RSS feed URLs
    feed_urls = [
        "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
        "https://www.eia.gov/rss/todayinenergy.xml",
        "https://energytransferpartners.gcs-web.com/rss/news-releases.xml",
    ]

    # Keywords for filtering
    keywords = ["Trump", "solar", "wind", "renewable", "energy", "climate", "Inflation Reduction Act", "Transferability"]

    # Fetch and filter articles
    all_articles = fetch_from_multiple_feeds(feed_urls)
    filtered_articles = filter_articles_by_keywords(all_articles, keywords)

    if filtered_articles:
        print(f"Filtered {len(filtered_articles)} articles with keywords: {', '.join(keywords)}")
        for article in filtered_articles[:3]:  # Display the first 3 articles
            print(f"Title: {article['title']}")
            print(f"Summary: {article['summary']}")
            print(f"Link: {article['link']}")
            print("-" * 80)
        
        # Inject articles into the HTML
        inject_articles_into_html(filtered_articles, r"C:/Users/ykamel1/Documents/GitHub/webtech24f/tpvf/news.htm")
    else:
        print("No articles matched the keywords.")

if __name__ == "__main__":
    main_script()