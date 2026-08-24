from playwright.sync_api import sync_playwright
from urllib.parse import quote

KEYWORD = "청소기"
TARGET_DOMAIN = "bestshop.lge.co.kr"

url = (
    "https://search.naver.com/search.naver?query="
    + quote(KEYWORD)
)

SELECTOR = "#power_link_body span.lnk_url_area > a"

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

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=30000
    )

    try:
        page.locator(SELECTOR).first.wait_for(
            state="attached",
            timeout=10000
        )
    except:
        print("파워링크를 찾지 못했습니다.")
        browser.close()
        exit()

    links = page.locator(SELECTOR)

    print()
    print("전체 광고 URL 개수:", links.count())
    print()

    # 일단 전체를 DOM 순서대로 출력
    print("===== DOM 순서 전체 =====")

    for i in range(links.count()):

        link = links.nth(i)

        text = link.inner_text().strip()

        print(
            f"DOM {i + 1}위 : {text}"
        )

    print("==========================")

    context.close()
    browser.close()
