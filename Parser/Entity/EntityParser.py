from Utils.utils import *
import spacy
from spacy.matcher import PhraseMatcher
import os
import pickle


class EntityParser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.model_dir = os.path.join(MODELS, self.__class__.__name__)
        self.subject_entity_model_path = os.path.join(self.model_dir, "subject_entity.pickle")
        self.command_entity_model_path = os.path.join(self.model_dir, "command_entity.pickle")
        self.get_matchers()

    def train_subject_matcher(self):
        matcher = PhraseMatcher(self.nlp.vocab)

        for key in KEYWORDS_SUBJECT.keys():
            for pattern in KEYWORDS_SUBJECT[key]:
                matcher.add(key, [self.nlp(pattern)])
        with open(self.subject_entity_model_path, 'wb') as fh:
            pickle.dump(matcher, fh)
        return matcher

    def train_command_matcher(self):
        matcher = PhraseMatcher(self.nlp.vocab)

        for key in KEYWORDS_COMMAND.keys():
            for pattern in KEYWORDS_COMMAND[key]:
                matcher.add(key, [self.nlp(pattern)])
        with open(self.command_entity_model_path, 'wb') as fh:
            pickle.dump(matcher, fh)
        return matcher

    def get_matchers(self):
        if os.path.exists(self.subject_entity_model_path):
            self.subject_matcher = self.load_model(self.subject_entity_model_path)
        else:
            self.subject_matcher = self.train_subject_matcher()

        if os.path.exists(self.command_entity_model_path):
            self.command_matcher = self.load_model(self.command_entity_model_path)
        else:
            self.command_matcher = self.train_command_matcher()

    def load_model(self, model_path):
        with open(model_path, "rb") as fh:
            matcher = pickle.load(fh)
        return matcher

    def extract_entity(self, text):
        doc = self.nlp(text)
        subject_matches = self.subject_matcher(doc)
        command_matches = self.command_matcher(doc)
        subject_entities = []
        command_entities = []

        for match_id, start, end in subject_matches:
            string_id = self.nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            subject_entities.append({
                'match_id': match_id,
                'string_id': string_id,
                'start': start,
                'end': end,
                'text': span.text
            })

        for match_id, start, end in command_matches:
            string_id = self.nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            command_entities.append({
                'match_id': match_id,
                'string_id': string_id,
                'start': start,
                'end': end,
                'text': span.text
            })
        return command_entities, subject_entities
