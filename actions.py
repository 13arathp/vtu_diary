from playwright.sync_api import sync_playwright, Page, BrowserContext, Browser
from pathlib import Path
from config import settings
from datetime import date, datetime
import json
def run_actions(current_date: date, data):
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        
        if Path("state.json").is_file():
            print("Context exist")
            context: BrowserContext = browser.new_context(storage_state="state.json")
        else:
            context: BrowserContext = browser.new_context()
                
        page: Page = context.new_page()

        page.goto("https://vtu.internyet.in/dashboard/student", wait_until="networkidle")

        if "sign-in" in page.url:
            login(page, context)
        
        pop_up = page.get_by_role("button", name="I Understand")
        if pop_up.is_visible():
            pop_up.click()
        
        open_diary_page(page, current_date)
        create_diary_entry(page, data)
        page.wait_for_timeout(10000)
        browser.close()
    

def login(page: Page, context: BrowserContext):
    try:
        page.get_by_placeholder("Enter your email address").fill(settings.VTU_EMAIL)
        page.get_by_placeholder("Enter your password").fill(settings.VTU_PASSWORD)
        page.get_by_role("button", name="Sign In").click()
        page.wait_for_url("**/dashboard/student", timeout=5000)
        context.storage_state(path="state.json")
        print("Login successful, state saved.")
    except Exception as e:
        print(f"exception: {e}")


def open_diary_page(page: Page, date: date):
    try:
        if date.weekday() >= 5:
            print("skipping dairy_fill on weekends")
            return
        page.goto("https://vtu.internyet.in/dashboard/student/student-diary", wait_until="networkidle")
        page.locator("#internship_id").click()
        page.keyboard.press('Enter')
        page.get_by_text("Pick a Date").click()
        page.locator('select[aria-label="Choose the Year"]').select_option(str(date.year))
        page.locator('select[aria-label="Choose the Month"]').select_option(str(date.month - 1))
        page.locator(f'td[data-day="{str(date)}"]').click()
        page.get_by_role("button", name="Continue").click()
    except Exception as e:
        print(f"exception: {e}")

    

def create_diary_entry(page: Page, data):
    work_summary = data["work_summary"]
    learning_outcome = data["learning_outcome"]
    blockers_risks = data["blockers_risks"] if data["blockers_risks"] else ""
    skills =  data["skills"]
    page.get_by_placeholder("Briefly describe the work you did today…").fill(work_summary)
    page.get_by_placeholder("e.g. 6.5").fill(str(settings.DAILY_WORK_HRS))
    page.get_by_placeholder("What did you learn or ship today?").fill(learning_outcome)
    page.get_by_placeholder("Anything that slowed you down?").fill(blockers_risks)
    page.get_by_placeholder("Briefly describe the work you did today…").fill(work_summary)
    
    page.wait_for_timeout(1000)
    page.locator(".react-select__value-container").click()
    page.wait_for_timeout(100)
    page.wait_for_selector(".react-select__option")

    all_skills = page.locator(".react-select__option").all_inner_texts()

    for skill in skills:
        if skill in all_skills:
            page.get_by_text(skill).click()
            page.locator(".react-select__value-container").click()
            page.wait_for_timeout(100)
    
    page.wait_for_timeout(300)
    page.get_by_role("button", name="Save").click()

    



def main():
    
    start_date, end_date = date(2025, 10, 6), date(2025, 10, 15) # input_dates()
    internship_details_file = f"{str(start_date)}_{str(end_date)}_internship_details.json"
    holidays_file = f"{str(start_date)}_{str(end_date)}_holidays.json"
    
    with open(internship_details_file, 'r') as f1, open(holidays_file, 'r') as f2:
        internship_details_data = json.load(f1)
        holiday_data = json.load(f2)
        for date_str, data in internship_details_data.items():
            if date_str in holiday_data["holidays"]:
                continue
            run_actions(datetime.strptime(date_str, '%Y-%m-%d').date(), data)




if __name__ == "__main__":
    main()