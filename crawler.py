from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

KEYWORD = "청소기"

# 부산진구 부전동 테스트 좌표
LATITUDE = 35.1543
LONGITUDE = 126.9022

url = (
    "https://search.naver.com/search.naver?query="
    + quote(KEYWORD)
)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    context = browser.new_context(
        geolocation={
            "latitude": LATITUDE,
            "longitude": LONGITUDE
        },
        permissions=["geolocation"],
        locale="ko-KR",
        timezone_id="Asia/Seoul"
    )

    page = context.new_page()

    print("네이버 접속...")
    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    time.sleep(3)

    print("제목:", page.title())
    print("URL:", page.url)

    html = page.content()

    print("HTML 크기:", len(html))

    # BeautifulSoup
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    print("\n===== 검색 결과 =====")

    count = 0

    for tag in soup.find_all(["a", "h2", "h3"]):

        text = tag.get_text(
            " ",
            strip=True
        )

        if not text:
            continue

        if len(text) < 2:
            continue

        print(text[:200])

        count += 1

        if count >= 30:
            break

    # HTML 저장
    with open(
        "naver_result.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    print("\nHTML 저장 완료")

    browser.close()
