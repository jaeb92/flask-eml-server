from .parser import Parser

class EmlParsingService():
    def __init__(self):
        self.parser = Parser()
        pass

    def get_eml_contents(self, eml_file):
        ef = self.parser.file_open(eml_file)

        parsed_eml = self.parser.parse(ef)
        # print('parsed_eml=',parsed_eml)
        eml_header = self.parser.get_header(parsed_eml)
        eml_body = self.parser.get_body(parsed_eml)
        eml_attachment = self.parser.get_attachment(parsed_eml)

        return eml_header, eml_body, eml_attachment

    def save_eml_attachment(self):
        pass