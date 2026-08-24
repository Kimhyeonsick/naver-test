from playwright.sync_api import sync_playwright
from urllib.parse import quote
import re
import time

KEYWORD = "청소기"
TARGET_DOMAIN = "bestshop.lge.co.kr"

LATITUDE = 35.1543
LONGITUDE = 126.9022

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

    links = page.locator("a.lnk_url")

    print("lnk_url 개수:", links.count())

    found = False

    for i in range(links.count()):

        link = links.nth(i)

        onclick = link.get_attribute("onclick")
        text = link.inner_text().strip()

        if not onclick:
            continue

        # amp;r=숫자 추출
        match = re.search(
            r'(?:&amp;|&)r=(\d+)',
            onclick
        )

        if not match:
            continue

        rank = int(match.group(1))

        # 사이트 확인
        if TARGET_DOMAIN.lower() in text.lower():

            print()
            print("===== 광고 발견 =====")
            print("키워드 :", KEYWORD)
            print("사이트 :", TARGET_DOMAIN)
            print("순위   :", rank)
            print("====================")

            found = True
            break

    if not found:
        print()
        print("광고를 찾지 못했습니다.")
        print("키워드 :", KEYWORD)
        print("사이트 :", TARGET_DOMAIN)

    browser.close()
