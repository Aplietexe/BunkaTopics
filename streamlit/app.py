import sys

sys.path.append("../")

from bunkatopics import Bunka
import pandas as pd
import streamlit as st
from langchain.embeddings import HuggingFaceEmbeddings
import random

import os
from dotenv import load_dotenv

load_dotenv()
# Define a Streamlit app
st.title("Topic Modeling with Bunka")

# Upload CSV file
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

gen_ai = False

# from langchain.llms import OpenAI
# openai_api_key = st.text_input("Enter Your OpenAI API-key")
# generative_model = OpenAI(openai_api_key=openai_api_key)


if csv_file is not None:
    # Read CSV into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract text from the CSV column named 'text' (adjust column name as needed)
    text_data = df["text"].tolist()

    # Sample a subset of the text data (you can adjust the sample size)
    sample_size = 500
    full_docs = random.sample(text_data, sample_size)

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    bunka = Bunka(embedding_model=embedding_model)

    bunka.fit(full_docs)

    st.subheader("Topic Modeling Visualization")
    num_clusters = 5
    df_topics = bunka.get_topics(n_clusters=num_clusters)
    # if gen_ai:
    # df_clean_names = bunka.get_clean_topic_name(generative_model=generative_model)

    # Visualize topics
    topic_fig = bunka.visualize_topics(width=800, height=800)
    st.plotly_chart(topic_fig)

    """
    # Add a section for customizing the visualize_bourdieu parameters
    st.sidebar.title("Customize visualize_bourdieu Parameters")

    x_left_words = st.sidebar.text_input("x_left_words (comma-separated)", "war")
    x_right_words = st.sidebar.text_input("x_right_words (comma-separated)", "peace")
    y_top_words = st.sidebar.text_input("y_top_words (comma-separated)", "men")
    y_bottom_words = st.sidebar.text_input("y_bottom_words (comma-separated)", "women")

    # Display the visualize_bourdieu results
    if st.sidebar.button("Visualize Bourdieu"):
        bunka = fit_bunka(full_docs)
        bourdieu_fig = bunka.visualize_bourdieu(
            generative_model,
            x_left_words=x_left_words.split(","),
            x_right_words=x_right_words.split(","),
            y_top_words=y_top_words.split(","),
            y_bottom_words=y_bottom_words.split(","),
            height=800,
            width=800,
            label_size_ratio_label=50,
            display_percent=True,
            clustering=True,
            topic_n_clusters=10,
            topic_terms=5,
            topic_top_terms_overall=500,
            topic_gen_name=False,
        )
        st.subheader("Bourdieu Visualization")
        st.plotly_chart(bourdieu_fig)

    """
