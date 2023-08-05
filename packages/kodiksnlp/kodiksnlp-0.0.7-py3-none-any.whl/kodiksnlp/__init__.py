# -*- coding: utf-8 -*-
import requests
session = requests.Session()

__title__ = 'KodiksNLP'
__version__ = "0.5"

#BASE_URL = "http://localhost:5010/api/"
BASE_URL = "http://40.91.125.237:5030/api/"

from .preprocessing import PreProcessing
from .wordembedding import WordEmbedding
from .similarity import Similarity