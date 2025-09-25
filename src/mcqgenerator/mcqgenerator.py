import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from mcqgenerator.utils import read_file,get_table_data
from mcqgenerator.logger import logging

#importing necessary packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains import LLLMChain
from langchain.chains import SequentialChain

# load env vriables from the .env files
load_dotenv()

# acess the environment variable just like you would with os.version
key=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(
    open_api=key,model_name='gpt-4mini-o',temperature=0.5
)

template="""
Text:{text}

you are an expert MCqs maker, given the above text. It is your job to create a quiz of {numbers},
 multiple quiz-wise questions for {subject}, students in {tone} tone. In curly brackets,
   make sure the questions are not repeated and check all the questions to be confirming the text as well.
     Make sure to format your response like response.json below and use it as a guide. Make sure to make dash {numbers} of MCqs
     
# response.json.
{response_json}"""

quiz_generation_prompt=PromptTemplate(
    input_variable=['text','number','subject','tone','response.json'],
    template=template
)
# chain
quiz_chain=LLMChain(llm=llm,
                    prompt=quiz_generation_prompt,
                    output_key='quiz',verbose=True)

template2="""
You are an expert teacher .given a multiple choice quiz for {subject} students.
You need to evalute the complexity of the question and give a complete analysis of the quiz .only use 50 words for complexity 
if the quiz is not per with the congitive and analytical abilities of the student.
Update the quiz questions which needs to be changed and change the tone such that is perfectly fits the student level.
Check the quiz answer realted to the content .
Quiz_MCQS
{quiz}

"""
quiz_generation_prompt=PromptTemplate(
    input_variable=['subject','quiz'],
    template=template2
)
# chain2
review_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,
                      output_key='review',
                      verbose=True
                      )


generate_chains = SequentialChain(
    chains=[quiz_chain, review_chain], 
    input_variables=['text', 'numbers', 'subject', 'tone', 'response_json'],  # ✅ cleaned
    output_variables=["quiz", "review"],                                     # ✅ matches invoke
    verbose=True
)
