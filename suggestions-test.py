from wordbooklib.wordbookclient import WordbookClient, SuggestionObject

client = WordbookClient()

suggestions = client.suggestions("hej så länge")
suggestion: SuggestionObject
for suggestion in suggestions:
    word = suggestion.word
    language = suggestion.language
    word_id = suggestion.word_id
    language_id = suggestion.language_id
    source_language_id = suggestion.source_language_id

    print(f"word ........: {word}")
    print(f"word id .....: {word_id}")
    print(f"language ....: {language}")

    definitions = suggestion.definitions()
    if not definitions:
        continue

    # loop definitions.
    for dictionary_id in definitions:
        print(f"dictionary id: {dictionary_id}")
        # the definition is a dict where the
        # named index is a dictionary id
        for definition in definitions[dictionary_id]:
            _definition = definition["definition"]
            dictionary = definition["dictionary"]
            word_id = definition["word_id"]
            dest_language_id = definition["dest_language_id"]
            src_language_id = definition["src_language_id"]

            print(f"dictionary ..: {dictionary}")
            print(f"definition ..: {_definition}\n")
