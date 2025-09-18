# for installing local package
from setuptools import find_packages,setup

setup(
    name="walisha",
    version="0.0.1",
    author="Walisha",
    author_email="walishatahir00@gmail.com",
    packages=find_packages(),  # finds all packages with __init__.py
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2",
        "pandas"
    ],
    python_requires=">=3.10",
)
