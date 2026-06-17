import requests
from bs4 import BeautifulSoup
import re
import urllib.parse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
MAX_RESULTS = 5
CHUNK_SIZE = 500
TOP_CHUNKS = 3


def search_web(query: str) -> list[dict]:
    """Search DuckDuckGo and return a list of result URLs and titles."""
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Web search failed: {e}")

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.select(".result__body")[:MAX_RESULTS]:
        title_tag = result.select_one(".result__title")
        link_tag = result.select_one(".result__url")

        title = title_tag.get_text(strip=True) if title_tag else "Unknown"
        url_text = link_tag.get_text(strip=True) if link_tag else ""

        # Normalise URL
        if url_text and not url_text.startswith("http"):
            url_text = "https://" + url_text

        if url_text:
            results.append({"title": title, "url": url_text})

    return results


def scrape_page(url: str) -> str:
    """Scrape visible text from a webpage."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove noise tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return clean_text(text)
    except Exception:
        return ""


def clean_text(text: str) -> str:
    """Normalise whitespace and remove very short lines."""
    text = re.sub(r"\s+", " ", text)
    lines = [line.strip() for line in text.split(".") if len(line.strip()) > 40]
    return ". ".join(lines)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """Split text into overlapping chunks of approximately chunk_size words."""
    words = text.split()
    chunks = []
    overlap = chunk_size // 5

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk:
            chunks.append(chunk)

    return chunks


def retrieve_context(query: str) -> tuple[list[str], list[dict]]:
    """
    Run a web search for *query*, scrape the top results, chunk the text,
    and return (top_chunks, sources).
    """
    search_results = search_web(query)

    all_chunks: list[str] = []
    sources: list[dict] = []

    for result in search_results:
        page_text = scrape_page(result["url"])
        if not page_text:
            continue

        chunks = chunk_text(page_text)
        all_chunks.extend(chunks[:2])  # take up to 2 chunks per page
        sources.append(result)

    # Return a capped number of the most-relevant chunks (first = most relevant
    # in a simple keyword search scenario)
    top_chunks = all_chunks[:TOP_CHUNKS]
    return top_chunks, sources
