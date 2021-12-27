from abc import ABC, abstractmethod

class TextExtractor(ABC):

    def __init__(self, full_path, filename):
        self.full_path = full_path
        self.filename = filename
    @abstractmethod
    def extract_text(self):
        pass
