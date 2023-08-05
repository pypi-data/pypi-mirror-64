# -*- coding: utf-8 -*-
import json
from . import BASE_URL, session
from requests.exceptions import ConnectionError

ENDPOINT = "wordembedding/"

class WordEmbedding(object):

    @staticmethod
    def get_vectors_dict(words):
        #word2vec vectors

        api_url = BASE_URL + ENDPOINT + 'wordsvectorsdict'
        source = "Word2Vec"

        headers = {'Content-type': 'application/json'}

        data = {
            "source" : source,
            "words": words
        }

        try:
            r = session.post(api_url, data=json.dumps(data), headers=headers)
            print("status:", r.status_code)
            print("time:", r.elapsed.total_seconds())

            return r.json()
        except ConnectionError as e:
            print("ConnectionError: " + str(e))
            return None

    @staticmethod
    def get_synonym(word, topn=5):
        #word2vec vectors

        api_url = BASE_URL + ENDPOINT + 'wordsynonym'
        source = "Word2Vec"

        headers = {'Content-type': 'application/json'}

        data = {
            "source" : source,
            "word": word,
            "topn": topn
        }

        try:
            r = session.post(api_url, data=json.dumps(data), headers=headers)
            print("status:", r.status_code)
            print("time:", r.elapsed.total_seconds())

            return r.json()
        except ConnectionError as e:
            print("ConnectionError: " + str(e))
            return None

    @staticmethod
    def get_similarity_words(word1, word2):
        #word2vec vectors

        api_url = BASE_URL + ENDPOINT + 'wordssimilarity'
        source = "Word2Vec"

        headers = {'Content-type': 'application/json'}

        data = {
            "source" : source,
            "word1": word1,
            "word2": word2
        }

        try:
            r = session.post(api_url, data=json.dumps(data), headers=headers)
            print("status:", r.status_code)
            print("time:", r.elapsed.total_seconds())

            return r.json()
        except ConnectionError as e:
            print("ConnectionError: " + str(e))
            return None