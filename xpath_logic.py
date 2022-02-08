from bs4 import BeautifulSoup
from lxml import html
import aiohttp
import asyncio


async def get_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            return await response.text()


def get_course_links(html_string: str) -> list:
    tree = html.fromstring(html_string)
    course_links = tree.xpath("//*[contains(@href, '/p/')]/@href")
    return course_links


# time card data point is something of value but it is the main courses page
# TODO implement get_course_length into dictionary returned by parse_all_courses
def get_course_length(html_string: str):
    tree = html.fromstring(html_string)
    time_details = tree.xpath("//*[contains(@class, 'TimeDetails')]/text()")
    return time_details


def parse_all_courses(html_string: str) -> dict:
    tree = html.fromstring(html_string)
    modules_xpath = "//*[@class='block__curriculum__section__lock-icon']/ following-sibling :: text()" 
    modules = tree.xpath(modules_xpath)
    parsed_modules = [item.strip() for item in modules if not item == "\n  "]
    title = tree.xpath("//h1/b/text()")[0]
    instructors = tree.xpath("//p[@class='authors']/a/text()")
    return {
            'title': title,
            "modules": parsed_modules,
            "taught by": instructors
            } 


async def run_tasks(url, loop: asyncio.AbstractEventLoop):
    tasks = []
    async with aiohttp.ClientSession() as session:
        main_html = await get_html(url)
        course_links = set(get_course_links(main_html))
        for link in course_links:
            tasks.append(loop.create_task(get_html(link)))

        for task in tasks:
            html = await task
            course_data = parse_all_courses(html)
            print(course_data)


def main():
    url = "https://www.zerotomastery.io/courses"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks(url, loop))
    print("done")


if __name__ == "__main__":
    main()
