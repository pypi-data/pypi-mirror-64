# -*- coding: utf-8 -*-
import json
from . import BASE_URL, session

ENDPOINT = "preprocessing/"

class PreProcessing(object):

    @staticmethod
    def get_clean_content(content, is_remove_stop_words = False, is_remove_url = False, is_steamming = False, is_lemmatizer = False):

        api_url = BASE_URL + ENDPOINT + 'cleancontent'
        headers = {'Content-type': 'application/json'}

        data = {
            "content": content,
            "isRemoveStopWords": is_remove_stop_words,
            "isSteamming": is_steamming,
            "isLemmatizer": is_lemmatizer,
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
    def tokenize_sentence(content, is_clean = False):

        api_url = BASE_URL + ENDPOINT + 'tokenizesentence'
        headers = {'Content-type': 'application/json'}

        data = {
            "content": content,
            "isClean": is_clean
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
    def tokenize_word(sentences):

        api_url = BASE_URL + ENDPOINT + 'tokenizeword'
        headers = {'Content-type': 'application/json'}

        data = {
            "sentences": sentences
        }

        try:
            r = session.post(api_url, data=json.dumps(data), headers=headers)

            print("status:", r.status_code)
            print("time:", r.elapsed.total_seconds())

            return r.json()
        except ConnectionError as e:
            print("ConnectionError: " + str(e))
            return None