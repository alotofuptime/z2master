import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


'''
The code below has turned out be ineffecient and a bit overengineered. It has come to my attention that browser automation will not be necessary to grab the desired data. This file will be changed to implement a different feature of the app. See xpath_logic.py for the new implementation of the web scraping portion below. Playwright and BeautifulSoup will no longer be used. Playwright is simply no longer needed & BeautifulSoup is not to my liking since it isn't xpath compatible.
'''
url = "https://zerotomastery.io/courses/"

async def main():
    html = await course_page_html(url)
    links = get_course_links(html)
    parsed_data = await parse_course_links(links)
    print(parsed_data)


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
    curriculum = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        for url in urls:
            await page.goto(url)
            title = await page.query_selector("//h1")
            show_all_xpath = '//*[@class="block__curriculum__view-all-lectures-btn"]'
            show_all_btn = await page.query_selector(show_all_xpath)
            if show_all_btn:
                await show_all_btn.click()
            titles.append(await title.inner_text())
            sections_xpath = '//*[@class="block__curriculum__section__lock-icon"]/ following-sibling :: text() '
            sections = await page.locator(sections_xpath)
                # curriculum.append(sec.inner_text())
            # await page.wait_for_timeout(1000)
            break
        return sections, type(sections)



if __name__ == "__main__":
    asyncio.run(main())
