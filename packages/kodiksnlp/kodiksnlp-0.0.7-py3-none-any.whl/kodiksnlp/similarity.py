# -*- coding: utf-8 -*-
import json
from . import BASE_URL, session
from requests.exceptions import ConnectionError

ENDPOINT = "similarity/"

class Similarity(object):

    @staticmethod
    def get_content_to_many_similarity(similarity_type, content, content_list, threshold=0.8):
        #word2vec vectors

        api_url = BASE_URL + ENDPOINT + 'contentlistsimilarity'

        headers = {'Content-type': 'application/json'}

        data = {
            "similarity_type" : similarity_type,
            "threshold": threshold,
            "content": content,
            "content_list": content_list
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
    def get_content_to_many_similarity_and_citation(similarity_type, content, content_list, threshold_citation=0.9, threshold_similarity=0.8):
        #word2vec vectors

        api_url = BASE_URL + ENDPOINT + 'contentlistsimilarityandcitation'

        headers = {'Content-type': 'application/json'}

        data = {
            "similarity_type" : similarity_type,
            "threshold_citation": threshold_citation,
            "threshold_similarity": threshold_similarity,
            "content": content,
            "content_list": content_list
        }

        try:
            r = session.post(api_url, data=json.dumps(data), headers=headers)
            print("status:", r.status_code)
            print("time:", r.elapsed.total_seconds())

            return r.json()
        except ConnectionError as e:
            print("ConnectionError: " + str(e))
            return None


