import csv
import logging
from pathlib import Path
from pydantic_classes import Question

logger = logging.getLogger(__name__)

#********************************************************************************************
# Get CSV file path
#********************************************************************************************
def get_csv_file_path() -> Path:
   current_file_path = Path(__file__).resolve()
   src_folder = current_file_path.parent
   week4_folder = src_folder.parent
   csv_file = week4_folder / "data" / "questions.csv"
   if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found at: {csv_file.relative_to(week4_folder.parent)}")
   
   return csv_file 

#********************************************************************************************
# Read questions from CSV file
#********************************************************************************************
def read_questions_from_csv(csv_file_path: Path) -> list[Question]:
    question_list = []    
    data_folder = csv_file_path.parent
    week4_folder = data_folder.parent

    with open(csv_file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the 'text' header line
        question_list = [Question(text=row[0].strip()) for row in reader if row]

    if not question_list:
        raise ValueError("Empty List")

    logger.info(f"Successfully loaded {len(question_list)} questions from {csv_file_path.relative_to(week4_folder)}")

    return question_list


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
        case _:  # Default / WHEN OTHERS
            raise ValueError(f"Unknown or unsupported model: {model}")    

    cost = (token_count_in * usd_per_m_input + token_count_out * usd_per_m_output) / 1_000_000
    return cost