from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime


async def get_data_for_month(month_text, page, attendance_month, attendance_year, show_button):
    await page.select_option(attendance_month, label=month_text)
    await page.select_option(attendance_year, label='2022')
    await page.click(show_button)

    await page.is_visible('div#viewAttendanceMonthlyParent_wrapper')
    html = await page.inner_html('table#viewAttendanceMonthlyParent tbody')
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('td')
    grouped_data = [data[n:n + 5] for n in range(0, len(data), 5)]
    course = []

    for row in grouped_data:
        course.append([int(row[0].getText()), row[1].getText(), int(row[2].getText()), float(row[3].getText())])

    return course


async def run(playwright, username, password):
    browser = await playwright.chromium.launch(headless=False, slow_mo=1000)
    page = await browser.new_page()
    await page.goto('https://portal.svkm.ac.in/usermgmt/login')
    await page.fill('input#userName', username)
    await page.fill('input#userPwd', password)
    await page.click('input[type=submit]')

    failure_message_visible = await page.is_visible('p', timeout=2000)
    print(failure_message_visible)
    if failure_message_visible:
        return {"success": False, "data": "Please provide valid credentials"}

    await page.click('a[data-dismiss=modal]')
    await page.click('a[href="/SBM-NM-B/viewDailyAttendanceByStudent"]')

    attendance_month = 'select#attendanceMonth'
    attendance_year = 'select#attendanceYear'
    show_button = 'form a[onclick="showAttendanceSummaryByMonthAndYear()"]'
    await page.wait_for_selector(attendance_month, state="attached")
    await page.wait_for_selector(attendance_year, state="attached")
    await page.is_visible(show_button)

    current_month = datetime.now().month
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'July',
                  8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    current_month_text = month_dict[current_month]

    await page.select_option(attendance_month, label=current_month_text)
    await page.select_option(attendance_year, label=str(datetime.now().year))
    await page.click(show_button)

    await page.is_visible('div#viewAttendanceMonthlyParent_wrapper')
    html = await page.inner_html('table#viewAttendanceMonthlyParent tbody')
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all('td')
    grouped_data = [data[n:n + 5] for n in range(0, len(data), 5)]
    course = []
    for row in grouped_data:
        course.append([int(row[0].getText()), row[1].getText(), int(row[2].getText()), float(row[3].getText())])

    current_month_data = await get_data_for_month(current_month_text, page, attendance_month,
                                                  attendance_year, show_button)
    last_month_data = await get_data_for_month(month_dict[current_month - 1], page, attendance_month,
                                               attendance_year, show_button)
    previous_month_data = await get_data_for_month(month_dict[current_month - 2], page, attendance_month,
                                                   attendance_year, show_button)

    json_list = []
    for idx, course in enumerate(current_month_data):
        total_classes = course[2] + last_month_data[idx][2] + previous_month_data[idx][2]
        lecture_attended = course[3] + last_month_data[idx][3] + previous_month_data[idx][3]

        attended_dict = {"lecture_attended": str(int(lecture_attended)), "total_classes": str(total_classes)}
        course_dict = {course[1]: attended_dict}
        json_list.append(course_dict)

    return json_list


async def main(username, password):
    async with async_playwright() as playwright:
        return await run(playwright, username, password)

