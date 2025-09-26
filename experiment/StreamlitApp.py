

import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQgenerator import generate_chains
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

st.set_page_config(page_title="MCQ Generator", layout="wide")

# loading json file
with open(r"C:\Users\user\mcqgen\experiment\Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Generator App")

# create a form using st.form
with st.form("user_input"):
    uploaded_file = st.file_uploader("Upload a Pdf or TXT file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity level of Question", max_chars=20, placeholder="simple")
    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)

                # API call with token callback
                with get_openai_callback() as cb:
                    response = generate_chains({
                        'text': text,
                        'numbers': mcq_count,   # ✅ correct key
                        'subject': subject,
                        'tone': tone,
                        'response_json': json.dumps(RESPONSE_JSON)
                    })

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error while generating MCQs")

            else:
                st.success("MCQs generated successfully!")
                st.write(f"Total tokens: {cb.total_tokens}")
                st.write(f"Prompt tokens: {cb.prompt_tokens}")
                st.write(f"Completion tokens: {cb.completion_tokens}")
                st.write(f"Total cost: {cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get("quiz", None)

                    if quiz is not None:
                        table_data = get_table_data(quiz)

                        if table_data is not None:
                            # 🔧 Flatten nested dict into rows
                            rows = []
                            for key, value in table_data:
                                row = {"Question": value.get("mcq", "")}
                                options = value.get("option", {})
                                for opt_key, opt_value in options:
                                    row[opt_key.upper()] = opt_value
                                row["Correct"] = value.get("correct", "")
                                rows.append(row)

                            df = pd.DataFrame(rows)
                            df.index = df.index + 1

                            st.table(df)

                            st.text_area(label="Review", value=response.get("review", ""))
                        else:
                            st.error("Error in the table data")
                    else:
                        st.error("No quiz found in the response")
                else:
                    st.write(response)
