---

# Document Processing with LLAMA Parser and Google Cloud Services

## Overview

This code demonstrates how to leverage LLAMA Parser, a natural language processing (NLP) tool, along with Google Cloud services for efficient document processing. By integrating LLAMA Parser with Google Cloud Storage and other services, you can streamline the extraction of structured data from unstructured text, such as PDF documents.

## Prerequisites

Before running the code, ensure you have the following:

- Access to Google Cloud Platform (GCP) with permissions to access Google Cloud Storage.
- LLAMA Cloud API key for using LLAMA Parser.
- Python environment with necessary dependencies installed (PyPDF2, google-cloud-storage, dotenv, IPython, and llama_parse).

## Setup

1. **LLAMA Parser API Key**: Set up LLAMA Parser API key by registering on the LLAMA website (provide link). Once registered, obtain the API key and store it in the `.env` file as `LLAMA_CLOUD_API_KEY`.

2. **Google Cloud Setup**: Ensure you have a GCP project with access to Google Cloud Storage. Set up authentication by either setting environment variables or using default credentials.

3. **Python Environment**: Install the required Python dependencies using pip:

   ```bash
   pip install PyPDF2 google-cloud-storage dotenv IPython llama_parse
   ```

4. **Code Configuration**: Update the `bucket_name` and `directory_prefix` variables in the code with your Google Cloud Storage bucket name and directory prefix.

## Usage

1. **Run the Script**: Execute the Python script `document_processing.py` to start the document processing workflow.

   ```bash
   python document_processing.py
   ```

2. **Processing Results**: Once the script completes execution, it generates a JSON file named `file_summaries.json` containing the extracted text and summaries for each document processed.

## Additional Notes

- Adjust the code as per your specific requirements, such as handling different file formats or customizing the parsing logic.
- Ensure proper error handling and resource cleanup to maintain reliability and efficiency in document processing workflows.

## References

- LLAMA Parser Documentation: https://docs.llamaindex.ai/en/stable/module_guides/loading/connector/llama_parse/
- Google Cloud Storage Documentation: https://cloud.google.com/storage/docs
- PyPDF2 Documentation: https://pypdf2.readthedocs.io/en/3.x/

---
