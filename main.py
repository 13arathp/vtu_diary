from config import settings
from datetime import datetime, date
from ai import GeminiService
from prompts import build_prompt_generate_diary_json
import json
from pathlib import Path

def input_dates() -> tuple[date, date]:
    """Extract & Return start date and end date"""
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    end_date_str = input("Enter the end date (YYYY-MM-DD): ")

    format_string = "%Y-%m-%d"

    start_date: date = datetime.strptime(start_date_str, format_string).date()
    end_date: date = datetime.strptime(end_date_str, format_string).date()

    return start_date, end_date



def generate_ai_response(start_date, end_date, content):
    prompt = build_prompt_generate_diary_json(start_date, end_date, content)
    # print("logger: prompt: ", prompt)
    gemini_service = GeminiService()
    response = gemini_service.get_response(prompt)
    return response



def main():
    start_date, end_date = date(2025, 10, 6), date(2025, 10, 15) # input_dates()
    internship_details_file = f"{str(start_date)}_{str(end_date)}_internship_details.json"
    if not Path(internship_details_file).is_file():
        print(f"logger: dates: {start_date}, {end_date}")
        content = open("content.txt", "r").read()
        response = generate_ai_response(start_date, end_date, content)
        json_data = json.loads(response)
        with open(internship_details_file, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4)
            print("json dumped!!", internship_details_file)
    else:
        with open(internship_details_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        
    holidays_file = f"{str(start_date)}_{str(end_date)}_holidays.json"
    if not Path(holidays_file).is_file():
        from utils import get_weekends_date
        holidays = get_weekends_date(start_date)
        holidays_str_list = [str(d) for d in holidays]
        holidays_dict = {"holidays": holidays_str_list}
        with open(holidays_file, "w", encoding="utf-8") as file:
            json.dump(holidays_dict, file, indent=4)
            print("json dumped!!", holidays_file)
        
    

if __name__ == "__main__":
    main()
