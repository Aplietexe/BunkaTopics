from setuptools import setup, find_packages

dependencies = [
    "pandas>=2.0.2",
    "umap-learn>=0.5.3",
    "pydantic>=1.10.9",
    "loguru>=0.7.0",
    "langchain>=0.0.206",
    "plotly>=5.15.0",
    "textacy>=0.13.0",
    "gensim>=4.3.1",
    "sentence-transformers>=2.2.2",
    "openai>=0.28.0",
    "python-dotenv>=1.0.0",
    "matplotlib>=3.7.2",
    "datasets>=2.14.5",
    "chromadb>=0.4.13",
    "psutil>=5.9.7",
    "colorlog>=6.8.0",
]

dev = [
    "black ~= 23.0",
    "isort ~= 5.0",
    "pytest ~= 7.0",
    "pytest-cov",
    "twine ~= 4.0",
    "wheel",
]

docs = [
    "mkdocs>=1.1.2",
    "mkdocs-material>=8.1.4",
    "mkdocstrings>=0.24.0",
    "mkdocstrings-python>=1.8.0",
]

check = [
    "black ~= 23.0",
    "isort ~= 5.0",
    "mypy ~= 1.0.0",
    "pytest ~= 7.0",
    "pytest-cov",
    "ruff",
]


front = ["streamlit"]

setup(
    name="bunkatopics",
    packages=find_packages(exclude=["notebooks", "docs"]),
    version="0.43.1",
    author="Charles de Dampierre",
    author_email="charlesdedampierre@gmail.com",
    description="Bunkatopics is great",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=dependencies,
    extras_require={
        "test": dev,
        "docs": docs,
        "check": check,
    },
    python_requires=">=3.9",
)
