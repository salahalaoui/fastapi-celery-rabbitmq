from app.FileHandler.TextExtractor import TextExtractor

from pathlib import Path

class PlainTextExtractor(TextExtractor):

    def extract_text(self):
        try:
            return Path(self.full_path).read_text()
        except Exception as e:
            raise Exception(f'error while reading file {self.filename}')