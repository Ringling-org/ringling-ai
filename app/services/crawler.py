import requests
from bs4 import BeautifulSoup

def crawl_page(url: str, timeout: int = 10) -> dict[str, str] | None:
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, 'html.parser')
        # title = next(soup.stripped_strings, "제목 없음")
        title = extract_title(soup)
        # script/style 제거
        for tag in soup(["script", "style"]):
            tag.decompose()

        content = soup.get_text(separator="\n", strip=True)[:2000]
        return {"title": title, "content": content}

    except requests.exceptions.RequestException as e:
        print(f"[crawl_page] 요청 오류: {e}")
        return None
    except Exception as e:
        print(f"[crawl_page] 크롤링 중 오류 발생: {e}")
        return None

def extract_title(soup: BeautifulSoup) -> str:
    if (meta := soup.find("meta", property="og:title")):
        return meta.get("content", "").strip()

    if soup.title and soup.title.string:
        return soup.title.string.strip()

    if (h1 := soup.find("h1")):
        return h1.get_text(strip=True)

    return "제목 없음"
