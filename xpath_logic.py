from bs4 import BeautifulSoup
from lxml import html
import aiohttp
import asyncio


async def get_html(link: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            assert response.status == 200
            return await response.text()
            # html = await response.text()


def get_course_links(html_string: str) -> list:
    tree = html.fromstring(html_string)
    courses = tree.xpath("//*[contains(@href, '/p/')]/@href")
    return courses


def parse_course_page(html_string: str) -> dict:
    tree = html.fromstring(html_string)
    modules_xpath = "//*[@class='block__curriculum__section__lock-icon']/ following-sibling :: text()" 
    modules = tree.xpath(modules_xpath)
    parsed_modules = [item.strip() for item in modules if not item == "\n  "]
    title = tree.xpath("//h1/b/text()")[0]
    return {
            'title': title,
            "modules": parsed_modules
            } 


async def run_tasks(loop: asyncio.AbstractEventLoop):
    tasks = []
    url = "https://www.zerotomastery.io/courses"
    async with aiohttp.ClientSession() as session:
        main_html = await get_html(url)
        course_links = set(get_course_links(main_html))
        for link in course_links:
            tasks.append(loop.create_task(get_html(link)))

        for task in tasks:
            html = await task
            course_data = parse_course_page(html)
            print(course_data)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks(loop))
    print("done")


if __name__ == "__main__":
    main()
