from Utils.utils import *
from Parser.Entity.EntityParser import EntityParser


class Command:
    def __init__(self, text, platform):
        self.text = text
        self.platform = platform
        self.entity_parser = EntityParser()

    def get_command(self):
        command_entities, subject_entities = self.entity_parser.extract_entity(self.text)
        if command_entities and subject_entities:
            command_key = command_entities[0]['string_id'] + '_' + subject_entities[0]['string_id']
            command = SCRIPT_COMMAND[self.platform][command_key]
        else:
            command = False
        return command
