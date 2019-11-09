from wordbooklib.wordbookclient import WordbookClient, DictionaryObject

# create the client!
client = WordbookClient()
# download the dictionaries
dictionaries = client.dictionaries

dictionary: DictionaryObject
# loop over the dictionaries
for dictionary in dictionaries:
    # dictionary id eg. 20-11
    dict_id = dictionary.id
    # long name eg. Afrikaans-German
    long_name = dictionary.long_name
    # short name eg. afr-deu
    short_name = dictionary.short_name
    # alphabet of this dictionary url
    alphabet_url = dictionary.alphabet_url
    # extended database info url
    info_url = dictionary.info_url
    # url of the publisher!
    url_url = dictionary.url_url

    # print the dictionary info
    print(f"ID .......: {dict_id}")
    print(f"Short name: {short_name}")
    print(f"Long name : {long_name}\n")
    # print(dictionary.info)
    print(f"Long name : {dictionary.alphabet}\n")
