from playwright.sync_api import sync_playwright
from urllib.parse import quote

KEYWORD = "청소기"
TARGET_DOMAIN = "bestshop.lge.co.kr"

url = (
    "https://search.naver.com/search.naver?query="
    + quote(KEYWORD)
)

SELECTOR = (
    "#power_link_body > ul > "
    "li.lst.js-hover-item.type_sublink.ext_desc.type_subtitle "
    "> div.inner > div.title_url_area > div "
    "> span.lnk_url_area > a"
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

    print("파워링크 광고 개수:", links.count())
    print()

    print("===== 파워링크 TOP 5 =====")

    target_rank = None

    for i in range(min(links.count(), 5)):

        link = links.nth(i)

        text = link.inner_text().strip()

        print(f"{i + 1}위 : {text}")

        if TARGET_DOMAIN.lower().rstrip("/") == \
           text.lower().rstrip("/"):

            target_rank = i + 1

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
