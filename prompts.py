from datetime import date
from utils import get_weekends_date

def build_prompt_generate_diary_json(
    start_date: date, end_date: date, content: str
) -> str:
    weekends_list:list[date] = get_weekends_date(start_date)
    weekends = str([str(d) for d in weekends_list])
    return f"""
You are an intern required to submit a professional internship diary.

You will receive:
- start_date
- end_date
- raw content (basic notes like tech stack, project tasks, blockers, etc.)
- holidays date on which you dont have to generate any tasks
Your task:

1. Generate a diary entry for EVERY date between start_date and end_date (inclusive).
2. DATE must be in format: YYYY-MM-DD.
3. Each date must be a JSON key.
4. Distribute the work logically across the dates.
5. Expand minimal raw content into professional diary language.

Writing Requirements:
- work_summary: 3-5 professional lines.
- learning_outcome: 2-3 clear lines.
- blockers_risks: 
    - If applicable → 1-2 lines.
    - If none → null.

Strict Rules:
- Output ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanation text.
- Do NOT include ```json.
- Ensure valid JSON formatting (double quotes, commas correct).
- All keys must be strings.
- Follow the exact structure below.
- Do NOT generate for holidays

start_date: {start_date}
end_date: {end_date}
content: {content}
holidays: {weekends}

Required JSON format:

{{
   "YYYY-MM-DD": {{
        "work_summary": "...",
        "learning_outcome": "...",
        "blockers_risks": "..." | null
   }}
}}
"""


def build_prompt_ask_questions(start_date: date, end_date: date):
    start_date = start_date.strftime("%d %b, %Y")
    end_date = end_date.strftime("%d %b, %Y")
    return f"""
Ask questions about what technology the student has learned in the on-going internship(start date: {start_date}, today_date: {end_date}).
Ask 4-5 (max 6) questions to extract the details from the student considering the dates above.

---
Based on the questions and answers provide the below details in the JSON FORMAT:
- Work Summary ()
- Learnings / Outcomes
- Blockers / Risks (leave blank if no)

GENERATE STRICT JSON IN THE BELOW FORMAT AT THE LAST:
{{
    "work_summary": str
    "learning_outcome": str
    "blockers_risks": str | null
}}
"""
