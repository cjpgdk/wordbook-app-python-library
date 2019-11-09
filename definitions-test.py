from wordbooklib.wordbookclient import WordbookClient, DictionaryObject


client = WordbookClient()

print(client.definitions(376038))

src_language_id = 1
dest_language_id = 2
print(client.definitions(None, "hej så länge", dest_language_id, src_language_id))

dest_language_id = 1
print(client.definitions(5876, None, None, src_language_id))
