from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
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

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=30000
    )

    # HTML만 가져옴
    html = page.content()

    browser.close()


# BeautifulSoup으로 파싱
soup = BeautifulSoup(
    html,
    "html.parser"
)

# 파워링크 영역
power_link = soup.select_one(
    "#power_link_body"
)

if not power_link:
    print("파워링크 영역을 찾지 못했습니다.")
    exit()


# 광고 컨테이너
ads = power_link.select(
    "ul > li"
)

print("광고 컨테이너:", len(ads))
print()

rank = 0
target_rank = None

print("===== 파워링크 TOP 5 =====")

for ad in ads:

    url_tag = ad.select_one(
        "span.lnk_url_area > a"
    )

    if not url_tag:
        continue

    site = url_tag.get_text(
        strip=True
    )

    if not site:
        continue

    rank += 1

    if rank > 5:
        break

    print(
        f"{rank}위 : {site}"
    )

    if (
        site.lower().rstrip("/")
        == TARGET_DOMAIN.lower().rstrip("/")
    ):
        target_rank = rank

print("==========================")

print()

if target_rank:
    print("사이트 :", TARGET_DOMAIN)
    print("순위   :", target_rank)
else:
    print("사이트 :", TARGET_DOMAIN)
    print("순위   : TOP 5 밖 또는 미노출")
