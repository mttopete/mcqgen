import json
import os
import traceback

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback

from src.mcqgenerator.logger import logging
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.utils import get_table_data, read_file

with open(r"C:\Users\Mateo\Desktop\mcqgen\response.json",'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQs Creator Application with LangChain")

ui = st.form("user_inputs")


uploaded_file = ui.file_uploader("Upload a PDF or txt file")

mcq_count = ui.number_input("No. of MCQs", min_value = 3,max_value = 50)

subject = ui.text_input("Insert Subject",max_chars=20)

tone = ui.text_input("Complexity Level of Questions",max_chars=20,placeholder="Simple")

button = ui.form_submit_button("Create MCQs")

if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("loading..."):
        try:
            text = read_file(uploaded_file)

            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
        except Exception as e:
            traceback.print_exception(type(e),e,e.__traceback__)
            ui.error("Error")
        
        else:
            print(f"Total Tokens:{cb.total_tokens}")
            print(f"Prompt Tokens:{cb.prompt_tokens}")
            print(f"Completion Tokens:{cb.completion_tokens}")
            print(f"Total Cost:{cb.total_cost}")
            if isinstance(response,dict):
                quiz = response.get("quiz",None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index+1
                        ui.table(df)
                        ui.text_area(label = "Review",value = response["review"])
                        st.download_button(
                        label = "Download MCQs",
                        data = response.get("quiz"),
                        file_name=f"{subject} MCQs",
                        )
                    else:
                        ui.error("Error in the table data")
            else:
                ui.write(response)
