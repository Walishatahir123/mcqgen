import os
import PyPDF2
import json
import traceback
from langchain_community.callbacks import get_openai_callback
# NEW
# from src.mcqgenerator.utils import read_file, get_table_data   # or whatever you really use


import PyPDF2

def read_file(file):
    try:
        # For PDF files
        if file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(file)  # ✅ modern PyPDF2 class
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""  # avoid None
            return text

        # For TXT files
        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")

        else:
            raise Exception("Unsupported file format. Only PDF and TXT files are supported.")

    except Exception as e:
        raise Exception(f"Error reading the file: {str(e)}")


# def get_table_data(quiz_str):
#     try:
#         # Load JSON string to dictionary
#         quiz_dict = json.loads(quiz_str)
#         quiz_table_data = []

#         # Iterate over the quiz dictionary and extract information
#         for key, value in quiz_dict.items():
#             mcq = value["quiz"]

#             # Format options as A -> Option text
#             options = " | ".join(
#                 [f"{option} -> {option_value}" for option, option_value in value["options"].items()]
#             )

#             correct = value["correct"]

#             # Append structured row
#             quiz_table_data.append({
#                 "MCQ": mcq,
#                 "Choices": options,
#                 "Correct": correct
#             })

#         return quiz_table_data

#     except Exception as e:
#         traceback.print_exception(type(e), e, e.__traceback__)
#         return False
def get_table_data(quiz_str):
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["quiz"]

            # Format options as A -> Option text
            options = " | ".join(
                [f"{option} -> {option_value}" for option, option_value in value["options"].items()]
            )

            correct = value["correct"]

            # Append structured row
            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })

            
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return []   # <- you fixed it to return [] not False
