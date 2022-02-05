import asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


# TODO rename course_page_html
# TODO create function to navigate all links returned by get_course_links
# TODO extract course title, outline, & what you'll learn sections
# TODO create ztm api to store extracted data
# TODO create even loop

url = "https://zerotomastery.io/courses/"

async def main():
    html = await course_page_html(url)
    links = get_course_links(html)
    course_titles = await parse_course_links(links)
    print(course_titles)


async def course_page_html(start_url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(start_url)
        html = await page.content()
        await browser.close()
        return html


def get_course_links(html: str) -> set:
    href_set = set()
    soup = BeautifulSoup(html, "html.parser")
    course_links = soup.find_all("a")
    for a_tag in course_links:
        href = a_tag.get("href")
        if "/p/" in str( href ):
            href_set.add(href)
    return href_set


async def parse_course_links(urls: set) -> list:
    titles = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        for url in urls:
            await page.goto(url)
            title_xpath = "//h1" 
            title = await page.query_selector(title_xpath)
            titles.append(await title.inner_text())
        return titles



if __name__ == "__main__":
    asyncio.run(main())
