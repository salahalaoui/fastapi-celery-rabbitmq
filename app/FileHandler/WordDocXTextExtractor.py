from app.FileHandler.TextExtractor import TextExtractor

import docx2txt

class WordDocXTextExtractor(TextExtractor):

    def extract_text(self):
        text = docx2txt.process(self.full_path)
        return text
