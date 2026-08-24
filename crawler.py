from playwright.sync_api import sync_playwright
from urllib.parse import quote

KEYWORD = "청소기"
TARGET_DOMAIN = "bestshop.lge.co.kr"

url = (
    "https://search.naver.com/search.naver?query="
    + quote(KEYWORD)
)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    context = browser.new_context(
        locale="ko-KR",
        timezone_id="Asia/Seoul"
    )

    page = context.new_page()

    print("네이버 접속...")
    print("키워드 :", KEYWORD)

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=30000
    )

    try:
        page.locator(
            "span.lnk_url_area"
        ).first.wait_for(
            state="attached",
            timeout=10000
        )
    except:
        print("파워링크를 찾지 못했습니다.")
        browser.close()
        exit()

    areas = page.locator("span.lnk_url_area")

    print("lnk_url_area 개수:", areas.count())
    print()

    print("===== 파워링크 TOP 5 =====")

    target_rank = None

    for i in range(areas.count()):

        area = areas.nth(i)

        link = area.locator("a.lnk_url")

        if link.count() == 0:
            continue

        text = link.first.inner_text().strip()

        if not text:
            continue

        rank = i + 1

        if rank > 5:
            break

        print(f"{rank}위 : {text}")

        if TARGET_DOMAIN.lower().rstrip("/") == \
           text.lower().rstrip("/"):
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

    context.close()
    browser.close()
