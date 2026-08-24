from playwright.sync_api import sync_playwright
from urllib.parse import quote

KEYWORD = "청소기"
TARGET_DOMAIN = "bestshop.lge.co.kr"

REGION = "부산진구 부전동"
LATITUDE = 35.1579
LONGITUDE = 129.0594

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
    print("키워드 :", KEYWORD)
    print("지역   :", REGION)

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=30000
    )

    try:
        page.locator("a.lnk_url").first.wait_for(
            state="attached",
            timeout=10000
        )
    except:
        print("파워링크를 찾지 못했습니다.")
        browser.close()
        exit()

    links = page.locator("a.lnk_url")

    print()
    print("===== 파워링크 TOP 5 =====")

    rank = 0
    target_rank = None
    seen_domains = set()

    for i in range(links.count()):

        link = links.nth(i)

        text = link.inner_text().strip()

        if not text:
            continue

        # 같은 광고의 중복 링크 방지
        domain = text.lower().rstrip("/")

        if domain in seen_domains:
            continue

        seen_domains.add(domain)

        rank += 1

        if rank > 5:
            break

        print(f"{rank}위 : {text}")

        if TARGET_DOMAIN.lower().rstrip("/") == domain:
            target_rank = rank

    print("==========================")

    if target_rank:
        print()
        print("===== 내 광고 =====")
        print("사이트 :", TARGET_DOMAIN)
        print("순위   :", target_rank)
        print("===================")
    else:
        print()
        print("===== 내 광고 =====")
        print("사이트 :", TARGET_DOMAIN)
        print("순위   : TOP 5 밖 또는 미노출")
        print("===================")

    context.close()
    browser.close()
