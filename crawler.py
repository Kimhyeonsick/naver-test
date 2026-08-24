from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import re

KEYWORD = "청소기"

# 부산진구 부전동 테스트 좌표
LATITUDE = 35.1543
LONGITUDE = 126.9022

TARGET_DOMAIN = "bestshop.lge.co.kr"

url = (
    "https://search.naver.com/search.naver?query="
    + quote(KEYWORD)
)

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

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

    # lnk_url 클래스만 검색
    links = page.locator("a.lnk_url")

    print("lnk_url 개수:", links.count())

    for i in range(links.count()):

        link = links.nth(i)

        href = link.get_attribute("href")
        onclick = link.get_attribute("onclick")
        text = link.inner_text().strip()

        if not onclick:
            continue

        # amp;r=숫자 추출
        match = re.search(r'(?:&amp;|&)r=(\d+)', onclick)

        if not match:
            continue

        rank = int(match.group(1))

        print(
            f"순위: {rank} | "
            f"사이트: {text} | "
            f"href: {href}"
        )

        # 내가 찾는 사이트인지 확인
        if TARGET_DOMAIN in (href or "") or TARGET_DOMAIN in text:

            print()
            print("===== 광고 발견 =====")
            print("키워드 :", KEYWORD)
            print("사이트 :", TARGET_DOMAIN)
            print("순위   :", rank)
            print("====================")

            break

    browser.close()
