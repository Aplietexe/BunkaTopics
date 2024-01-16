import os
import random
import sys
import unittest

import pandas as pd
import plotly.graph_objects as go
from datasets import load_dataset
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub

from bunkatopics import Bunka

sys.path.append("../")

load_dotenv()

random.seed(42)

repo_id = "mistralai/Mistral-7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=repo_id,
    huggingfacehub_api_token=os.environ.get("HF_TOKEN"),
)


class TestBunka(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load a sample dataset
        dataset = load_dataset("rguo123/trump_tweets")
        docs = dataset["train"]["content"]
        docs = random.sample(docs, 2000)
        cls.bunka = Bunka()
        cls.bunka.fit(docs)

    def test_topic_modeling(self):
        # Test Topic Modeling
        n_clusters = 10
        df_topics = self.bunka.get_topics(n_clusters=n_clusters, min_count_terms=1)
        print(df_topics.name)
        self.assertIsInstance(df_topics, pd.DataFrame)
        self.assertEqual(len(df_topics), n_clusters)

        # Visualize Topics
        topic_fig = self.bunka.visualize_topics(width=800, height=800, show_text=True)
        topic_fig.show()
        self.assertIsInstance(topic_fig, go.Figure)

    def test_generative_names(self):
        n_clusters = 3

        self.bunka.get_topics(n_clusters=n_clusters, min_count_terms=1)
        df_topics_clean = self.bunka.get_clean_topic_name(llm=llm)
        print(df_topics_clean.name)
        self.assertIsInstance(df_topics_clean, pd.DataFrame)
        self.assertEqual(len(df_topics_clean), n_clusters)
        # Visualize Topics

    def test_bourdieu_modeling(self):
        bourdieu_fig = self.bunka.visualize_bourdieu(
            x_left_words=["past"],
            x_right_words=["future"],
            y_top_words=["men"],
            y_bottom_words=["women"],
            height=800,
            width=800,
            clustering=False,
            topic_gen_name=False,
            topic_n_clusters=3,
        )
        # bourdieu_fig.show()
        self.assertIsInstance(bourdieu_fig, go.Figure)

    def test_rag(self):
        top_doc_len = 3
        res = self.bunka.rag_query(
            query="What is great?",
            llm=llm,
            top_doc=top_doc_len,
        )

        result = res["result"]
        print(result)
        self.assertIsInstance(result, str)
        document_sources = res["source_documents"]
        self.assertEqual(len(document_sources), top_doc_len)

    def test_plot_query(self):
        query = "What is great?"
        fig_query, percent = self.bunka.visualize_query(
            query=query, width=800, height=800
        )
        self.assertIsInstance(fig_query, go.Figure)

    def test_boudieu_unique_dimension(self):
        fig_one_dimension, _ = self.bunka.visualize_bourdieu_one_dimension(
            left=["negative"], right=["positive"], explainer=False
        )
        self.assertIsInstance(fig_one_dimension, go.Figure)

    def test_topic_distribution(self):
        self.bunka.get_topics(n_clusters=3, min_count_terms=1)
        fig_distribution = self.bunka.get_topic_repartition()
        self.assertIsInstance(fig_distribution, go.Figure)


if __name__ == "__main__":
    unittest.main()
