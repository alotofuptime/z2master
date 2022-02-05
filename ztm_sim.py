import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


# TODO rename course_page_html
# TODO create function to navigate all links returned by get_course_links
# TODO extract course title, outline, & what you'll learn sections
# TODO create ztm api to store extracted data
async def main():
    html = await course_page_html()
    links = get_course_links(html)
    print(links)


async def course_page_html() -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://zerotomastery.io/courses/")
        html = await page.content()
        await browser.close()
        return html


def get_course_links(html: str) -> set:
    href_set = set()
    soup = BeautifulSoup(html, "html.parser")
    course_links = soup.find_all("a")
    for a_tag in course_links:
        href = link.a_tag("href")
        if "/p/" in str( href ):
            href_set.add(href)
    return href_set


if __name__ == "__main__":
    asyncio.run(main())
