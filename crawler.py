from playwright.sync_api import sync_playwright
from urllib.parse import quote
import re

KEYWORD = "청소기"
TARGET_DOMAIN = "bestshop.lge.co.kr"

# 테스트 지역
REGIONS = [
    {
        "name": "부산 부산진구 부전동",
        "latitude": 35.1579,
        "longitude": 129.0594
    },
    {
        "name": "광주 서구 양동",
        "latitude": 35.1497,
        "longitude": 126.9020
    },
    {
        "name": "서울 마포구 서교동",
        "latitude": 37.5550,
        "longitude": 126.9220
    }
]

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
    print("키워드 :", KEYWORD)
    print("지역   :", REGION)
    print("좌표   :", LATITUDE, LONGITUDE)

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=30000
    )

    # 고정 sleep 대신 광고 링크가 나타날 때까지 대기
    try:
        page.locator("a.lnk_url").first.wait_for(
            state="attached",
            timeout=10000
        )
    except:
        print("파워링크 광고를 찾지 못했습니다.")
        browser.close()
        exit()

    links = page.locator("a.lnk_url")

    print()
    print("===== 파워링크 TOP 5 =====")

    target_rank = None
    count = 0

    for i in range(links.count()):

        link = links.nth(i)

        onclick = link.get_attribute("onclick")
        text = link.inner_text().strip()

        if not onclick:
            continue

        # amp;r=숫자
        match = re.search(
            r'(?:&amp;|&)r=(\d+)',
            onclick
        )

        if not match:
            continue

        rank = int(match.group(1))

        # 1~5위만 출력
        if rank > 5:
            continue

        print(f"{rank}위 : {text}")

        # 내가 찾는 도메인
        if TARGET_DOMAIN.lower() in text.lower():

            target_rank = rank

    print("==========================")

    print()

    if target_rank:
        print("===== 내 광고 =====")
        print("사이트 :", TARGET_DOMAIN)
        print("순위   :", target_rank)
        print("===================")
    else:
        print("===== 내 광고 =====")
        print("사이트 :", TARGET_DOMAIN)
        print("순위   : TOP 5 밖 또는 미노출")
        print("===================")

    browser.close()
