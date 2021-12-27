
import re

def text_analysis(text):
    return len(re.findall(r'\w+', text))