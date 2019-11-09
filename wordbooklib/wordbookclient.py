import requests


class WordbookClient:
    """
    Class WordbookClient, gives you the possibility to use the API of wordbook.cjpg.app
    """

    def __init__(self):
        # The base url for API requests
        self._API_BASE_URL = "https://wordbook.cjpg.app"
        # Api dictionaries path
        self._API_PATH_DICTIONARIES = "/dictionaries"
        # Api suggestions path
        self._API_PATH_SUGGESTIONS = "/suggestions"
        # Api definitions path
        self._API_PATH_DEFINITIONS = "/definitions"
        # required header for api requests
        self._headers = {
            "User-Agent": "Python-Wordbook-Library/1.0",
            "Accept": "application/json"
        }

    def call_api(self, url: str, args: dict = {}) -> requests.Response:
        """Send request to the api ensures that headers are set"""
        return requests.request("GET", url, headers=self._headers, params=args)

    def suggestions(self, query: str, dictionary_id: int = None):
        args = {"query": query}
        if dictionary_id:
            dict["language"] = dictionary_id
        req = self.call_api(f"{self._API_BASE_URL}{self._API_PATH_SUGGESTIONS}", args)
        req_res = req.json()

        if "suggestions" not in req_res:
            return None

        res = []
        for suggestion in req_res["suggestions"]:
            obj = SuggestionObject(suggestion)
            obj.set_wordbook_client(self)
            res.append(obj)
        return res

    @property
    def dictionaries(self):
        """Return a list of available dictionaries as DictionaryObject's"""
        req = self.call_api(f"{self._API_BASE_URL}{self._API_PATH_DICTIONARIES}")
        res = []
        for dictionary in req.json():
            obj = DictionaryObject(dictionary)
            obj.set_wordbook_client(self)
            res.append(obj)
        return res

    def definitions(self, word_id, word: str = None, src_language_id: int = None, dest_language_id: int = None):
        """
        Gets a list of definitions
        :param word_id:
        :param word:
        :param src_language_id:
        :param dest_language_id:
        :return:
        """
        args = {}
        if word_id and dest_language_id:
            args["id"] = word_id
            args["dest_language_id"] = dest_language_id
        elif word and src_language_id and dest_language_id:
            args["word"] = word
            args["src_language_id"] = src_language_id
            args["dest_language_id"] = dest_language_id
        elif word_id:
            args["id"] = word_id
        else:
            return None

        req = self.call_api(f"{self._API_BASE_URL}{self._API_PATH_DEFINITIONS}", args)
        return req.json()


class SuggestionObject:
    """
    A class to simplify the suggestion json object from the wordbook API!
    """
    _client: WordbookClient
    word: str
    word_id: int
    language: str
    language_id: int
    source_language_id: int

    def __init__(self, suggestion: dict, source_language_id: int = None):
        self.language = suggestion["data"]["language"]
        self.language_id = suggestion["data"]["language_id"]
        self.word = suggestion["data"]["word"]
        self.word_id = suggestion["data"]["word_id"]
        self.source_language_id = source_language_id

    def definitions(self, source_language_id: int = None):
        _definitions = self._client.definitions(self.word_id, None, self.language_id, self.source_language_id)
        return _definitions

    def set_wordbook_client(self, client: WordbookClient):
        """
        Sets the wordbook instance.
        :param client: The wordbook client object.
        :return:
        """
        self._client = client


class DictionaryObject:
    """
    A class to simplify the dictionary json object from the wordbook API!
    """
    _client: WordbookClient
    id: str
    long_name: str
    short_name: str
    alphabet_url: str
    info_url: str
    url_url: str
    source_language_id: int
    destination_language_id: int

    def __init__(self, dictionary: dict):
        # dictionary id eg. 20-11
        self.id = dictionary["id"]
        # long name eg. Afrikaans-German
        self.long_name = dictionary["long"]
        # short name eg. afr-deu
        self.short_name = dictionary["short"]
        # alphabet of this dictionary url
        self.alphabet_url = dictionary["alphabet"]
        # extended database info url
        self.info_url = dictionary["info"]
        # url of the publisher!
        self.url_url = dictionary["url"]

        _id = self.id.split('-')
        # The id of the source language of the dictionary
        self.source_language_id = _id[0]
        # The id of the destination language of the dictionary
        self.destination_language_id = _id[1]
        self._client = None

    @property
    def alphabet(self):
        """
        Gets the alphabet of this dictionary
        :return: str
        """
        _info = self._client.definitions(None, "00databasealphabet", self.source_language_id,
                                         self.destination_language_id)
        if len(_info[self.id]) > 0:
            return _info[self.id][0]["definition"]
        return None

    @property
    def info(self):
        """
        Gets the extended database info.
        :return: str
        """
        _info = self._client.definitions(None, "00databaseinfo", self.source_language_id, self.destination_language_id)
        if len(_info[self.id]) > 0:
            return _info[self.id][0]["definition"]
        return None

    def set_wordbook_client(self, client: WordbookClient):
        """
        Sets the wordbook instance.
        :param client: The wordbook client object.
        :return:
        """
        self._client = client
