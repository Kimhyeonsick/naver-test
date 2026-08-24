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

    # 지역 설정 없이 일반 브라우저
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
            "a.lnk_url"
        ).first.wait_for(
            state="attached",
            timeout=10000
        )
    except:
        print("파워링크를 찾지 못했습니다.")
        browser.close()
        exit()

    links = page.locator("a.lnk_url")

    print("lnk_url 개수:", links.count())
    print()

    print("===== 파워링크 TOP 5 =====")

    target_rank = None
    rank = 0
    seen = set()

    for i in range(links.count()):

        link = links.nth(i)

        text = link.inner_text().strip()

        if not text:
            continue

        domain = text.lower().rstrip("/")

        # 일단 동일 URL 중복 제거
        if domain in seen:
            continue

        seen.add(domain)

        rank += 1

        if rank > 5:
            break

        print(f"{rank}위 : {text}")

        if domain == TARGET_DOMAIN.lower().rstrip("/"):
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
