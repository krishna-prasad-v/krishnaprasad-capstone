zero_shot_base_instruction = """
Extract "company", "role", and "years_experience_required" in valid JSON format 
from the <job_posting_snippet> below""" 



system_prompt = """You are an expert data extraction assistant.
Your task is to extract specific fields from <job_posting_snippet> and return them
as a single JSON object matching this exact schema:

...
JSON Schema:
{
  "type": "object",
  "properties": {
    "company": {
      "type": "string",
      "description": "The hiring company or organization name."
    },
    "role": {
      "type": ["string", "null"],
      "description": "The exact job title or role being hired for, or null if not stated."
    },
    "years_experience_required": {
      "type": ["integer", "null"],
      "description": "Minimum years of professional experience required as an integer, or null if unstated."
    }
  },
  "required": ["company", "role", "years_experience_required"]
}
...

Rules:
- Return ONLY the JSON object, with no preamble, explanation, or markdown code fences.
- All three fields are required in every response.
- If a field cannot be determined from the text, return null. Do not assume a value.
- "years_experience_required" must be an integer, not a string or range.
"""


cot_base_prompt =  """
You are an expert data extraction assistant.
Analyze <job_posting_snippet> step by step before answering:
1. Identify the hiring company name.
2. Identify the role or job title.
3. Identify the required years of experience:
   - Convert words to numbers (e.g. "five" -> 5).
   - If a range is given (e.g. "3-5 years"), take the minimum integer (3).
   - If no experience requirement is stated, use null.
First, briefly explain your step-by-step reasoning.
Then, conclude your response with the final extraction as a single valid JSON object with keys:
"company", "role", and "years_experience_required". Do not enclose the JSON string within any ``` markdown fences
"""