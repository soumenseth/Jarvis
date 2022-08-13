from Utils.utils import *

sentence_types = {
    "exclamatory": 0, 
    "imperative": 1, 
    "interrogative": 2, 
    "assertive" : 3
    }

def get_labelled_data(sentence_data):
    labelled_sentence_types_data = []
    for sent_type in sentence_types.keys():
        labelled_sentence_types_data.extend({"label": sentence_types[sent_type], "text": sent} for sent in sentence_data[sent_type])
    return labelled_sentence_types_data

if __name__ == "__main__":
    all_sentences = read_json("resources/data/sentences_dataset.json")
    write_json("resources/data/labelled_sentence_type_dataset.json", get_labelled_data(all_sentences))
