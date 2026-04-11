from setuptools import setup, find_packages

setup(
    name="charaka_vaidya",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.29.0",
        "pydantic>=2.6.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "groq>=0.4.2",
        "langchain>=0.1.14",
        "langchain-community>=0.0.31",
        "langchain-huggingface>=0.1.0",
        "langchain-chroma>=0.1.0",
        "sentence-transformers>=2.6.1",
        "chromadb>=0.4.24",
        "pypdf>=4.1.0",
        "httpx>=0.27.0",
        "reportlab>=4.1.0",
    ],
)