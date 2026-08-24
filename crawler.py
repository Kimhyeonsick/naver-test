from playwright.sync_api import sync_playwright
from urllib.parse import quote
import re

KEYWORD = "청소기"
TARGET_DOMAIN = "bestshop.lge.co.kr"

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

    for region in REGIONS:

        print()
        print("================================")
        print("지역 :", region["name"])
        print(
            "좌표 :",
            region["latitude"],
            region["longitude"]
        )
        print("================================")

        context = browser.new_context(
            geolocation={
                "latitude": region["latitude"],
                "longitude": region["longitude"]
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
            timeout=30000
        )

        try:
            page.locator(
                "a.lnk_url"
            ).first.wait_for(
                state="attached",
                timeout=10000
            )
        except:
            print("파워링크를 찾지 못했습니다.")
            context.close()
            continue

        links = page.locator("a.lnk_url")

        target_rank = None

        print()
        print("===== 파워링크 TOP 5 =====")

        for i in range(links.count()):

            link = links.nth(i)

            onclick = link.get_attribute("onclick")
            text = link.inner_text().strip()

            if not onclick:
                continue

            match = re.search(
                r'(?:&amp;|&)r=(\d+)',
                onclick
            )

            if not match:
                continue

            rank = int(match.group(1))

            if rank > 5:
                continue

            print(f"{rank}위 : {text}")

            if TARGET_DOMAIN.lower() in text.lower():
                target_rank = rank

        print("==========================")

        if target_rank:
            print(
                "내 광고 :",
                TARGET_DOMAIN,
                "→",
                target_rank,
                "위"
            )
        else:
            print(
                "내 광고 :",
                TARGET_DOMAIN,
                "→ TOP 5 밖 또는 미노출"
            )

        context.close()

    browser.close()
