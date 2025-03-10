import os
import PyPDF2
from tqdm import tqdm
import re
import json


def read_pdfs_from_folder(folder_path):
    pdf_list = []

    # Loop through all files in the specified folder
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)

            # Open each PDF file
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                content = ""

                # Read each page's content and append it to a string
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    content += page.extract_text()

                # Add the PDF content to the list
                pdf_list.append({"content": content, "filename": filename})

    return pdf_list





from typing import Optional
import requests


def fetch_url_content(url: str) -> Optional[str]:
    """
    Fetches content from a URL by performing an HTTP GET request.

    Parameters:
        url (str): The endpoint or URL to fetch content from.

    Returns:
        Optional[str]: The content retrieved from the URL as a string,
                       or None if the request fails.
    """
    prefix_url: str = "https://r.jina.ai/"
    full_url: str = prefix_url + url  # Concatenate the prefix URL with the provided URL

    try:
        response = requests.get(full_url)  # Perform a GET request
        if response.status_code == 200:
            return response.content.decode('utf-8')  # Return the content of the response as a string
        else:
            print(f"Error: HTTP GET request failed with status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: Failed to fetch URL {full_url}. Exception: {e}")
        return None


if __name__ == "__main__":
    # url: str = "https://em360tech.com/tech-article/what-is-llama-3"
    # content: Optional[str] = fetch_url_content(url)

    # print(content)

    folder_path = "./pdfs"

    all_documents = read_pdfs_from_folder(folder_path)

    print(all_documents)