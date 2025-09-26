# import os
# import json
# import traceback
# import pandas as pd
# from dotenv import load_dotenv
# from mcqgenerator.utils import read_file,get_table_data
# from mcqgenerator.logger import logging

# #importing necessary packages from langchain
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts  import PromptTemplate
# from langchain.chains import LLLMChain
# from langchain.chains import SequentialChain

# # load env vriables from the .env files
# load_dotenv()

# # acess the environment variable just like you would with os.version
# key=os.getenv("OPENAI_API_KEY")

# llm=ChatOpenAI(
#     open_api=key,model_name='gpt-4mini-o',temperature=0.5
# )

# template="""
# Text:{text}

# you are an expert MCqs maker, given the above text. It is your job to create a quiz of {numbers},
#  multiple quiz-wise questions for {subject}, students in {tone} tone. In curly brackets,
#    make sure the questions are not repeated and check all the questions to be confirming the text as well.
#      Make sure to format your response like response.json below and use it as a guide. Make sure to make dash {numbers} of MCqs
     
# # response.json.
# {response_json}"""

# quiz_generation_prompt=PromptTemplate(
#     input_variable=['text','number','subject','tone','response.json'],
#     template=template
# )
# # chain
# quiz_chain=LLMChain(llm=llm,
#                     prompt=quiz_generation_prompt,
#                     output_key='quiz',verbose=True)

# template2="""
# You are an expert teacher .given a multiple choice quiz for {subject} students.
# You need to evalute the complexity of the question and give a complete analysis of the quiz .only use 50 words for complexity 
# if the quiz is not per with the congitive and analytical abilities of the student.
# Update the quiz questions which needs to be changed and change the tone such that is perfectly fits the student level.
# Check the quiz answer realted to the content .
# Quiz_MCQS
# {quiz}

# """
# quiz_generation_prompt=PromptTemplate(
#     input_variable=['subject','quiz'],
#     template=template2
# )
# # chain2
# review_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,
#                       output_key='review',
#                       verbose=True
#                       )


# generate_chains = SequentialChain(
#     chains=[quiz_chain, review_chain], 
#     input_variables=['text', 'numbers', 'subject', 'tone', 'response_json'],  # ✅ cleaned
#     output_variables=["quiz", "review"],                                     # ✅ matches invoke
#     verbose=True
# )
import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
# from mcqgenerator.utils import read_file, get_table_data
# from mcqgenerator.logger import logging

# NEW ✅
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# # Importing necessary packages from langchain
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI   # if you installed `langchain-openai`

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Load env variables from the .env file
load_dotenv()

# Access the environment variable
key = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(
    openai_api_key=key, 
    model_name="gpt-4o-mini",
    temperature=0.5
)

# -------- Quiz Generation Prompt --------
template = """
Text: {text}

You are an expert MCQs maker. Given the above text, create {numbers} quiz questions 
for {subject} students in a {tone} tone. 

- Do not repeat questions.
- Ensure all questions are grounded in the text.
- Format your response using the schema below.

Response JSON:
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "numbers", "subject", "tone", "response_json"],
    template=template
)

quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz",
    verbose=True
)

# -------- Review Prompt --------
template2 = """
You are an expert teacher. Given a multiple-choice quiz for {subject} students,
evaluate the complexity of the questions and give a brief analysis (50 words max). 

- If questions are too hard or too easy, update them.
- Ensure tone and level match the students.
- Verify that answers are consistent with the text.
Quiz:
{quiz}
"""

review_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2
)

review_chain = LLMChain(
    llm=llm,
    prompt=review_prompt,
    output_key="review",
    verbose=True
)

# -------- Sequential Chain --------
generate_chains = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "numbers", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)
# quiz_chain = quiz_generation_prompt | llm
# review_chain = review_prompt | llm

# generate_chains = quiz_chain | review_chain

