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


# time card data point is something of value but it is on the main courses page
# TODO fix title mismatch in parse_all_courses only Complete Web Dev course is matching


def get_course_length(html_string: str):
    tree = html.fromstring(html_string)
    course_length = {}
    content_divs = tree.xpath("//*[contains(@class, '__ContentContainer')]")
    for div in content_divs:
        time_details = div.xpath("./span[contains(@class, 'TimeDetails')]/text()")
    # title is needed again here to determine which course the time_details data point applies
        title = div.xpath("./a/text()")[0]
    # return course_length
        hours = float(time_details[0])
        lessons = int(time_details[2])
        course_length[title] = {
                "hours": hours,
                "lessons": lessons
                } 
        return course_length


def parse_all_courses(course_url: str, main_url) -> dict:
    tree = html.fromstring(course_url)
    modules_xpath = "//*[@class='block__curriculum__section__lock-icon']/ following-sibling :: text()"
    modules = tree.xpath(modules_xpath)
    parsed_modules = [item.strip() for item in modules if not item == "\n  "]
    title = tree.xpath("//h1/b/text()")[0]
    instructors = tree.xpath("//p[@class='authors']/a/text()")
    content_quanity = get_course_length(main_url)
    course_content = {
            'title': title,
            "modules": parsed_modules,
            "taught by": instructors
            }
    if content_quanity.get(title, None):
        course_content["hours"] = content_quanity[title]["hours"]
        course_content["lessons"] = content_quanity[title]["lessons"]
    else:
        return "Title mismatch in parse_all_courses"

    return course_content


async def run_tasks(url, loop: asyncio.AbstractEventLoop):
    tasks = []
    async with aiohttp.ClientSession() as session:
        main_html = await get_html(url)
        course_links = set(get_course_links(main_html))
        for link in course_links:
            tasks.append(loop.create_task(get_html(link)))

        for task in tasks:
            html = await task
            course_data = parse_all_courses(html, main_html)
            # course_time = get_course_length(main_html)
            print(course_data)


def main():
    url = "https://www.zerotomastery.io/courses"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tasks(url, loop))
    print("done")


if __name__ == "__main__":
    main()
