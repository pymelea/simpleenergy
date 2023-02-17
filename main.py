# Import library 
import json
import requests
import PyPDF2
import os
import hashlib
from tqdm import tqdm

print(
    """
    
    ######################################################################
    #                                                                    #
    #  Created by: Lily Perera                                           #
    #  Email: lilycapetillo86@gmail.com                                  #
    #  Test for Junior/Pleno Python job                                  #
    #                                                                    #
    ######################################################################
    
    """
)


CODIG = input("Enter the code that you need to access: ")

print('\n')

class Files:
    """This is a class for work with the files

    Arguments:
        name { string}  -- Name the file
        hash_sha256 ( variable) -- Hash of file
    """

    name = ""
    hash_sha256 = ""

    def __init__(self, name, hash_sha256):
        self.name = name
        self.hash_sha256 = hash_sha256

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.hash_sha256)

    def toJson(self):
        return {
            "name": self.name,
            "hash_sha256": self.hash_sha256,
            "isValid": hash_file(self.name) == self.hash_sha256
        }


def get_names_files(codig):
    """ Function to get names of files

    Args:
        codig (String): Code that by prompt

    Returns:
        _String_: _Use for generate de name of files_
    """
    return ["arquivo1-{}.txt".format(codig), "arquivo1-{}.pdf".format(codig),
            "arquivo2-{}.txt".format(codig), "arquivo2-{}.txt".format(codig)]


def hash_file(path):
    """
    Funtion to compare hash of files 
    """
    hash = hashlib.sha256()
    hash.update(path.encode('utf-8'))
    return hash.hexdigest()


def get_request(url, type="txt"):
    """Function to get the response with the request library

    Args:
        url (link): Link the site to access
        type (str, optional): _description_. Defaults to "txt".

    Returns:
        pdf: PDF files text
        ó 
        text: File's text        
    """
    payload = {}
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if type == "pdf":
        return response.content
    return response.text


def get_content_data_by_pdf(path):
    """Function for get content of pdf documents

    Args:
        path (url): Url where get file 

    Returns:
        content: Get content of file
    """
    content = ''
    open("url.pdf", "wb").write(get_request(path, "pdf"))
    reader = PyPDF2.PdfReader('url.pdf')
    content = reader.pages[0].extract_text()
    os.remove("url.pdf")
    return content


def get_content_data_by_txt(path):
    """Function to get content of txt files

    Args:
        path (url): Url where get file 

    Returns:
        content: Get content of file
    """
    return get_request(path)


def get_content_data(path):

    type_file = path[-3:]
    if type_file == "pdf":
        return get_content_data_by_pdf(path)
    elif type_file == "txt":
        return get_content_data_by_txt(path)
    return ""


def get_data_by_files(codig):
    """Function to recive 

    Args:
        codig (String): Get the codig to access a url

    Returns:
        content: Get content of file and set in json format
    """
    content_file = []
    for i in tqdm(get_names_files(codig), desc="Generando datos del codigo {}".format(codig)):
        content = get_content_data(
            "https://simpleenergy.com.br/teste/{}".format(i))
        file = Files(i, content)
        content_file.append(file.toJson())
    return content_file


def get_file_by_code():
    """Function to get file for the input code 

    Returns:
        The data of files filter by CODIG
    """
    if CODIG == "321465" or CODIG == "98465":
        return get_data_by_files(CODIG)


def convert_in_json_file():
    """
    Function to convert info in to json file with the name of 
    code you use in the name

    Returns:
        data-CODIG.json encoding in UTF-8
    """
    data_files = get_data_by_files(CODIG)
    with open('data-{}.json'.format(CODIG), 'w', encoding='utf-8') as f:
        json.dump(data_files, f)


if __name__ == "__main__":
    """ 
    Run the function for each of your need
    """
    convert_in_json_file()
    print('\n')

