import asyncio
import json
import os
import sys
import time
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from openai import AsyncOpenAI
from prompts import zero_shot_base_instruction, system_prompt, cot_base_prompt
# from tabulate import tabulate
load_dotenv()

# Make sure OPENAI_API_KEY is set in the environment
assert os.environ.get('OPENAI_API_KEY'), 'Set OPENAI_API_KEY first'

# Synchronous client configured with Vocareum base_url
client = AsyncOpenAI()

MODEL = "gpt-4o-mini"
JUDGE_MODEL = "gpt-4o"
TEMPERATURE = 0.0

print('\nSetup complete.')

# Load the data
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

try:
    job_snippets = [json.loads(line) for line in (DATA_DIR / "job_snippets.jsonl").read_text().splitlines() if line.strip()]
    golden = {row["id"]: row for row in (json.loads(line) for line in (DATA_DIR / "golden_set.jsonl").read_text().splitlines() if line.strip())}
except Exception as e:
    print(f"Exception: {str(e)}")
    sys.exit(1)

print(f"\nLoaded {len(job_snippets)} snippets, {len(golden)} golden entries.")

#********************************************************************************************
# prompt function - zero-shot
#********************************************************************************************
def prompt_zero_shot(snippet_text: str) -> list[dict]:
    """Strategy 1 — zero-shot. Just ask, no examples, no persona."""

    prompt = f"""
             {zero_shot_base_instruction}
            <job_posting_snippet>
            {snippet_text}
            </job_posting_snippet>
            """
    return [{"role": "user", "content": prompt}]

#********************************************************************************************
# prompt function - few-shot
#********************************************************************************************
def prompt_few_shot(snippet_text: str) -> list[dict]:    
    messages = []
# Few-shot example - 1  
    message_dict = { 
        "role" : "user",
        "content" : f"""
                    {zero_shot_base_instruction}
                    <job_posting_snippet>
                    Acme Corp is hiring a Senior Software Engineer to join our platform team. The ideal candidate has 5+ years of backend development experience and strong skills in Python and distributed systems.
                    </job_posting_snippet>
                    """            }
    messages.append(message_dict)
  
    message_dict = { "role" : "assistant",
                     "content": '{"company": "Acme Corp", "role": "Senior Software Engineer", "years_experience_required": 5}'   
                   }

    messages.append(message_dict)

# Few-shot example - 2
    message_dict = { 
        "role" : "user",
        "content" : f"""
                    {zero_shot_base_instruction}
                    <job_posting_snippet>
                    Stark Industries: Cybersecurity Analyst (mid-level). Three to five years in a SOC environment or equivalent. Familiarity with SIEM tools, incident response runbooks, and basic threat modelling.
                    </job_posting_snippet>
                    """            }
    messages.append(message_dict)

    message_dict = { "role" : "assistant",
                     "content": '{"company": "Stark Industries", "role": "Cybersecurity Analyst", "years_experience_required": 3}'   
                   }

    messages.append(message_dict)

# Actual job snippet
    prompt = f"""
            {zero_shot_base_instruction}
            <job_posting_snippet>
            {snippet_text}
            </job_posting_snippet>
            """
    message_dict = { "role" : "user",
                     "content": prompt}

    messages.append(message_dict)

    return messages    

#********************************************************************************************
# prompt function - structured with persona and JSON schema
#********************************************************************************************
def prompt_structured(snippet_text: str) -> list[dict]:
    """Strategy 3 — structured / role-based. Use a system prompt with a persona and explicit JSON schema."""
    
    messages = []
    message_dict =  { 
                    "role" : "system",
                    "content": system_prompt   }
    
    messages.append(message_dict)

    prompt = f"""
             {zero_shot_base_instruction}
             <job_posting_snippet>
             {snippet_text}
             </job_posting_snippet>
             """
    
    message_dict = { 
                   "role" : "user",
                   "content": prompt }

    messages.append(message_dict)
    return messages

#********************************************************************************************
# prompt function - chanin-of-thought
#********************************************************************************************
def prompt_cot(snippet_text: str) -> list[dict]:
    """Strategy 4 — chain-of-thought. Ask the model to reason before answering."""
    messages = []

    prompt = f"""
             {cot_base_prompt}
             <job_posting_snippet>
             {snippet_text}
             </job_posting_snippet>
             """

    message_dict = { 
                    "role" : "user",
                    "content": prompt }
    
    messages.append(message_dict)
    return messages

STRATEGIES = {
    'zero_shot': prompt_zero_shot,
    'few_shot': prompt_few_shot,
    'structured': prompt_structured,
    'cot': prompt_cot,
}

#********************************************************************************************
# parse_response
#********************************************************************************************
def parse_response(text: str) -> dict | None:
    """Try to parse a JSON object out of the model's response. Return None if it doesn't parse.
    
    Hint: models sometimes wrap JSON in ```json ... ``` fences. Strip them first.
    """
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end]), True
    except ValueError:
        return None, False
#********************************************************************************************
# calculate cost
#********************************************************************************************            
def calculate_cost( token_count_in, token_count_out, model) -> float:
    match model:
        case "claude-haiku-4-5-20251001":
            usd_per_m_input, usd_per_m_output = 1.00, 5.00
        case "claude-sonnet-5":
            usd_per_m_input, usd_per_m_output = 2.00, 10.00
        case "claude-opus-5":
            usd_per_m_input, usd_per_m_output = 5.00, 25.00
        case "gpt-4o-mini":
            usd_per_m_input, usd_per_m_output = 0.15, 0.60
        case "gpt-4o":
            usd_per_m_input, usd_per_m_output = 2.50, 10.00
        case _:  # Default / WHEN OTHERS
            raise ValueError(f"Unknown or unsupported model: {model}")    

    cost = (token_count_in * usd_per_m_input + token_count_out * usd_per_m_output) / 1_000_000
    return cost

#********************************************************************************************
# calculate accuracy score for a snippet
#********************************************************************************************
def score_accuracy(extracted: dict | None, gold: dict) -> int:
    """Compare 3 fields. Case-insensitive, whitespace-trimmed for strings. Return 0, 1, 2, or 3."""
    if not extracted or not isinstance(extracted, dict):
        return 0
    
    score = 0

    # Get all the values first, so the comparisons below are easier to read
    extracted_company = extracted.get("company")
    gold_company = gold.get("company")

    extracted_role = extracted.get("role")
    gold_role = gold.get("role")

    ext_years = extracted.get("years_experience_required")
    gold_years = gold.get("years_experience_required")

    # 1. Check "company"
    if extracted_company is None and gold_company is None:
        score = score + 1
    else:
        if extracted_company is not None and gold_company is not None:
            if extracted_company.strip().lower() == gold_company.strip().lower():
                score = score + 1

    # 2. Check "role"
    if extracted_role is None and gold_role is None:
        score = score + 1
    else:
        if extracted_role is not None and gold_role is not None:
            if extracted_role.strip().lower() == gold_role.strip().lower():
                score = score + 1

    # 3. Check "years_experience_required"
    # assumption  gold_years is always a clean, valid integer.
    if ext_years is None and gold_years is None:
        score = score + 1
    else:
        if ext_years is not None and gold_years is not None:
            try:
                if int(ext_years) == gold_years:
                    score = score + 1
            except:
                # ext_years couldn't be converted to a number, so it's not a match
                pass

    return score
    
#********************************************************************************************
# run_one
#******************************************************************************************** 
async def run_one(strategy_name: str, snippet: dict) -> dict:
    """Run one strategy on one snippet. Return a dict with all the captured fields."""
    prompt_func = STRATEGIES[strategy_name]

    snippet_text = snippet["snippet"]

    messages = prompt_func(snippet_text)

    start_time = time.perf_counter()

    try:
        response = await client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE,
            max_completion_tokens=1000,
            messages=messages   )

        latency_s = time.perf_counter() - start_time

        cost_usd = calculate_cost(
                token_count_in=response.usage.prompt_tokens,
                token_count_out=response.usage.completion_tokens,
                model=MODEL      )
        
        raw_text = response.choices[0].message.content
        
        if not raw_text:
            raw_text = None
            accuracy = 0
            judge_accuracy = 0
        else:
            parsed_dict, parse_success = parse_response(raw_text)
            gold = golden[ snippet["id"] ]
            accuracy = score_accuracy(extracted=parsed_dict, gold=gold)
            judge_accuracy = await score_llm_judge(snippet_text=snippet_text, extracted=parsed_dict, gold=gold)
        
        return {
                "strategy": strategy_name,
                "snippet_id": snippet["id"],
                "raw_response": raw_text,
                "extracted": parsed_dict,  # parsed dict or None
                "parse_success": parse_success,  # True or False (used in Step 4 evaluation!)
                "latency_s": latency_s,
                "cost_usd": cost_usd,
                "accuracy": accuracy,
                "llm_judge_score": judge_accuracy
                }
    
    except Exception as e:
        raise  

#********************************************************************************************
# score from judge llm
#******************************************************************************************** 
async def score_llm_judge(snippet_text: str, extracted: dict | None, gold: dict) -> int:
    """Use gpt-4o as a judge. Return integer 1-4.
    
    Rubric (suggested):
      3 — all three fields correct
      2 — two of three correct, no fabricated data
      1 — one of three correct, or fabricated a field
      0 — none correct or unparsable
    """

    if not extracted or not isinstance(extracted, dict):
      return 0

    prompt = f"""
            You are an expert evaluator grading a data extraction model.
            Original Job Snippet:
            {snippet_text}

            Ground Truth (Gold):
            - Company: {gold.get('company')}
            - Role: {gold.get('role')}
            - Years of Experience: {gold.get('years_experience_required')}

            LLM Extracted Data:
            - Company: {extracted.get('company')}
            - Role: {extracted.get('role')}
            - Years Experience: {extracted.get('years_experience_required')}

            Judging Rules:
            - Years of experience extracted by LLM must be strictly an integer or None. Otherwise, the match is failed, return 0 for this field.

            Scoring Rubric:
            3: All three fields are correct.
            2: Two of three fields are correct, and no data was fabricated.
            1: Only one field is correct, OR a field was fabricated (hallucinated).
            0: None of the fields are correct.
            Respond with ONLY a single digit integer: 0, 1, 2, or 3.
            """
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=10,
        )
        raw_score = response.choices[0].message.content.strip()
        
        # Extract the first integer found in the response
        for char in raw_score:
            if char in "0123":
                return int(char)
        return 0
    except Exception as e:
        raise

#********************************************************************************************
# run_all
#********************************************************************************************     
async def run_all() -> list[dict]:
    """Run all 10 × 4 = 40 calls in parallel. Use asyncio.gather."""
    
    results_list = []
    tasks = []

    # snippet = job_snippets[9]
    # strategy = 'few_shot'

    for strategy in STRATEGIES:
        for job_snippet in job_snippets:
            task = run_one(strategy_name=strategy, snippet=job_snippet)
            tasks.append(task)
    # task = run_one(strategy_name=strategy, snippet=job_snippet)
    # tasks.append(task)
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    return results_list

#********************************************************************************************
# main
#******************************************************************************************** 
async def main():
    # results = await run_all()
    results = await run_all()

    for result in results:
        if isinstance( result, Exception):
            stars = '*' * 56
            print(f"\n{stars}\nException occurred\n{stars}\n{result}\n")
            sys.exit(1)
        
    print(f'\nGot {len(results)} results.\n')

    df = pd.DataFrame(results)
    columns_to_show = ["strategy", "snippet_id", "accuracy", "llm_judge_score", "latency_s", "raw_response"]
    print(df[columns_to_show].to_markdown(tablefmt="grid",index=False))

    summary = df.groupby('strategy').agg({
    'accuracy': 'mean',
    'parse_success': lambda x: x.mean() * 100,
    'llm_judge_score': 'mean',
    'cost_usd': 'sum',
    'latency_s': 'median',
}).round(3)

    summary.columns = ['Accuracy (mean of 3)', 'Parse rate (%)', 'Judge score', 'Total cost ($)', 'Latency p50 (s)']
    print(summary.to_markdown()) 

if __name__ == "__main__":
    asyncio.run(main()) 