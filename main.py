# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Optional
from google.cloud import storage
import json
import os

import PyPDF2
from google.api_core.exceptions import InvalidArgument
import nest_asyncio
from IPython.display import Markdown, display
from dotenv import load_dotenv
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader


nest_asyncio.apply()
load_dotenv()

#llx-xKFKgy7Md6iWeLBVpVbv2of9MTQMZGcXcfGORZnprEBtqiQR
llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_num_pages_pypdf2(pdf_file_path):
    """Gets the number of pages in a PDF using PyPDF2"""
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)  
    return num_pages


  # noqa: E402


# bring in our LLAMA_CLOUD_API_KEY

# bring in deps


def llamaparser(llamaparse_api_key,file_path):
# set up parser
    parser = LlamaParse(
        api_key=llamaparse_api_key,
        result_type="markdown"  # "markdown" and "text" are available
    )

    # use SimpleDirectoryReader to parse our file
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files=[file_path], file_extractor=file_extractor).load_data()
    return documents

def download_blob_to_tempfile(bucket_name, blob_name):
    # Initialize a GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Create a temporary file
    temp_local_path = "temp_file.pdf"
    print(temp_local_path)
    # Download the blob to the temporary file
    blob.download_to_filename(temp_local_path)
    
    return temp_local_path

def get_files_and_summaries(bucket_name, prefix,llamaparse_api_key):
    files_and_summaries = {}

    # Initialize a GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    summary_list = []
    for blob in blobs:
        # Download the file to a temp location
        if blob.name == "Your directory":
            pass
        else:
            local_path = download_blob_to_tempfile(bucket_name, blob.name)
            page_no = get_num_pages_pypdf2(local_path)
            documents= llamaparser(llamaparse_api_key,local_path)
            selected_document_text = documents[0].text  # Adjust the index or selection appropriately
            sections = selected_document_text.split('\n---\n')
            try:
                for i in range(1,page_no+1):
                    
                    parts = blob.name.split('_')
                    summary_list. append(
                        {   
                            "file": blob.name,
                            "page_no": i,
                            "extracted_text": sections[i-1],
                        }
                    )
            finally:
                # Clean up: remove the temporary file
                os.remove(local_path)

    return summary_list

# Usage:
bucket_name = 'YOUR-BUCKET-NAME'
directory_prefix = 'YOUR-DIRECTORY-NAME'  # The prefix is like a directory path

try:
    
    summaries = get_files_and_summaries(bucket_name, directory_prefix,llamaparse_api_key)
    with open('file_summaries.json', 'w') as f:
        json.dump(summaries, f)
except Exception as e:
    print(f"Error during processing: {e}")

print("Processing complete.")
