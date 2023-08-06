"""
 # Download data and models
 download_bnpp_data(dir='./data/bnpp_newsroom_v1.1/')
 download_model(model='bert-squad_1.1', dir='./models')
"""

# It will be neccessary later
!pip install wget

import os
import wget

def download_covid_data(dir="."):
    """
    Download Kaggle COVID dataset

    Parameters
    ----------
    dir: str
        Directory where the dataset will be stored

    """

    dir = os.path.expanduser(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

    url = 'https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/download/all_sources_metadata_2020-03-13.csv'

    print("\nDownloading COVID data...")

    file = url.split("/")[-1]
    if os.path.exists(os.path.join(dir, file)):
        print(file, "already downloaded")
    else:
        wget.download(url=url, out=dir)
        
def download_model(model="scibert_scivocab_uncased", dir="."):
    """
    Download pretrained models

    Parameters
    ----------
    model: str
        Model to be download. It should be one of the models in the list:
        `bert-squad_1.1`, `distilbert-squad_1.1`

    dir: str
        Directory where the dataset will be stored

    """

    models_url = {
      # "bert-squad_1.1": "https://github.com/cdqa-suite/cdQA/releases/download/bert_qa/bert_qa.joblib",
      # "distilbert-squad_1.1": "https://github.com/cdqa-suite/cdQA/releases/download/distilbert_qa/distilbert_qa.joblib"
        "scibert_scivocab_uncased": "https://github.com/allenai/scibert/scibert_scivocab_uncased'"
    }

    if not model in models_url:
        print(
            "The model you chose does not exist. Please choose one of the following models:"
        )
        for model in models_url.keys():
            print(model)
    else:
        print("\nDownloading trained model...")

        dir = os.path.expanduser(dir)
        if not os.path.exists(dir):
            os.makedirs(dir)

        url = models_url[model]
        file = url.split("/")[-1]
        if os.path.exists(os.path.join(dir, file)):
            print(file, "already downloaded")
        else:
            wget.download(url=url, out=dir)

os.chdir("./models")
!tar -xvf "scibert_scivocab_uncased.tar"
   
#/models/scibert_scivocab_uncased/scibert_scivocab_uncased   
"""
download_model(model='scibert_scivocab_uncased', dir='./models')
os.chdir("./models")
!tar -xvf "scibert_scivocab_uncased.tar"
"""
