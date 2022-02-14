import json

with open("data/google-rude-words.txt", 'r') as google_rude_words_file:
    google_rude_words_lines = google_rude_words_file.readlines()

with open("data/more-rude-words.json", 'r') as more_rude_words_json:
    more_rude_words_json_list = json.load(more_rude_words_json)

print(type(more_rude_words_json_list))

for word in google_rude_words_lines:
    more_rude_words_json_list.append(word.replace("\n", "").replace(" ", ""))

with open("rude-words.json", 'w') as rude_words_json:
    json.dump(more_rude_words_json_list, rude_words_json, indent=4)